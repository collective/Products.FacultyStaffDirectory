from zope.interface import implements
from zope.component import adapts

from Products.membrane.interfaces import IGroup
from Products.FacultyStaffDirectory.interfaces.persongrouping import IPersonGrouping
from Products.FacultyStaffDirectory.membership.person import UserRelated

class Group(object):
    """Allow an FSDPersonGrouping to act as a group for related people
    """
    implements(IGroup)
    adapts(IPersonGrouping)
    
    def __init__(self, context):
        self.context = context
        
    def Title(self):
        return self.context.Title()
    
    def getRoles(self):
        """ We don't actually want person groupings to provide any global roles,
            so let's just return an empty list for this
        """
        return ()
    
    def getGroupId(self):
        return self.context.getId()

    def getGroupMembers(self):
        members = self.context.getDeepPeople()
        mlist = [UserRelated(m).getUserId() for m in members]
        return tuple(mlist)