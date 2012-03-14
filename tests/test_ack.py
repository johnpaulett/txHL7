from twistedhl7.ack import ACK
from unittest import TestCase

from utils import HL7_MESSAGE

class ACKTest(TestCase):
    def test_aa(self):
        result = ACK(HL7_MESSAGE)
        expected = 'MSH|^~\\&|GHH OE|BLDG4|GHH LAB|ELAB-3|200202150930||ACK^001|CNTRL-3456|P|2.4\rMSA|AA|CNTRL-3456'

        self.assertEqual(expected, result)

    def test_ar(self):
        result = ACK(HL7_MESSAGE, 'AR')
        expected = 'MSH|^~\\&|GHH OE|BLDG4|GHH LAB|ELAB-3|200202150930||ACK^001|CNTRL-3456|P|2.4\rMSA|AR|CNTRL-3456'

        self.assertEqual(expected, result)

    def test_ae(self):
        result = ACK(HL7_MESSAGE, 'AE')
        expected = 'MSH|^~\\&|GHH OE|BLDG4|GHH LAB|ELAB-3|200202150930||ACK^001|CNTRL-3456|P|2.4\rMSA|AE|CNTRL-3456'

        self.assertEqual(expected, result)

    def test_unicode(self):
        # ACK takes and returns unicode.  The Factory is responsible for
        # decoding/encoding
        message = unicode(HL7_MESSAGE).replace(u'BLDG4', u'x\u201ay')
        result = ACK(message)

        expected = u'MSH|^~\\&|GHH OE|x\u201ay|GHH LAB|ELAB-3|200202150930||ACK^001|CNTRL-3456|P|2.4\rMSA|AA|CNTRL-3456'
        self.assertEqual(expected, result)
