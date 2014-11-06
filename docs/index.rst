=======================================
txHL7 -- Providing HL7 MLLP via twisted
=======================================

txHL7 provides a network-level HL7 implementation, the Minimal Lower Level
Protocol (MLLP) using Python's `twisted <https://twistedmatrix.com/trac/>`_.

Current Status
==============

txHL7 is still *alpha* quality software. The API can still drastically
change before a "1.0" release.  Currently, only the bare-minimum of MLLP is
implemented.  However, we are working towards more complete support
of the specification.

python-hl7 vs txHL7
===================

`python-hl7 <http://python-hl7.readthedocs.org>`_ and txHL7 are
complementary python modules for handling HL7 data.

* txHL7 provides a network-level HL7 implementation (MLLP)
* python-hl7 provides a HL7 parsing implementation

txHL7 and python-hl7 can (and often are) used together.  But, the modular
approach allows a developer to substitute out either component.  For example,
a developer may not wish to use Twisted, instead he may elect to implement
the TCP server using :py:mod:`socket` or :py:mod:`asyncore`.  Likewise, a developer
may wish to use an alternate HL7 parsing routine, but still use txHL7.

As of the :ref:`0.2.0 release <release-0.2.0>`, there is a streamlined way
to use python-hl7 as the parser for txHL7, via the
:py:class:`txHL7.receiver.AbstractHL7Receiver`.

txHL7 vs twisted-hl7
====================

twisted-hl7 is the previous project name for txHL7.  The "tx" prefix
better follows twisted's `Community Code
<http://twistedmatrix.com/trac/wiki/CommunityCode>`_ recommendations.

txHL7 is not an official twisted project.

.. note::

   Please update setup dependencies and imports to txHL7.
   See :ref:`release-0.3.0`

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

