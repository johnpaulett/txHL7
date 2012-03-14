==========
Change Log
==========

0.0.3 - March 2012
==================

* Convert to unicode.  As soon as a message string is assembled, decode into
  unicode, using the codec specified by the implementation of
  ``IHL7Receiver.getCodec()`.  When writing an ACK, the message is re-encoded
  into that codec.

0.0.2 - September 2011
======================

* ACK^001 for acknowledging messages (adds python-hl7 dependency)
* Add errBack for catching unhandled errors that responds with reject (AR) ACK.

0.0.1 - September 2011
======================

* Initial basic MLLP implementation
