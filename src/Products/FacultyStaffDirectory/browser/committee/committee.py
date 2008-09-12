from Products.FacultyStaffDirectory.interfaces import IPersonGroupingView
from Products.Five import BrowserView
from plone.app.layout.viewlets.common import ViewletBase
from zope.interface import implements

class CommitteeView(BrowserView):
    pass
    
class GalleryView(CommitteeView):
    pass

class TabularView(CommitteeView):
    pass    
    
class CommitteeGalleryPeople(ViewletBase):
    implements(IPersonGroupingView)
    viewletForPerson = u"facultystaffdirectory.persongallery"

class CommitteeTabularPeople(ViewletBase):
    implements(IPersonGroupingView)
    viewletForPerson = u"facultystaffdirectory.persontabular"