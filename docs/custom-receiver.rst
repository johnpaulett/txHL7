================
Custom Receivers
================

twisted-hl7 ships with a simple example of a
:py:class:`twisted.receiver.LoggingReceiver`, but for most cases, you will want
to execute some custom actions when a message is received.  To do this, you will
need to define your own receiver, which implements
:py:class:`twistedhl7.receiver.IHL7Receiver`.

:py:class:`twistedhl7.receiver.IHL7Receiver` only requires a few methods to be
implemented (and if you look further down this document, you will find the
even easier ``AbstractHL7Receiver``):

* ``parseMessage`` provides the parsing logic to transform the pipe-delimited
  message into something more useful.  It will return an instance of
  :py:class:`twistedhl7.receiver.MessageContainer`. The ``MessageContainer``
  is important, because it implements how build an HL7 ACK message.
* ``handleMessage`` receives the parsed 
  :py:class:`twistedhl7.receiver.MessageContainer` and is where you should put
  your business logic.  It must return a
  :py:cls:`twisted.internet.defer.Deferred` instance.
* Internally twisted-hl7 treats data as unicode, and ``getCodec`` provides
  the codec to use to decode the bytestring into unicode.


If you wish to use `python-hl7 <http://python-hl7.readthedocs.org>`_ to parse
the message, :py:class:`twistedhl7.receiver.AbstractHl7Receiver` makes your
job even easier.  You just need to implement ``handleMessage`` and optionally
``getCodec``.


Example Receiver
================

A simple example::

    from twistedhl7.receiver import AbstractHL7Receiver
    from twisted.internet import defer

    class ExampleReceiver(AbstractHL7Receiver):
        def handleMessage(self, container):
            message = container.message

            # Our business logic
            mrn = message.segment('PID')[3][0]
            # Do something with mrn

            # We succeeded, so ACK back (default is AA)
            return defer.succeed(container.ack())

        def getCodec(self):
            # Our messages are encoded in Windows-1252
            # WARNING this is an example and is not universally true! You will
            # need to figure out the encoding you are receiving.
            return 'cp1252'


We can launch this receiver with::

    twistd --nodaemon mllp --receiver example.ExampleReceiver



Deferring to a Thread
=====================

Remember that twisted is non-blocking.  Blocking operations should ideally be
executed outside the main loop. One way to accomplish this is to defer to a
thread in twisted [1]_.

.. warning::

   It is up to you to ensure that your application is thread-safe.



Here is an example that calls a blocking operation in ``importMessage``, which
is defered to a thread in ``handleMessage``.  We additionally, show catching
an error are returning a reject message::


    from twistedhl7.receiver import AbstractHL7Receiver
    from twisted.internet import threads

    class ThreadedReceiver(AbstractHL7Receiver):
        def saveMessage(self, message):
            try:
                self.database.insert(message)
                return message.ack()
            except:
                # reject the message
                return message.ack(ack_code='AR')

        def handleMessage(self, message):
             return threads.deferToThread(self.saveMessage, message)


.. [1] https://twistedmatrix.com/documents/current/core/howto/threading.html
