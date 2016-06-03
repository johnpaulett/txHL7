import re
import six
from mock import Mock
from twisted.internet import defer
from twisted.trial.unittest import TestCase
from txHL7.mllp import IHL7Receiver, MinimalLowerLayerProtocol, MLLPFactory
from txHL7.receiver import MessageContainer, HL7MessageContainer, AbstractReceiver
from .utils import HL7_MESSAGE
from zope.interface import implementer


ACK_ID = "TESTACK"


class BaseTestCase(TestCase):
    def assertAck(self, actual, ack_code, sending_facility='BLDG4',
                  encoding='cp1252'):
        ack_re = (
            '^' +
            re.escape('\x0bMSH|^~\\&|GHH OE|' + sending_facility + '|GHH LAB|ELAB-3|') +
            r'\d+' +
            re.escape('||ACK^R01|' + ACK_ID + '|P|2.4\rMSA|') +
            ack_code + re.escape('|CNTRL-3456\x1c\x0d') +
            '$'
        )
        # re.match requires we compare bytestring to bytestring
        encoded_ack = ack_re.encode(encoding)
        self.assertTrue(re.match(encoded_ack, actual))


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
        return six.text_type(self.message.create_ack(ack_code, message_id=ACK_ID))


@implementer(IHL7Receiver)
class HL7CaptureReceiver(CaptureReceiver):
    # very simple, fake receiver that logs messages

    def parseMessage(self, raw_message):
        return HL7ControlMessage(raw_message)

    def getCodec(self):
        return 'cp1252', 'strict'


def create_protocol(receiver):
    protocol = MinimalLowerLayerProtocol()
    protocol.factory = MLLPFactory(receiver)
    protocol.transport = Mock()
    return protocol


class MinimalLowerLayerProtocolTest(BaseTestCase):
    def setUp(self):
        self.receiver = HL7CaptureReceiver()
        self.protocol = create_protocol(self.receiver)

    def testParseMessage(self):
        self.protocol.dataReceived(b'\x0b' + HL7_MESSAGE + b'\x1c\x0d')

        self.assertEqual(self.receiver.messages, [HL7_MESSAGE.decode('cp1252')])
        self.assertAck(self.protocol.transport.write.call_args[0][0], 'AA')

    def testUncaughtError(self):
        # throw a random exception, make sure Errback is used
        self.receiver.handleMessage = Mock()
        self.receiver.handleMessage.side_effect = Exception

        self.protocol.dataReceived(b'\x0b' + HL7_MESSAGE + b'\x1c\x0d')

        self.assertAck(self.protocol.transport.write.call_args[0][0], 'AR')
        self.assertEqual(len(self.flushLoggedErrors(Exception)), 1)

    def testParseMessageUnicode(self):
        message = HL7_MESSAGE.replace(b'BLDG4', b'x\x82y')
        self.protocol.dataReceived(b'\x0b' + message + b'\x1c\x0d')

        expected_message = HL7_MESSAGE.decode('cp1252').replace('BLDG4', u'x\u201ay')
        self.assertEqual(self.receiver.messages, [expected_message])

        self.assertAck(self.protocol.transport.write.call_args[0][0], 'AA',
                       sending_facility=u'x\u201ay')


class BasicCaptureReceiver(AbstractReceiver, CaptureReceiver):
    """AbstractReceiver subclass that just captures messages"""


class BasicReceiverTest(TestCase):
    def setUp(self):
        self.receiver = BasicCaptureReceiver()
        self.protocol = create_protocol(self.receiver)

    def testParseMessage(self):
        self.protocol.dataReceived(b'\x0b' + HL7_MESSAGE + b'\x1c\x0d')
        self.assertEqual(self.receiver.messages, [HL7_MESSAGE.decode('cp1252')])
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
        self.protocol.dataReceived(b'\x0b' + m.encode('cp1252') + b'\x1c\x0d')
        self.assertEqual(self.receiver.messages, [m])
        self.assertEqual(
            b"\x0bACK-AA\x1c\x0d",
            self.protocol.transport.write.call_args[0][0]
        )
