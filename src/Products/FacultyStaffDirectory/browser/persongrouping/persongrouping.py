from AccessControl.ZopeGuards import guarded_hasattr
from Products.Five import BrowserView
from zope.component import getMultiAdapter, ComponentLookupError
from zope.interface import implements
from zope.viewlet.interfaces import IViewlet, IViewletManager
from Products.FacultyStaffDirectory.interfaces import IPersonGroupingViewletManager, IPersonGroupingView

class PersonListView(BrowserView):
    implements(IPersonGroupingView)

    viewletOfChoice = u'facultystaffdirectory.personlistitem'


class PersonGroupingViewletManager(object):
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
                    self.__parent__.viewletForPerson)

            # wrap the viewlet for security purposes
            viewlet = viewlet.__of__(viewlet.context)

            # update the viewlet
            viewlet.update()

            # check security
            if guarded_hasattr(viewlet, 'render'):
                # then add it 
                self.viewlets.append(viewlet)

    def render(self):
        """See zope.contentprovider.interfaces.IContentProvider"""
        # Now render the view
        if self.template:
            return self.template(viewlets=self.viewlets)
        else:
            return u'\n'.join([viewlet.render() for viewlet in self.viewlets])

