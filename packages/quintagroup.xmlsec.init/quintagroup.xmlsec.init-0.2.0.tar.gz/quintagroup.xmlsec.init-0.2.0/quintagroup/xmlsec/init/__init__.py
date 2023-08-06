"""Initialize xmlsec bindings."""

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('quintagroup.xmlsec.init')

def initialize(context):
    """Initializer called when used as a Zope 2 product."""

from dm.xmlsec.binding import initialize; initialize()
