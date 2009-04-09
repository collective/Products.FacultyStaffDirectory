from zope.publisher.interfaces.browser import IBrowserView
from zope.viewlet.interfaces import IViewletManager
from zope.interface import Attribute


class IPersonViewletManager(IViewletManager):
    """A person viewlet manager for every block"""

class IPersonView(IBrowserView):
    """A view for a person object"""

class IPersonOfficeAddressViewletManager(IViewletManager):
    """ Stores parts of a person's office address """

class IPersonGroupingViewletManager(IViewletManager):
    """A person grouping viewlet manager"""

class IPersonGroupingView(IBrowserView):
    """A view for a grouping of person objects"""

class IPersonGroupingContainerViewletManager(IViewletManager):
    """A viewlet manager containing the parts of a person grouping's view (page content, person listing, nested person groupings)."""
    
class IClassificationViewletManager(IViewletManager):
    """Ordered viewlet manager that contains and orders parts of a classification like description and person listing."""
    
class ICommitteeViewletManager(IViewletManager):
    """Ordered viewlet manager that contains and orders parts of a committee like body text and committee members"""
        
class IListingFormat(IBrowserView):
    """ Determines how a listing should be formatted"""
    
class ITabularListingFormat(IListingFormat):
    """View that provides a tabular listing"""
    
class IGalleryListingFormat(IListingFormat):
    """View that provides a gallery listing"""
