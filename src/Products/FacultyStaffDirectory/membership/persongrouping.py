from zope.interface import implements
from zope.component import adapts

from Products.membrane.interfaces import IGroup
from Products.FacultyStaffDirectory.interfaces import IGroupingProvidingMembership
from Products.FacultyStaffDirectory.membership.person import UserRelated

class Group(object):
    """Allow a Department, Committee, etc. to act as a group for contained people."""
    adapts(IGroupingProvidingMembership)
    implements(IGroup)
    
    def __init__(self, context):
        self.context = context
        
    def Title(self):
        return self.context.Title()
    
    def getRoles(self):
        """We don't actually want a Department to provide any global roles to it's members, so let's just return an empty list for this."""
        return ()
    
    def getGroupId(self):
        return self.context.getId()

    def getGroupMembers(self):
        mlist = [UserRelated(m).getUserId() for m in self.context.getPeople()]
        return tuple(mlist)