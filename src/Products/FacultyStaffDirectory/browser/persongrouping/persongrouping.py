from AccessControl.ZopeGuards import guarded_hasattr
from plone.app.layout.viewlets.common import ViewletBase
from Products.FacultyStaffDirectory.interfaces import IPersonGroupingViewletManager, IPersonGroupingView, IListingFormat, ITabularListingFormat, IGalleryListingFormat
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Five.viewlet.manager import ViewletManagerBase
from zope.component import getMultiAdapter, ComponentLookupError, queryMultiAdapter
from zope.interface import implements
from zope.viewlet.interfaces import IViewlet, IViewletManager

class GalleryView(object):
    implements(IGalleryListingFormat)

class TabularView(object):
    implements(ITabularListingFormat)

class GroupingsOnlyView(object):
    implements(ITabularListingFormat)

class ViewletManager(ViewletManagerBase):
    implements(IPersonGroupingViewletManager)

    viewlets = []

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.__parent__ = view
        self.__updated = False

    def __getitem__(self, name):
        """See zope.interface.common.mapping.IReadMapping"""

        # Find the viewlet
        if name in self.viewlets:
            return self.viewlets[name]
        else:
            raise ComponentLookupError(
                'No provider with name `%s` found.' %name)

    def get(self, name, default=None):
        """See zope.interface.common.mapping.IReadMapping"""
        try:
            return self[name]
        except (ComponentLookupError):
            return default

    def update(self):
        """See zope.contentprovider.interfaces.IContentProvider"""
        self.__updated = True
        self.viewlets = []

        # make a list of the viewlets
        people = self.context.getSortedPeople()
        for person in people:
            # adapt a person into our viewlet of choice
            viewlet = getMultiAdapter(
                    (person, self.request, self.__parent__, self),
                    IViewlet,
                    'facultystaffdirectory.persongroupingitemviewlet')
            # wrap the viewlet for security purposes
            viewlet = viewlet.__of__(viewlet.context)

            # update the viewlet
            viewlet.update()

            # check security
            if guarded_hasattr(viewlet, 'render'):
                # then add it 
                self.viewlets.append(viewlet)

        # grab the column headers from the first viewlet
        if self.viewlets:
            self.columns = self.viewlets[0].columns()
        else:
            self.columns = []

    def render(self):
        """See zope.contentprovider.interfaces.IContentProvider"""
        # Now render the view
        if self.template:
            return self.template(viewlets=self.viewlets)
        else:
            return u'\n'.join([viewlet.render() for viewlet in self.viewlets])

class ItemViewlet(ViewletBase):

    def parentMultiView(self):
        """Look up the person's multiview (typically a tabular or gallery view)"""
        person = self.context
        # TODO self.__parent__.__parent__.__parent__ and self.__parent__.__parent__ completely wrong. Do it right.
        grouping = self.__parent__.__parent__.__parent__
        format = self.__parent__.__parent__
        view =  queryMultiAdapter((person, grouping, format, self.request), name='view')
        # wrap the view for security purposes
        view = view.__of__(person)

        self.person = person
        self.grouping = grouping
        self.format = format

        return view
        
    def index(self):
        return self.parentMultiView()()

    def columns(self):
        return self.parentMultiView().columns()

    def associationContent(self):
        """ Return the content objects attached to the association between the Person and the PersonGrouping. """
        return self.person.getGroupingAssociationContent(target=self.grouping)

        
        
