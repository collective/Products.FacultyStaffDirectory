from zope.interface import implements
from zope.component import adapts

from Products.CMFCore.utils import getToolByName

from Products.membrane.interfaces import IGroup
from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.interfaces import ICategoryMapper

from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.config import TOOLNAME as MEMBRANE_TOOL
from Products.membrane.utils import generateCategorySetIdForType

from Products.FacultyStaffDirectory.interfaces.department import IDepartment
from Products.FacultyStaffDirectory.interfaces.person import IPerson
from Products.FacultyStaffDirectory.membership.person import UserRelated

class Group(object):
    """Allow a Department to act as a group for contained people
    """
    implements(IGroup)
    adapts(IDepartment)
    
    def __init__(self, context):
        self.context = context
        
    def Title(self):
        return self.context.Title()
    
    def getRoles(self):
        """We don't actually want a department to provide any global roles to it's members,
        so let's just return an empty list for this
        """
        return ()
    
    def getGroupId(self):
        return self.context.getId()

    def getGroupMembers(self):
        members = self.context.getMembers()
        mlist = [UserRelated(m).getUserId() for m in members]
        return tuple(mlist)