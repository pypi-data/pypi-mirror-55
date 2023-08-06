from PySide2.QtCore import QObject, QIODevice, QDataStream, QByteArray, QCborValue, QCborMap
from PySide2.QtNetwork import QLocalSocket
import sys
import re

# An exception class for the Ashes module
class AshesException(Exception):
    """Base class for other exceptions"""
    def __init__(self,*args,**kwargs):
        Exception.__init__(self,*args,**kwargs)

class AshesCouldNotConnectToServer(AshesException):
    """Raised when the socket cannot connect to the server"""
    def __init__(self, expression="", message=""):
        self.expression = expression
        self.message = message

class AshesLostConnectionToServer(AshesException):
    """Raised when the server stopped responding"""
    def __init__(self, expression="", message=""):
        self.expression = expression
        self.message = message

class AshesMissingCallbackFunction(AshesException):
    """Raised when callback function does not exist"""
    def __init__(self, expression="", message=""):
        self.expression = expression
        self.message = message

class AshesInvalidCallbackFunction(AshesException):
    """Raised when callback function either does not take the required arguments or does not return a model"""
    def __init__(self, expression="", message=""):
        self.expression = expression
        self.message = message

class Model(object):
    def __init__(self):
        pass

class Ashes(QObject):
    """This is a class for exchange between Ashes application and Python code"""

    def __init__(self, debugModeOn = False):
        QObject.__init__(self)
        
        # Set debug mode
        self.debugModeOn = debugModeOn

        # Create the model
        self.model = Model()

        # This is the callback function called whenever there is data available
        self.callbackFunction = None

        # This socket will 
        self.socket = QLocalSocket()

    def buildModelRecursively(self, dataMap, model):
        for key in dataMap.keys():
            if dataMap.value(key).isMap():
                modified_key = key.replace(" ", "")
                model.__setattr__(modified_key, Model())
                matches = re.match(r'^([a-zA-Z]+)([0-9]+)$', key)
                if matches:
                    elementType = matches.group(0)
                    elementIndex = matches.group(1)
                    if not hasattr(model, elementType):
                        model.__setattr__(elementType, {elementIndex: model.__getattribute__(modified_key)})
                    else:
                        model.__getattribute__(elementType)[elementIndex] = model.__getattribute__(modified_key)

                self.buildModelRecursively(dataMap(key), model.__getattribute__(modified_key))
            else:
                model.__setattr__(modified_key, dataMap.value(key).toDouble())


    def updateModelRecursively(self, dataMap, model):
        for key in dataMap.keys():
            modified_key = key.replace(" ", "")
            if dataMap.value(key).isMap():
                self.updateModelRecursively(dataMap(key), model.__getattribute__(modified_key))
            else:
                model.__setattr__(modified_key, dataMap.value(key).toDouble())

    def makeModelToCbor(self, model):
        cbor = QCborMap()
        for key in model.__dict__.keys():
            if key[:1] != '_':
                if type(model.__getattribute__(key)) == type(model):
                    cbor.insert(key, self.makeModelToCbor(model.__getattribute__(key)))
                else:
                    cbor.insert(key, QCborValue(model.__getattribute__(key)))
        return cbor

    def start(self, callbackFunction):
        # Set up the local socket
        self.socket.connectToServer("ASHES-SCRIPT", QIODevice.ReadWrite)

        # Check if the socket can connect - otherwise, raise an exception
        if not self.socket.waitForConnected():
            raise AshesCouldNotConnectToServer(self.socket.error())
        
        if self.debugModeOn:
            print("Successfully connected to Ashes application.")

        # Wait for the server to write data
        if not self.socket.waitForReadyRead():
            raise AshesLostConnectionToServer()

        if self.debugModeOn:
            print("Data received from server")

        # Read the data from the server
        message = ""
        data = QByteArray()
        while True:
            stream = QDataStream(self.socket, QIODevice.ReadOnly)
            stream.startTransaction()
            message = stream.readQString()
            stream >> data

            if stream.commitTransaction():
                break
            else:
                data.clear()

            if not self.socket.state() == QLocalSocket.ConnectedState:
                sys.exit()

        if self.debugModeOn:
            print("Message: {}\nSize: {}".format(message, data.size()))

        # Make a QCborValue from the received data
        cborValue = QCborValue.fromCbor(data)

        # Make data to map
        dataMap = data.toMap()

        # Build a model from the data
        self.model = Model()
        self.buildModelRecursively(dataMap, self.model)

        # Check if there is a callback function defined
        # we don't do anything with the modified model yet
        try:
            modifiedModel = callbackFunction(self.model)
            
            if not type(modifiedModel) == type(model):
                raise AshesInvalidCallbackFunction()
        except NameError:
            raise AshesMissingCallbackFunction()
        except TypeError:
            raise AshesInvalidCallbackFunction()

        # Tell the server that we are done here
        block = QByteArray()
        stream = QDataStream(block, QIODevice.WriteOnly)
        stream.writeQString("success")
        bytesWritten = self.socket.write(block)

        # Now we are going in a loop for each time step
        while True:
            # First wait for the server to send an update command
            message = ""
            data = QByteArray()
            while True:
                stream = QDataStream(self.socket, QIODevice.ReadOnly)
                stream.startTransaction()
                message = stream.readQString()
                stream >> data

                if stream.commitTransaction():
                    break
                else:
                    data.clear()

                if not self.socket.state() == QLocalSocket.ConnectedState:
                    sys.exit()

            # Check the message
            if message == "update":
                # Make a QCborValue from the received data
                cborValue = QCborValue.fromCbor(data)

                # Make data to map
                dataMap = data.toMap()

                # Update our model
                self.updateModelRecursively(dataMap, self.model)

                # Call the callback function
                self.model = callbackFunction(self.model)

                # Convert model back to cbor
                cbor = self.makeModelToCbor(self.model)

                 # Tell the server that we are done here
                block = QByteArray()
                stream = QDataStream(block, QIODevice.WriteOnly)
                stream.writeQString("success")
                stream.write(cbor)
                bytesWritten = self.socket.write(block)



