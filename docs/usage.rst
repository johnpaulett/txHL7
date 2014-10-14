Usage
=====

Run simple demo server on default port 2575::

    twistd --nodaemon mllp

Run simple server with a :doc:`custom receiver <custom-receiver>` on port 7575::

    twistd --nodaemon mllp --endpoint tcp:7575 --receiver myreceiver.Receiver

Options help::

    twistd mllp --help


..note::

  Installation of this package may result in a warning which can be ignored::

    package init file 'twisted/plugins/__init__.py' not found (or not a regular file)


Direct Factory & Reactor Usage
------------------------------

twistd & the mllp plugin are not required. You are able to directly start a
twisted reactor or application, instantiating the,
:py:class:`twistedhl7.mllp.MLLPFactory` passing into it an instance of an
:py:class:`twistedhl7.receiver.IHL7Receiver`::

    from twisted.internet import reactor
    from twistedhl7.mllp import MLLPFactory
    from myreceiver import Receiver

    def run(port):
        receiver = Receiver()
        factory = MLLPFactory(receiver)

        reactor = get_reactor()
        reactor.listenTCP(port, factory)
        reactor.run()

    run(6666)
