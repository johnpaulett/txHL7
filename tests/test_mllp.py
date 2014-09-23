import re
from mock import Mock
from twisted.internet import defer
from twistedhl7.mllp import IHL7Receiver, MinimalLowerLayerProtocol, MLLPFactory
from twistedhl7.receiver import MessageContainer, HL7MessageContainer, AbstractReceiver
from unittest import TestCase
from utils import HL7_MESSAGE
from zope.interface import implements


ACK_ID = "TESTACK"
EXPECTED_ACK_RE = '^' + re.escape('\x0bMSH|^~\\&|GHH OE|BLDG4|GHH LAB|ELAB-3|') + r'\d+' + re.escape('||ACK^R01|' + ACK_ID + '|P|2.4\rMSA|') + '{0}' + re.escape('|CNTRL-3456\x1c\x0d') + '$'


class CaptureReceiver(object):
    def __init__(self):
        self.messages = []
        self.ack_code = 'AA'

    def handleMessage(self, message_container):
        self.messages.append(message_container.raw_message)
        return defer.succeed(message_container.ack(self.ack_code))


class HL7ControlMessage(HL7MessageContainer):
    # Reimplement ACK so we can control message ID
    def ack(self, ack_code='AA'):
        return unicode(self.message.create_ack(ack_code, message_id=ACK_ID))


class HL7CaptureReceiver(CaptureReceiver):
    # very simple, fake receiver that logs messages
    implements(IHL7Receiver)

    def parseMessage(self, raw_message):
        return HL7ControlMessage(raw_message)

    def getCodec(self):
        return 'cp1252', 'strict'


def create_protocol(receiver):
    protocol = MinimalLowerLayerProtocol()
    protocol.factory = MLLPFactory(receiver)
    protocol.transport = Mock()
    return protocol


class MinimalLowerLayerProtocolTest(TestCase):
    def setUp(self):
        self.receiver = HL7CaptureReceiver()
        self.protocol = create_protocol(self.receiver)

    def testParseMessage(self):
        self.protocol.dataReceived('\x0b' + HL7_MESSAGE + '\x1c\x0d')

        self.assertEqual(self.receiver.messages, [HL7_MESSAGE])
        self.assertTrue(re.match(EXPECTED_ACK_RE.format('AA'),
                                 self.protocol.transport.write.call_args[0][0]))

    def testUncaughtError(self):
        # throw a random exception, make sure Errback is used
        self.receiver.handleMessage = Mock()
        self.receiver.handleMessage.side_effect = Exception

        self.protocol.dataReceived('\x0b' + HL7_MESSAGE + '\x1c\x0d')

        self.assertTrue(re.match(EXPECTED_ACK_RE.format('AR'),
                                 self.protocol.transport.write.call_args[0][0]))

    def testParseMessageUnicode(self):
        message = HL7_MESSAGE.replace('BLDG4', 'x\x82y')
        self.protocol.dataReceived('\x0b' + message + '\x1c\x0d')

        expected_message = unicode(HL7_MESSAGE).replace(u'BLDG4', u'x\u201ay')
        self.assertEqual(self.receiver.messages, [expected_message])

        expected_ack = EXPECTED_ACK_RE.replace('BLDG4', 'x\x82y')
        self.assertTrue(re.match(expected_ack.format('AA'),
                                 self.protocol.transport.write.call_args[0][0]))


class BasicCaptureReceiver(AbstractReceiver, CaptureReceiver):
    """AbstractReceiver subclass that just captures messages"""


class BasicReceiverTest(TestCase):
    def setUp(self):
        self.receiver = BasicCaptureReceiver()
        self.protocol = create_protocol(self.receiver)

    def testParseMessage(self):
        self.protocol.dataReceived('\x0b' + HL7_MESSAGE + '\x1c\x0d')
        self.assertEqual(self.receiver.messages, [HL7_MESSAGE])
        # No ACK
        self.assertFalse(self.protocol.transport.write.called)


class CustomMessage(MessageContainer):
    # Implement a custom non-HL7 ACK
    def ack(self, ack_code='AA'):
        return u"ACK-{0}".format(ack_code)


class CustomCaptureReceiver(AbstractReceiver, CaptureReceiver):
    """AbstractReceiver subclass that just captures messages"""
    def parseMessage(self, raw_message):
        return CustomMessage(raw_message)


class CustomReceiverTest(TestCase):
    def setUp(self):
        self.receiver = CustomCaptureReceiver()
        self.protocol = create_protocol(self.receiver)

    def testParseMessage(self):
        m = "HELLOTHERE"
        self.protocol.dataReceived('\x0b' + m + '\x1c\x0d')
        self.assertEqual(self.receiver.messages, [m])
        self.assertEqual("\x0bACK-AA\x1c\x0d", self.protocol.transport.write.call_args[0][0])
