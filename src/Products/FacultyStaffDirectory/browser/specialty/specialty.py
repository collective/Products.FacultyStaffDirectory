from Products.Five import BrowserView
from plone.app.layout.viewlets.common import ViewletBase

class SpecialtyView(BrowserView):
    pass
    
class GalleryView(SpecialtyView):
    pass

class TabularView(SpecialtyView):
    pass
    
class SubspecialtiesViewlet(ViewletBase):
    def getSubspecialties(self):
        return self.context.getFolderContents({'portal_type':'FSDSpecialty', 'sort_on':'sortable_title'})  # TODO: Use getSpecialtyTree
