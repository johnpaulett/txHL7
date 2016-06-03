==========
Change Log
==========

.. _release-0.4.0:

0.4.0 - unreleased
==================

* Ported to Python 3.4. Support for Python 2.6 dropped. Currently supported
  platforms are Python 2.7 & 3.4. API remains the same, mostly test changes
  to more explicitly indicate bytestrings vs unicode strings. Also needed
  to convert to use zope.interface's ``@implementer()`` class advice instead
  of the ``implements()``.
* Use tox as primary test runner.


.. _release-0.3.0:

0.3.0 - November 2014
=====================

* Renamed project from twisted-hl7 to txHL7, to be in line with
  twisted's `Community Code
  <http://twistedmatrix.com/trac/wiki/CommunityCode>`_ recommendations.

.. warning::

   Please update your project to use the ``txHL7`` import instead
   of ``twistedhl7`` and replace "twisted-hl7" with "txHL7" in
   your setup.py or requirements.txt.

   If you perform a ``pip uninstall twisted-hl7``, ensure you do it
   before installing txHL7, since both packages use the
   :file:`twisted/plugins/mllp_plugin.py` twisted plugin, otherwise
   the twisted-hl7 uninstall will remove txHL7's version of the plugin.


0.2.2 - November 2014
=====================

* Add a description to setup.py.  Thanks `Low Kian Seong
  <https://github.com/lowks>`_`


0.2.1 - November 2014
=====================

* Delegate error processing to
  :py:meth:`txHL7.receiver.MessageContainer.err`, allowing subclasses
  to define logic.

.. _release-0.2.0:

0.2.0 - September 2014
======================

* Abstract message into a separate class that is responsible for building ACK.
  This makes txHL7 useable with other HL7 parsing frameworks.
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
