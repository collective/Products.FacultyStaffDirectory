from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class SpecialtyView(BrowserView):
    @property
    def subSpecialties(self):
        return self.context.getFolderContents({'portal_type':'FSDSpecialty', 'sort_on':'sortable_title'})
    
class GalleryView(SpecialtyView):
    pass

class TabularView(SpecialtyView):
    pass