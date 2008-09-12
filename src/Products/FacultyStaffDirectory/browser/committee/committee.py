from Products.Five import BrowserView
from plone.app.layout.viewlets.common import ViewletBase

class CommitteeView(BrowserView):
    pass
    
class GalleryView(CommitteeView):
    pass

class TabularView(CommitteeView):
    pass