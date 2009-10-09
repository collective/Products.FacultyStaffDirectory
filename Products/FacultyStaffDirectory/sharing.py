from zope.interface import implements, Interface
from Products.CMFPlone import PloneMessageFactory as _

try:
    from plone.app.workflow.interfaces import ISharingPageRole as interfaceToImplement
except ImportError:
    # Fail nicely, this version of Plone doesn't know anything about @@sharing page roles.
    class IDoNothing(Interface):
        pass
    interfaceToImplement = IDoNothing

class PersonnelManagerRole(object):
    implements(interfaceToImplement)
    title = _(u"title_can_manage_personnel", default=u"Can manage personnel")
    required_permission = 'Manage portal'
