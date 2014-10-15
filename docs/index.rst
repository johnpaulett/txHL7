===========
twisted-hl7
===========

twisted-hl7 provides a network-level HL7 implementation, the Minimal Lower Level
Protocol (MLLP).

Current Status
==============

twisted-hl7 is still *alpha* quality software. The API can still drastically
change before a "1.0" release.  Currently, only the bare-minimum of MLLP is
implemented.  However, we are working towards more complete support
of the specification.

python-hl7 vs twisted-hl7
=========================

`python-hl7 <http://python-hl7.readthedocs.org>`_ and twisted-hl7 are
complementary python modules for handling HL7 data.

* twisted-hl7 provides a network-level HL7 implementation (MLLP)
* python-hl7 provides a HL7 parsing implementation

twisted-hl7 and python-hl7 can (and often are) used together.  But, the modular
approach allows a developer to substitute out either component.  For example,
a developer may not wish to use Twisted, instead he may elect to implement
the TCP server using :py:mod:`socket` or :py:mod:`asyncore`.  Likewise, a developer
may wish to use an alternate HL7 parsing routine, but still use twisted-hl7.

As of the :ref:`0.2.0 release <release-0.2.0>`, there is a streamlined way
to use python-hl7 as the parser for twisted-hl7, via the
:py:class:`twistedhl7.receiver.AbstractHL7Receiver`.

Contents
========

.. toctree::
   :maxdepth: 2

   usage
   custom-receiver
   api
   changelog
   license
   authors

References
==========

* http://archive.hl7.org/v3ballotarchive/v3ballot7/html/foundationdocuments/transport/transport-mllp.htm

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

