from zope.publisher.interfaces.browser import IBrowserView
from zope.viewlet.interfaces import IViewletManager
from zope.interface import Attribute

class IPersonGroupingViewletManager(IViewletManager):
    """A person grouping viewlet manager"""

class IPersonGroupingView(IBrowserView):
    """A view for a grouping of person objects"""

    viewletForPerson = Attribute("Viewlet to be used for rendering person objects within this view") 

class ISpecialtyViewletManager(IViewletManager):
    """Ordered viewlet manager that contains and orders parts of a specialty like body text, subspecialties, etc."""
    pass

class ISpecialtyTabularViewletManager(ISpecialtyViewletManager):
    """Ordered viewlet manager that contains and orders parts of a specialty like body text, subspecialties, etc. with tabular display of people"""
    pass

class ISpecialtyGalleryViewletManager(ISpecialtyViewletManager):
    """Ordered viewlet manager that contains and orders parts of a specialty like body text, subspecialties, etc. with gallery display of people"""
    pass

class IClassificationViewletManager(IViewletManager):
    """Ordered viewlet manager that contains and orders parts of a classification like description and person listing."""
