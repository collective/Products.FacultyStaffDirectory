from zope.interface import implements
from zope.component import adapts, getUtility
from zope.publisher.interfaces.http import IHTTPRequest
from zope.traversing.interfaces import ITraversable, TraversalError
from Products.FacultyStaffDirectory.interfaces import IConfiguration, ISiteMarker

class MembershipTraverser(object):
    """The namespace traverser for ++fsdmembership++, which gives access to membrane-integration settings."""
    
    implements(ITraversable)
    adapts(ISiteMarker, IHTTPRequest)
    
    def __init__(self, context, request=None):
        self.context = context
        self.request = request        
        
    def traverse(self, name, furtherPath):
        """For the moment, just always return the monolithic configuration utility."""
        return getUtility(IConfiguration)
        #raise TraversalError(self.context, name)
