from twisted.internet import defer
from twisted.python import log
from zope.interface import Interface, implementer
import hl7


class MessageContainer(object):
    """Base class for messages returned from :py:meth:`txHL7.receiver.IHL7Receiver.parseMessage`
    and passed to :py:meth:`txHL7.receiver.IHL7Receiver.handleMessage`
    """
    def __init__(self, raw_message):
        """Initialize a message with ``raw_message`` - an unparsed HL7 message
        (the MLLP wrapping around the HL7 message will be removed).
        The message will be in unicode, using the codec from
        :py:meth:`txHL7.receiver.IHL7Receiver.getCodec` to decode the message.
        """
        self.raw_message = raw_message

    def ack(self, ack_code='AA'):
        """Return unicode acknowledgement message, or None for no ACK.

        ``ack_code`` options are one of `AA` (accept), `AR` (reject), `AE` (error)

        :rtype: unicode
        """
        return None

    def err(self, failure):
        """Handle a twisted errback :py:class:`twisted.python.failure.Failure` ``failure``.
        Subclasses can override to log errors or handle them in a different way.
        Default implementation returns a rejection ACK.

        :rtype: unicode
        """
        # reject the message
        return self.ack(ack_code='AR')


class HL7MessageContainer(MessageContainer):
    """Message implementation that parses using `python-hl7 <http://python-hl7.readthedocs.org>`_"""
    def __init__(self, raw_message):
        super(HL7MessageContainer, self).__init__(raw_message)
        self.message = hl7.parse(raw_message)

    def ack(self, ack_code='AA'):
        """Return HL7 ACK created from the source message.

        :rtype: unicode
        """
        return str(self.message.create_ack(ack_code))


class IHL7Receiver(Interface):
    """Interface that must be implemented by MLLP protocol receiver instances"""

    def parseMessage(raw_message):
        """Clients should parse the message and return an instance of :py:class:`txHL7.receiver.MessageContainer` or subclass.

        :rtype: :py:class:`txHL7.receiver.MessageContainer`
        """
        pass

    def handleMessage(message_container):
        """Clients must implement ``handleMessage``, which takes a ``message_container``
        argument that is the :py:class:`txHL7.receiver.MessageContainer` instance
        returned from :py:meth:`txHL7.receiver.IHL7Receiver.parseMessage`.
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

    def getTimeout():
        """Clients should return the idle timeout in seconds, or None for no timeout

        :rtype: int
        """
        pass


@implementer(IHL7Receiver)
class AbstractReceiver(object):
    """Abstract base class implementation of :py:class:`txHL7.receiver.IHL7Receiver`"""

    message_cls = MessageContainer

    def parseMessage(self, raw_message):
        return self.message_cls(raw_message)

    def getCodec(self):
        return None, None

    def getTimeout(self):
        return None


class AbstractHL7Receiver(AbstractReceiver):
    """Abstract base class implementation of :py:class:`txHL7.receiver.IHL7Receiver`

    :rtype: :py:class:`txHL7.receiver.HL7MessageContainer`
    """
    message_cls = HL7MessageContainer


class LoggingReceiver(AbstractHL7Receiver):
    """Simple MLLP receiver implementation that logs and ACKs messages."""
    def handleMessage(self, message_container):
        log.msg(message_container.raw_message)
        return defer.succeed(message_container.ack())
