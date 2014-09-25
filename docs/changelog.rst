==========
Change Log
==========

0.2.0 - September 2014
======================

* Abstract message into a separate class that is responsible for building ACK.
  This makes twistedhl7 useable with other HL7 parsing frameworks.
  Requires a new ``IHL7Receiver.parseMessage()`` interface method.
* Add message implementation based on python-hl7, using the new ACK functionality in 0.3.1
* Upgrade to latest python-hl7, v0.3.1, for ACK creation

0.1.0 - August 2014
===================

* twistd plugin.  Thanks to `Andrew Wason <https://github.com/rectalogic>`_
* Upgrade to latest python-hl7, v0.3.0, for correct MSH indexing

.. warning::

   python-hl7 v0.3.0 breaks `backwards compatibility
   <http://python-hl7.readthedocs.org/en/latest/changelog.html#changelog-0-3-0>`_.

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
