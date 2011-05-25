from mock import Mock
from twisted.internet import defer
from twistedhl7.mllp import MinimalLowerLayerProtocol
from unittest import TestCase

HL7_MESSAGE = 'MSH|^~\&|GHH LAB|ELAB-3|GHH OE|BLDG4|200202150930||ORU^R01|CNTRL-3456|P|2.4\rID|||555-44-4444||EVERYWOMAN^EVE^E^^^^L|JONES|196203520|F|||153 FERNWOOD DR.^^STATESVILLE^OH^35292||(206)3345232|(206)752-121||||AC555444444||67-A4335^OH^20030520\rOBR|1|845439^GHH OE|1045813^GHH LAB|1554-5^GLUCOSE|||200202150730||||||||555-55-5555^PRIMARY^PATRICIA P^^^^MD^^LEVEL SEVEN HEALTHCARE, INC.|||||||||F||||||444-44-4444^HIPPOCRATES^HOWARD H^^^^MD\rBX|1|SN|1554-5^GLUCOSE^POST 12H CFST:MCNC:PT:SER/PLAS:QN||^182|mg/dl|70_105|H|||F'

class CaptureReceiver(object):
    def __init__(self):
        self.messages = []
    def handleMessage(self, message):
        self.messages.append(message)
        return defer.succeed('hi')

class MinimalLowerLayerProtocolTest(TestCase):
    def testParseMessage(self):
        #factory = Mock()
        #factory.handleMessage.return_value = defer.succeed('hi')
        factory = CaptureReceiver()

        protocol = MinimalLowerLayerProtocol()
        protocol.factory = factory
        protocol.transport = Mock()

        protocol.dataReceived('\x0b' + 'payload' + '\x1c\x0d')

        self.assertEqual(factory.messages, ['payload'])

