from Acquisition import aq_parent, aq_inner
from zope import schema
from zope.component import getMultiAdapter, ComponentLookupError
from zope.formlib import form
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from plone.app.relations.interfaces import IRelationshipTarget

from Acquisition import aq_inner
from DateTime.DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.FacultyStaffDirectory.interfaces import IPersonGrouping, IFacultyStaffDirectory

class IFSDSearchPortlet(IPortletDataProvider):
    """ A portlet displaying a (live) search box
    """

class Assignment(base.Assignment):
    implements(IFSDSearchPortlet)

    def __init__(self, enableLivesearch=True):
        self.enableLivesearch=enableLivesearch

    @property
    def title(self):
        return _(u"Search")


class Renderer(base.Renderer):

    render = ViewPageTemplateFile('fsd_search_portlet.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        
        portal_state = getMultiAdapter((context, request), name=u'plone_portal_state')
        plone_context_state = getMultiAdapter((context, request), name=u'plone_context_state')
        
        self.portal_url = portal_state.portal_url()
        self.current_url = plone_context_state.canonical_object_url()


    def _get_directory(self):
        """ return the FacultyStaffDirectory that contains this grouping
            
            if this grouping _is_ a FacultyStaffDirectory, return it
        """
        obj = self.context
        while not IFacultyStaffDirectory.providedBy(obj):
            obj = aq_parent(aq_inner(obj))
            
        return obj


    def _clean_search_text(self, s):
        """ given an incoming search string from the form input, return a cleaned
            string suitable for portal_catalog  full text searching

            modelled on the algorithm in livesearch_reply.py
        """
        def quotestring(string):
            return '"%s"' % string

        def quote_bad_chars(string):
            bad_chars = ["(", ")"]
            for char in bad_chars:
                string = string.replace(char, quotestring(char))
            return string

        for char in '?-+*':
            s = s.replace(char, ' ')
        cleaned = s.split()
        cleaned = " AND ".join(cleaned)
        cleaned = quote_bad_chars(cleaned)+'*'
        
        return cleaned


    def _perform_search(self):
        """ actually do the search
        """
        cleantext = ""
        all_people = []
        
        try:
            ptools = getMultiAdapter((self.context, self.request), name=u'plone_tools')
        except ComponentLookupError:
            # if for some reason we can't find the portal tools, re-raise so we can 
            # handle it at the next level
            raise
        else:
            cleantext += self._clean_search_text(self.request.get('SearchableText'))
            pc = ptools.catalog()
            search_path = '/'.join(self._get_directory().getPhysicalPath())
            all_people = pc(path=search_path,
                            portal_type="FSDPerson",
                            SearchableText=cleantext)
        
        if self.request.get('here_only'):
            # Darn, This doesn't work since brains returned by different searches are
            #   different, event if they represent the same object.  Too bad, using sets
            #   is an elegant solution :(
            # related_set = set(self.context.getPeopleAsBrains())
            # full_set = set(all_people)
            # return list(full_set & related_set)
            related_people = self.context.getPeopleAsBrains()
            # can we make any assumptions about the relative length of all_people and
            # related_people that would help to optimize this?
            ids = [b.id for b in all_people]
            return [b for b in related_people if b.id in ids]
        else:
            # the people we already have have been found in this FSD, so just 
            # return them directly
            return all_people


    def search_action(self):
        return self.current_url


    def current_location_title(self):
        return self.context.Title()


    def _data(self):
        """ return a dictionary representing search results
            dictionary in the form {'error': message <string>,
                                    'results': [{'title': Title <string>,
                                                 'url': URL <string>}]
                                   }
            
            results may be an empty list.  
            error may be None
        """
        output = {'error': None,
                  'results': []}
        
        if 'SearchableText' in self.request.form.keys():
            # we need to do a search, do it
            try:
                brains = self._perform_search()
            except ComponentLookupError:
                output['error'] = 'unable to perform search'
            except:
                output['error'] = 'unknown error in search'
            else:
                if len(brains) == 0:
                    # no results, report that to the user
                    output['results'].append({'title': 'No matches found',
                                              'url': None})
                else:
                    # there were results.  return them
                    for brain in brains:
                        b_dict = {'title': brain.Title,
                                  'url': brain.getURL()}
                        output['results'].append(b_dict)
        
        return output


class AddForm(base.NullAddForm):
    form_fields = form.Fields(IFSDSearchPortlet)
    label = _(u"Add Search Portlet")
    description = _(u"This portlet shows a search box for the current Faculty/Staff Directory.")

    def create(self):
        return Assignment()

