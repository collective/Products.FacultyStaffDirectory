from zope.publisher.interfaces.browser import IBrowserView
from zope.viewlet.interfaces import IViewletManager, IViewlet
from zope.interface import Attribute



class IPersonViewletManager(IViewletManager):
    """A person viewlet manager for every block"""
    def columns():
        """Return a list of dictionaries necessary to render table header cells"""

class IPersonView(IBrowserView):
    """A view for a person object"""

class IPersonOfficeAddressViewletManager(IViewletManager):
    """Stores parts of a person's office address"""

class IPersonGroupingViewletManager(IViewletManager):
    """A person grouping viewlet manager"""

class IPersonGroupingItemViewlet(IViewlet):
    """A viewlet containing the parts of a person, displayed within a person grouping"""

class IPersonGroupingView(IBrowserView):
    """A view for a grouping of person objects"""

class IPersonGroupingContainerViewletManager(IViewletManager):
    """A viewlet manager containing the parts of a person grouping's view (page content, person listing, nested person groupings)."""
    
class IPersonGroupingContainerTabularViewletManager(IViewletManager):
    """A viewlet manager containing the parts of a person grouping's view (page content, person listing, nested person groupings)."""
    
class IListingFormat(IBrowserView):
    """Determines how a listing should be formatted"""
    
class ITabularListingFormat(IListingFormat):
    """View that provides a tabular listing"""
    
class IGalleryListingFormat(IListingFormat):
    """View that provides a gallery listing"""
