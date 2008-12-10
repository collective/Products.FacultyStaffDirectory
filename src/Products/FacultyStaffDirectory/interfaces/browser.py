from zope.publisher.interfaces.browser import IBrowserView
from zope.viewlet.interfaces import IViewletManager
from zope.interface import Attribute


class IPersonViewletManager(IViewletManager):
    """A person viewlet manager for every block"""

class IPersonView(IBrowserView):
    """A view for a person object"""

class IPersonGroupingViewletManager(IViewletManager):
    """A person grouping viewlet manager"""

class IPersonGroupingView(IBrowserView):
    """A view for a grouping of person objects"""

    viewletForPerson = Attribute("Viewlet to be used for rendering person objects within this view") 

class IPersonGroupingContainerViewletManager(IViewletManager):
    """A viewlet manager containing the parts of a person grouping's view (page content, person listing, nested person groupings)."""

class ISpecialtyViewletManager(IViewletManager):
    """Ordered viewlet manager that contains and orders parts of a specialty like body text, subspecialties, etc."""
    pass
    
class IClassificationViewletManager(IViewletManager):
    """Ordered viewlet manager that contains and orders parts of a classification like description and person listing."""
    
class ICommitteeViewletManager(IViewletManager):
    """Ordered viewlet manager that contains and orders parts of a committee like body text and committee members"""
        
class IDepartmentViewletManager(IViewletManager):
    """Ordered viewlet manager that contains and orders parts of a committee like body text and committee members"""
    
class ITabularListing(IBrowserView):
    """View that provides a tabular listing"""
    
class IGalleryListing(IBrowserView):
    """View that provides a gallery listing"""
