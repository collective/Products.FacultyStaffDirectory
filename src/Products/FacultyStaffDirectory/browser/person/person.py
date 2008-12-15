from Products.Five import BrowserView
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getSiteManager
from Products.FacultyStaffDirectory.interfaces import IPersonViewletManager

class PersonView(BrowserView):
    
    @property
    def portrait(self):
        """Return None if no image. 
        
        (tag() field will return an img tag regardless)
        
        """
        return self.context.getImage() and self.context.getWrappedField('image').tag(self.context, scale='normal')
    
    @property
    def officeAddress(self):
        return self.context.getOfficeAddress().replace('\n', '<br />')
        
    @property
    def email(self):
        return self.context.spamProtectFSD(self.context.getEmail())
    

class PersonGalleryViewlet(ViewletBase, PersonView):
    @property
    def portrait(self):
        """Return None if no image. 
        
        (tag() field will return an img tag regardless)
        
        """
        width = self.context.getClassificationViewThumbnailWidth()
        return self.context.getImage() and self.context.getScaledImageByWidth(width)

class PersonMultiView(PersonView):
    def __init__(self, person, grouping, format, request): # Override __init__ so we have 4 params instead of the usual 3 (since this is called using a multi-view lookup)
        super(PersonMultiView, self).__init__(person, request)
        self.context = person
        self.grouping = grouping
        self.format = format
        self.request = request
    
    def __call__(self):
        # TODO Catch multiple managers in case two managers of the same specificity exist..
        # Look up the viewletmanager most specific to this context.
        # We're assuming that getAdapters returns the most specific last. Should this change...yikes!
        name, manager = list(getSiteManager().getAdapters((self.grouping, self.request, self.format), IPersonViewletManager))[-1]
        # Render the manager
        manager.update()
        self.renderedManager = manager.render()
        return self.template()

class PersonGalleryView(PersonMultiView):
    template = ViewPageTemplateFile('gallery/gallery.pt')

class PersonTabularView(PersonMultiView):
    template = ViewPageTemplateFile('tabular/tabular.pt')
