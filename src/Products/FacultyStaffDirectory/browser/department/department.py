from Products.FacultyStaffDirectory.interfaces import IPersonGroupingView
from Products.Five import BrowserView
from plone.app.layout.viewlets.common import ViewletBase
from zope.interface import implements

class DepartmentView(BrowserView):
    pass
    
class GalleryView(DepartmentView):
    pass

class TabularView(DepartmentView):
    pass    
    
class DepartmentGalleryPeople(ViewletBase):
    implements(IPersonGroupingView)
    viewletForPerson = u"facultystaffdirectory.persongallery"

class DepartmentTabularPeople(ViewletBase):
    implements(IPersonGroupingView)
    viewletForPerson = u"facultystaffdirectory.persontabular"