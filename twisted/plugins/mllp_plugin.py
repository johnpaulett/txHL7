from zope.interface import implements
from zope.interface.verify import verifyClass

from twisted.python import usage, reflect
from twisted.plugin import IPlugin
from twisted.internet import endpoints
from twisted.application.service import IServiceMaker
from twisted.application import internet

DEFAULT_ENDPOINT = "tcp:2575"
DEFAULT_RECEIVER = "twistedhl7.mllp.LoggingReceiver"


class Options(usage.Options):
    """Define the options accepted by the ``twistd mllp`` plugin"""
    synopsis = "[mllp options]"

    optParameters = [
        ['endpoint', 'e', DEFAULT_ENDPOINT, 'The string endpoint on which to listen.'],
        ['receiver', 'r', DEFAULT_RECEIVER, 'A twistedhl7.mllp.IHL7Receiver subclass to handle messages.'],
    ]

    longdesc = """\
Starts an MLLP server. If no arguments are specified,
it will be a demo server that logs and ACKs each message received."""


class MLLPServiceMaker(object):
    """Service maker for the MLLP server."""
    implements(IServiceMaker, IPlugin)
    tapname = "mllp"
    description = "HL7 MLLP server."
    options = Options

    def makeService(self, options):
        """Construct a server using MLLPFactory."""
        from twisted.internet import reactor
        from twistedhl7.mllp import IHL7Receiver, MLLPFactory

        receiver_name = options['receiver']
        receiver_class = reflect.namedClass(receiver_name)
        verifyClass(IHL7Receiver, receiver_class)
        factory = MLLPFactory(receiver_class())
        endpoint = endpoints.serverFromString(reactor, options['endpoint'])
        server = internet.StreamServerEndpointService(endpoint, factory)
        server.setName(u"mllp-{0}".format(receiver_name))
        return server

serviceMaker = MLLPServiceMaker()
