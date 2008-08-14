from zope.interface import implements
from plone.app.workflow.interfaces import ISharingPageRole
from Products.CMFPlone import PloneMessageFactory as _

class PersonnelManagerRole(object):
   implements(ISharingPageRole)
   title = _(u"title_can_manage_personnel", default=u"Can manage personnel")
   required_permission = 'Manage portal content'
