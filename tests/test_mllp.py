from mock import Mock
from twisted.internet import defer
from twistedhl7.ack import ACK
from twistedhl7.mllp import IHL7Receiver, MinimalLowerLayerProtocol, MLLPFactory
from unittest import TestCase
from utils import HL7_MESSAGE
from zope.interface import implements


EXPECTED_ACK = 'MSH|^~\\&|GHH OE|BLDG4|GHH LAB|ELAB-3|200202150930||ACK^001|CNTRL-3456|P|2.4\rMSA|{0}|CNTRL-3456'


class CaptureReceiver(object):
    # very simple, fake receiver that logs messages
    implements(IHL7Receiver)

    def __init__(self):
        self.messages = []
        self.ack_code = 'AA'

    def handleMessage(self, message):
        self.messages.append(message)
        return defer.succeed(ACK(message, self.ack_code))

class MinimalLowerLayerProtocolTest(TestCase):
    def setUp(self):
        self.receiver = CaptureReceiver()

        self.protocol = MinimalLowerLayerProtocol()
        self.protocol.factory = MLLPFactory(self.receiver)
        self.protocol.transport = Mock()

    def testParseMessage(self):
        self.protocol.dataReceived('\x0b' + HL7_MESSAGE + '\x1c\x0d')

        self.assertEqual(self.receiver.messages, [HL7_MESSAGE])
        self.assertEqual(self.protocol.transport.write.call_args[0][0],
                         '\x0b' + EXPECTED_ACK.format('AA') + '\x1c\x0d')

    def testUncaughtError(self):
        # throw a random exception, make sure Errback is used
        self.receiver.handleMessage = Mock()
        self.receiver.handleMessage.side_effect = Exception

        self.protocol.dataReceived('\x0b' + HL7_MESSAGE + '\x1c\x0d')

        self.assertEqual(self.protocol.transport.write.call_args[0][0],
                         '\x0b' + EXPECTED_ACK.format('AR') + '\x1c\x0d')
