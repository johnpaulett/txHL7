import sys

from twisted.internet import defer, protocol
from twisted.protocols.policies import TimeoutMixin
from zope.interface.verify import verifyObject
import six

from txHL7.receiver import IHL7Receiver


class MinimalLowerLayerProtocol(protocol.Protocol, TimeoutMixin):
    """
    Minimal Lower-Layer Protocol (MLLP) takes the form:

        <VT>[HL7 Message]<FS><CR>

    References:

    .. [1] http://www.hl7standards.com/blog/2007/05/02/hl7-mlp-minimum-layer-protocol-defined/
    .. [2] http://www.hl7standards.com/blog/2007/02/01/ack-message-original-mode-acknowledgement/
    """

    _buffer = b''
    start_block = b'\x0b'  # <VT>, vertical tab
    end_block = b'\x1c'  # <FS>, file separator
    carriage_return = b'\x0d'  # <CR>, \r

    def connectionMade(self):
        if self.factory.timeout is not None:
            self.setTimeout(self.factory.timeout)

    def dataReceived(self, data):
        self.resetTimeout()

        # success callback
        def onSuccess(message):
            self.writeMessage(message)

        # try to find a complete message(s) in the combined the buffer and data
        messages = (self._buffer + data).split(self.end_block)
        # whatever is in the last chunk is an uncompleted message, so put back
        # into the buffer
        self._buffer = messages.pop(-1)

        for raw_message in messages:
            # strip the rest of the MLLP shell from the HL7 message
            raw_message = raw_message.strip(self.start_block + self.carriage_return)

            # only pass messages with data
            if len(raw_message) > 0:
                # convert into unicode, parseMessage expects decoded string
                raw_message = self.factory.decode(raw_message)

                message_container = self.factory.parseMessage(raw_message)

                # error callback (defined here, since error depends on
                # current message).  rejects the message
                def onError(err):
                    reject = message_container.err(err)
                    self.writeMessage(reject)
                    return err

                # have the factory create a deferred and pass the message
                # to the approriate IHL7Receiver instance
                d = self.factory.handleMessage(message_container)
                d.addCallback(onSuccess)
                d.addErrback(onError)

    def writeMessage(self, message):
        if message is None:
            return
        # convert back to a byte string
        message = self.factory.encode(message)
        # wrap message in payload container
        self.transport.write(
            self.start_block + message + self.end_block + self.carriage_return
        )


class MLLPFactory(protocol.ServerFactory):
    protocol = MinimalLowerLayerProtocol

    def __init__(self, receiver):
        verifyObject(IHL7Receiver, receiver)
        self.receiver = receiver
        encoding = receiver.getCodec()
        if isinstance(encoding, tuple):
            encoding, encoding_errors = encoding
        else:
            encoding_errors = None
        self.encoding = encoding or sys.getdefaultencoding()
        self.encoding_errors = encoding_errors or 'strict'
        self.timeout = receiver.getTimeout()

    def parseMessage(self, message_str):
        return self.receiver.parseMessage(message_str)

    def handleMessage(self, message_container):
        # IHL7Receiver allows implementations to return a Deferred or the
        # result, so ensure we return a Deferred here
        return defer.maybeDeferred(self.receiver.handleMessage, message_container)

    def decode(self, value):
        # turn value into unicode using the receiver's declared codec
        if isinstance(value, six.binary_type):
            return value.decode(self.encoding, self.encoding_errors)
        return six.text_type(value)

    def encode(self, value):
        # turn value into byte string using the receiver's declared codec
        if isinstance(value, six.text_type):
            return value.encode(self.encoding, self.encoding_errors)
        return value
