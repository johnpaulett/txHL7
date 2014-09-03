from zope.interface import Interface, implements
from twisted.python import log
from twisted.internet import defer
import hl7


class IHL7Receiver(Interface):
    """Interface that must be implemented by MLLP protocol receiver instances"""

    def parseMessage(unparsed_message):
        """Clients should parse the message and return an instance of :py:class:`twistedhl7.receiver.ParsedMessage` or subclass.

        :rtype: :py:class:`twistedhl7.receiver.ParsedMessage`
        """
        pass

    def handleMessage(parsed_message):
        """Clients must implement ``handleMessage``, which takes a ``parsed_message``
        argument that is the :py:class:`twistedhl7.receiver.ParsedMessage` instance
        returned from :py:meth:`twistedhl7.receiver.IHL7Receiver.parseMessage`.
        The implementation, if non-blocking, may directly return the ack/nack
        message or can return the ack/nack within a
        :py:class:`twisted.internet.defer.Deferred`. If the implementation
        involves any blocking code, the implementation must return the result as
        :py:class:`twisted.internet.defer.Deferred` (possibly by using
        :py:func:`twisted.internet.threads.deferToThread`), to prevent the event
        loop from being blocked.
        """
        pass

    def getCodec():
        """Clients should return the codec name [1]_ and error handling scheme [2]_,
        used when decoding into unicode.

        :rtype: tuple(codec, errors)

        .. [1] http://docs.python.org/library/codecs.html#standard-encodings
        .. [2] https://docs.python.org/2/library/codecs.html#codec-base-classes
        """
        pass


class AbstractReceiver(object):
    """Abstract base class implementation of :py:class:`twistedhl7.receiver.IHL7Receiver`"""
    implements(IHL7Receiver)

    def parseMessage(self, unparsed_message):
        return ParsedMessage(unparsed_message)

    def getCodec(self):
        return None, None


class AbstractHL7Receiver(AbstractReceiver):
    """Abstract base class implementation of :py:class:`twistedhl7.receiver.IHL7Receiver`

    :rtype: :py:class:`twistedhl7.receiver.HL7ParsedMessage`
    """
    def parseMessage(self, unparsed_message):
        return HL7ParsedMessage(unparsed_message)


class LoggingReceiver(AbstractHL7Receiver):
    """Simple MLLP receiver implementation that logs and ACKs messages."""
    def handleMessage(self, parsed_message):
        log.msg(parsed_message.unparsed_message)
        return defer.succeed(parsed_message.ack())


class ParsedMessage(object):
    """Base class for messages returned from :py:meth:`twistedhl7.receiver.IHL7Receiver.parseMessage`
    and passed to :py:meth:`twistedhl7.receiver.IHL7Receiver.handleMessage`
    """
    def __init__(self, unparsed_message):
        """Initialize a message with ``unparsed_message`` - an unparsed HL7 message
        (the MLLP wrapping around the HL7 message will be removed).
        The message will be in unicode, using the codec from
        :py:meth:`twistedhl7.receiver.IHL7Receiver.getCodec` to decode the message.
        """
        self.unparsed_message = unparsed_message

    def ack(self, ack_code='AA'):
        """Return unicode acknowledgement message, or None for no ACK.

        ``ack_code`` options are one of `AA` (accept), `AR` (reject), `AE` (error)

        :rtype: unicode
        """
        return None


class HL7ParsedMessage(ParsedMessage):
    """Message implementation that parses using `python-hl7 <http://python-hl7.readthedocs.org>`_"""
    def __init__(self, unparsed_message):
        super(HL7ParsedMessage, self).__init__(unparsed_message)
        self.message = hl7.parse(unparsed_message)

    def ack(self, ack_code='AA'):
        """Return HL7 ACK created from the source message.

        :rtype: unicode
        """
        return unicode(self.message.create_ack(ack_code))
