import sys
from twisted.internet import protocol, defer
from twisted.python import log
from twistedhl7.ack import ACK
from zope.interface import Interface, implements
from zope.interface.verify import verifyObject


class IHL7Receiver(Interface):
    # set error handling code
    # set system name
    # set 2.9.2.1 validation

    def handleMessage(message):
        """Clients should implement ``handleMessage``, which takes a ``message``
        argument, that is an unparsed HL7 message (the MLLP wrapping around the
        HL7 message will be removed). The message will be in unicode, using
        the codec from get_codec() to decode the message.

        The implementation, if non-blocking, may directly return the ack/nack
        message or can return the ack/nack within a
        :py:cls:`twisted.internet.defer.Deferred`. If the implementation
        involves any blocking code, the implementation must return the result as
        :py:cls:`twisted.internet.defer.Deferred` (possibly by using
        :py:func:`twisted.internet.threads.deferToThread`), to prevent the event
        loop from being blocked.
        """

    def getCodec():
        """Clients should return the codec name and error handling scheme,
        used when decoding into unicode.

        http://docs.python.org/library/codecs.html#standard-encodings
        https://docs.python.org/2/library/codecs.html#codec-base-classes
        """


class LoggingReceiver(object):
    """Simple MLLP receiver implementation that logs messages."""
    implements(IHL7Receiver)

    def handleMessage(self, message):
        log.msg(message)
        return defer.succeed(ACK(message))

    def getCodec(self):
        return 'ascii', 'replace'


class MinimalLowerLayerProtocol(protocol.Protocol):
    """
    Minimal Lower-Layer Protocol (MLLP) takes the form:

        <VT>[HL7 Message]<FS><CR>

    References:

        [1]: http://www.hl7standards.com/blog/2007/05/02/hl7-mlp-minimum-layer-protocol-defined/
        [2]: http://www.hl7standards.com/blog/2007/02/01/ack-message-original-mode-acknowledgement/
    """

    _buffer = ''
    start_block = '\x0b'  # <VT>, vertical tab
    end_block = '\x1c'  # <FS>, file separator
    carriage_return = '\x0d'  # <CR>, \r

    def dataReceived(self, data):

        # success callback
        def onSuccess(message):
            self.writeMessage(message)

        # try to find a complete message(s) in the combined the buffer and data
        messages = (self._buffer + data).split(self.end_block)
        # whatever is in the last chunk is an uncompleted message, so put back
        # into the buffer
        self._buffer = messages.pop(-1)

        for message in messages:
            # strip the rest of the MLLP shell from the HL7 message
            message = message.strip(self.start_block + self.carriage_return)

            # only pass messages with data
            if len(message) > 0:
                # convert into unicode (ACK's call to hl7.parse will explode if
                # it receives a non-ASCII byte string, so we just convert to
                # unicode here
                message = self.factory.decode(message)

                # error callback (defined here, since error depends on
                # current message).  rejects the message
                def onError(err):
                    reject = ACK(message, ack_code='AR')
                    self.writeMessage(reject)

                # have the factory create a deferred and pass the message
                # to the approriate IHL7Receiver instance
                d = self.factory.handleMessage(message)
                d.addCallback(onSuccess)
                d.addErrback(onError)

    def writeMessage(self, message):
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

    def handleMessage(self, message):
        # IHL7Receiver allows implementations to return a Deferred or the
        # result, so ensure we return a Deferred here
        return defer.maybeDeferred(self.receiver.handleMessage, message)

    def decode(self, value):
        # turn value into unicode using the receiver's declared codec
        if isinstance(value, str):
            return value.decode(self.encoding, self.encoding_errors)
        return unicode(value)

    def encode(self, value):
        # turn value into byte string using the receiver's declared codec
        if isinstance(value, unicode):
            return value.encode(self.encoding, self.encoding_errors)
        return value
