"""Messages that obey the blackout protocol, can use this class"""

# System imports
import os
import socket#, _thread
import time
import json, uuid
import traceback
import sys, io
import logging
from collections import defaultdict
import ssl
import certifi
from threading import Thread



# 3rd party imports

# local imports
from .btWebsocket import *
# from websocket import *
from .message import Message
from .nexusExceptions import *

# end file header
__author__      = "Marc Fiedler, Gheorghe Lisca, Adrian Lubitz"
__copyright__   = "Copyright (c)2017, Blackout Technologies"

class NexusConnector():
    """The NexusConnector handles everything from connecting, subscibing and publishing messages in the btNexus"""
    version = "3.1"

    def __init__(self, connectCallback, parent,  token,  axonURL,  debug):
        """
        Sets up all configurations.

        :param connectCallback: function pointer to the onConnected of the Node using this NexusConnector
        :type connectCallback: function pointer
        :param parent: The Node using this NexusConnector (also used for some logging stuff)
        :type parent: Node
        :param token: AccessToken for the btNexus
        :type token: String
        :param axonURL: URL for the Axon(InstanceURL)
        :type axonURL: String
        :param debug: switch for debug messages
        :type debug: bool
        """
        #Set env for certs if not set
        os.environ["WEBSOCKET_CLIENT_CA_BUNDLE"] = certifi.where()
        self.debugTopic = "ai.blackout.debug"
        self.warningTopic = "ai.blackout.warning"
        self.errorTopic = "ai.blackout.error"
        self.parent = parent
        self.parentName = self.parent.nodeName
        self.nodeId = str(uuid.uuid4())
        self.protocol = "wss"
        self.token = token
        self.axon = axonURL
        self.debug = debug


        self.wsConf = self.protocol + "://"+ str(self.axon)

        self.ws = None
        self.logger = logging.getLogger('websocket')
        self.errHandler = logging.StreamHandler(self.parent)
        self.errHandler.setLevel(logging.ERROR)
        self.logger.addHandler(self.errHandler)
        # Adding handler for Debug
        self.dbgStream = io.StringIO()
        self.dbgStream.write = self.parent.publishWarning
        self.dbgHandler = logging.StreamHandler(self.dbgStream)
        self.dbgHandler.setLevel(logging.DEBUG)

        self.connectCallback = connectCallback
        self.callbacks = defaultdict(lambda: defaultdict(dict)) # saves every callback under a group and a topic, even if joining the group wasnt successufull(Messages will be filtered by the Axon)

        self.isConnected = False
        self.isRegistered = False
        sys.stderr = self.parent

    @classmethod
    def copyNexusForReconnect(cls, oldNexusConnector):
        """
        Returns a fresh nexusConnector to reconnect.
        """
        newNexusConnector = NexusConnector(oldNexusConnector.connectCallback, oldNexusConnector.parent, oldNexusConnector.token, oldNexusConnector.axon, oldNexusConnector.debug)
        newNexusConnector.nodeId = oldNexusConnector.nodeId
        #newNexusConnector.callbacks = oldNexusConnector.callbacks
        return newNexusConnector

    def __onConnected(self):
        """
        Shadow function for the connectCallback
        """
        self.connectCallback()
        self.publishDebug("{} succesfully started :)".format(self.parentName))

    def callbackManager(self, msg):
        """
        Links the Message to the corrosponding Callback

        :param msg: Incoming Message from the btNexus
        :type msg: Message
        """
        try:
            topic = msg["topic"].replace("ai.blackout.", "")
            callbackName = list(msg["payload"].keys())[0]
            params = msg["payload"][callbackName]
            group = msg["group"]
            if callbackName in self.callbacks[group][topic].keys():
                Thread(target=self.executeCallback, args=(group, topic, callbackName, params)).start()
                #self.executeCallback(group, topic, callbackName, params)
            else:
                error = NoCallbackFoundException("Callback {} doesn't exist in node {} on topic {} in group {}".format(callbackName, self.parentName, topic, group))
                self.publishDebug(str(error))
                return error
        except Exception as e:
            error = NoCallbackFoundException(str(e))
            self.publishError(str(error))
            return error

    def executeCallback(self, group, topic, callbackName, params):
        """
        This executes the given callback with the given params and send the response

        :param group: Name of the group
        :type group: String
        :param topic: Name of the topic
        :type topic: String
        :param callbackName: Name of the callback
        :type callbackName: String
        :param params: the params for the callback either as list or keywordDict
        :type params: list or keywordDict
        """
        if type(params) == list:
            retVal = self.callbacks[group][topic][callbackName](*params)
        elif type(params) == dict:
            retVal = self.callbacks[group][topic][callbackName](**params)
        else:
            self.publishError("Parameters can either be given as a list or a keywordDict.")
            return

        reply = Message("publish")
        reply["payload"] = {callbackName + "_response":{"orignCall":callbackName ,"originParams":params, "returnValue": retVal}}
        reply["topic"] = "ai.blackout." + topic
        reply["group"] = group
        reply["host"] = socket.gethostname()
        self.publish(reply)

    def setDebugMode(self, mode):
        """
        DEPRECATED
        Activate/Deactivate the Debug trace

        """
        #enableTrace(mode)#TODO:gucken, wo das hingesendet wird und das auf ai.blackout.error streamen
        if mode:
            self.logger.addHandler(self.dbgHandler)
            # self.logger.warning("Debug is active")
        else:
            self.logger.removeHandler(self.dbgHandler)

    def listen(self, ping_interval=None):
        """Start listening on Websocket communication"""
        self.ws = WebSocketApp(self.wsConf,
            on_message = self.onMessage, on_error = self.onError,
            on_close = self.onClose, on_open=self.onOpen, on_ping=self.onPing)

        #self.ws.on_open = self.onOpen

        #self.setDebugMode(self.parent.debug)
        #self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
        sslopt = None
        if( "DISABLE_SSL_VERIFY" in os.environ ):
            sslopt = {"cert_reqs": ssl.CERT_NONE}

        self.ws.run_forever(sslopt=sslopt, ping_interval=ping_interval)

        # self.ws.run_forever(sockopt=None, sslopt=None,
        #             ping_interval=0, ping_timeout=None,
        #             http_proxy_host=None, http_proxy_port=None,
        #             http_no_proxy=None, http_proxy_auth=None,
        #             skip_utf8_validation=False,
        #             host=None, origin=None)

    # def onPong(self, socket, payload):
    #     print("received Pong")
        

    def onPing(self):
        """
        react with a pong to a ping
        """
        self.ws.sock.pong("")

    def join(self, group):
        """
        Join a specific group

        :param group: Name of the group
        :type group: String
        """
        join = Message("join")
        join["groupName"] = group
        self.publish(join)

    def leave(self, group):
        """
        leave a specific group

        :param group: Name of the group
        :type group: String
        """
        leave = Message('leave')
        leave["groupName"] = group
        self.publish(leave)



    def subscribe(self, group, topic, callback, funcName = None):
        """
        Subscribe to a group & topic with a callback

        :param group: Name of the group
        :type group: String
        :param topic: Name of the topic
        :type topic: String
        :param callback: function pointer to the callback
        :type callback: function pointer
        :param funcName: Name of the function. If not set this is the name of the function in the implementation(needed if you want to link a function to a different name)
        :type funcName: String
        """
        if not self.isConnected:
            raise NexusNotConnectedException()
        if group not in self.callbacks:
            self.join(group)
        if topic not in self.callbacks[group]: #first subscribtion
            sub = Message("subscribe")
            sub["topic"] = "ai.blackout.{}".format(topic)
            self.publish(sub)
        if funcName == None:
            funcName = callback.__name__
        self.callbacks[group][topic][funcName] = callback
        # print ("self.callbacks: {}".format(self.callbacks))

    def unsubscribe(self, group, topic):
        """
        unsubscribe from a group & topic

        :param group: Name of the group
        :type group: String
        :param topic: Name of the topic
        :type topic: String
        """
        self.callbacks[group][topic] = {}

    def publish(self, message):
        """
        Publish a message on the btNexus

        :param message: A Message to send into the btNexus
        :type message: Message
        """
        # Add the node id as a source to that this node does not receive its own
        # messages
        message['nodeId'] = self.nodeId
        if self.isConnected:
            self.ws.send(message.getJsonContent())
        else:
            raise NexusNotConnectedException()

    def publishDebug(self, debug):
        """
        Publish a Debug message on the btNexus if debug is active

        :param debug: A Message to send to the debug topic
        :type debug: String
        """
        if self.debug:
            print(debug)
            deb = Message("publish")
            deb["group"] = "blackout-global"
            deb["topic"] = self.debugTopic
            deb["payload"] = {"debug":debug}
            self.publish(deb)


    def publishWarning(self, warning):
        """
        Publish a Warning message on the btNexus

        :param warning: A Message to send to the warning topic
        :type warning: String
        """
        print(warning)
        warn = Message("publish")
        warn["group"] = "blackout-global"
        warn["topic"] = self.warningTopic
        warn["payload"] = {"warning":warning}
        self.publish(warn)

    def publishError(self, error):
        """
        Publish a Error message on the btNexus

        :param error: A Message to send to the error topic
        :type error: String
        """
        print(error)
        err = Message("publish")
        err["group"] = "blackout-global"
        err["topic"] = self.errorTopic
        err["payload"] = {"error":error}
        self.publish(err)



    def onMessage(self, ws, message):
        """
        React on a incoming Message and decide what to do.

        :param ws: a pointer to the Websocket object
        :type ws: WebSocketApp
        :param message: The message to react on
        :type message: String
        """
        # print("Got Message: {}".format(message))
        msg = Message()
        msg.loadFromJsonString(message)
        #print("Frisch geladene Message: {}".format(msg.data))
        if( msg["api"]["intent"] == "registerSuccess" ):
            print("[{}]: Registered successfully".format(self.parentName))
            self.isRegistered = True
            self.isConnected = True
            self.__onConnected()
            #TODO: check here for versionmissmatch - just like in java
        elif ( msg["api"]["intent"] == "registerFailed" ):
            print("[{}]: Register failed with reason: {}".format(self.parentName, msg["reason"]))
        elif( msg["api"]["intent"] == "subscribeSuccess" ):
            print("[{}]: Subscribed to: {}".format(self.parentName, msg["topic"]))
        elif ( msg["api"]["intent"] == "subscribeFailed" ):
            print("[{}]: Failed to Subscribed to: {}".format(self.parentName, msg["topic"]))
        elif ( msg["api"]["intent"] == "joinSuccess" ):
            print("[{}]: Joined Group: {}".format(self.parentName, msg["groupName"]))
        elif ( msg["api"]["intent"] == "joinFailed" ):
            print("[{}]: Failed to join Group: {}".format(self.parentName, msg["groupName"]))
        elif ( msg["api"]["intent"] == "leaveSuccess" ):
            print("[{}]: Left Group: {}".format(self.parentName, msg["groupName"]))
        elif ( msg["api"]["intent"] == "leaveFailed" ):
            print("[{}]: Failed to leave Group: {}".format(self.parentName, msg["groupName"]))
        elif ( msg["api"]["intent"] == "unsubscribeSuccess" ):
            print("[{}]: Unsubscribed from topic: {}".format(self.parentName, msg["topic"]))
        elif ( msg["api"]["intent"] == "unsubscribeFailed" ):
            print("[{}]: Failed to unsubscribe from topic: {}".format(self.parentName, msg["topic"]))
        else:
            # Interaction is only allowed with registered nodes
            if( self.isRegistered ):
                try:
                    # Call topic callback with this message
                    self.callbackManager(msg)
                except Exception:
                    self.publishError(traceback.format_exc())




    def onError(self, ws, error):
        """
        React on a incoming Errors.

        :param ws: a pointer to the Websocket object
        :type ws: WebSocketApp
        :param error: The error to react on
        :type meserrorsage: exception object
        """
        self.publishError("[{}] Error: {}".format(self.parentName, error))

    def onClose(self, ws):
        """
        React on a closing the connection

        :param ws: a pointer to the Websocket object
        :type ws: WebSocketApp
        """
        self.isConnected = False
        print("[Nexus]: Connection closed")
        self.parent.onDisconnected()

    def onOpen(self, ws):
        """
        Things to do, when the WebsocketConnection is opened.

        :param ws: a pointer to the Websocket object
        :type ws: WebSocketApp
        """
        # print("Registering in the Nexus")
        msg = Message("register")
        msg["token"] = self.token #TODO: is this the access token? for older version use interface
        msg["host"] = socket.gethostname()
        msg["ip"] = "127.0.0.1" #socket.gethostbyname(socket.gethostname())
        msg["id"] = self.nodeId
        msg["node"] = {}    #TODO: What should be in this field?
        self.ws.send(msg.getJsonContent())
