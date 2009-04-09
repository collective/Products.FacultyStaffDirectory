# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner, aq_parent
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from Products.Relations.field import RelationField
from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.interfaces import IConfiguration
from Products.FacultyStaffDirectory.interfaces.persongrouping import IPersonGrouping
from Products.FacultyStaffDirectory.permissions import MANAGE_GROUP_MEMBERSHIP
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.interface import implements

schema =  ATContentTypeSchema.copy() + Schema((

    TextField(
        name='text',
        allowable_content_types=ALLOWABLE_CONTENT_TYPES,
        widget=RichWidget(
            label=u"Body Text",
            label_msgid='FacultyStaffDirectory_label_text',
            i18n_domain='FacultyStaffDirectory',
        ),
        default_output_type="text/x-html-safe",
        searchable=True,
        validators=('isTidyHtmlWithCleanup',)
    ),

    ImageField(
        name='image',
        widget=ImageWidget(
            label=u"An image or logo that will be used as a graphical representation of this group",
            label_msgid='FacultyStaffDirectory_label_overview_image',
            i18n_domain='FacultyStaffDirectory',
            default_content_type='image/gif',
        ),
        storage=AttributeStorage(),
        original_size=(200, 200),
        sizes={'normal': (200, 250)},
        default_output_type='image/jpeg',
        allowable_content_types=('image/gif','image/jpeg','image/png'),
    ),

    RelationField(
        name='people',
        widget=ReferenceBrowserWidget(
            label=u'Members',
            label_msgid='FacultyStaffDirectory_label_members',
            i18n_domain='FacultyStaffDirectory',
            base_query={'portal_type':'FSDPerson', 'sort_on':'getSortableName'},
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1,
        ),
        write_permission = MANAGE_GROUP_MEMBERSHIP,
        allowed_types=('FSDPerson',),
        multiValued=True,
        relationship='departments_members'
    ),

),
)

PersonGrouping_schema = OrderedBaseFolderSchema.copy() + schema.copy()  # + on Schemas does only a shallow copy

class PersonGrouping(OrderedBaseFolder, ATCTContent):
    """This is my docstring"""
    security = ClassSecurityInfo()
    __implements__ = (ATCTContent.__implements__,
                      getattr(OrderedBaseFolder,'__implements__', ()),                      
                     )
    implements(IPersonGrouping)

    meta_type = portal_type = 'FSDPersonGrouping'

    # moved schema setting after finalizeATCTSchema, so the order of the fieldsets
    # is preserved. Also after updateActions is called since it seems to overwrite the schema changes.
    # Move the description field, but not in Plone 2.5 since it's already in the metadata tab. Although, 
    # decription and relateditems are occasionally showing up in the "default" schemata. Move them
    # to "metadata" just to be safe.
    if 'categorization' not in PersonGrouping_schema.getSchemataNames():
        PersonGrouping_schema.changeSchemataForField('relatedItems', 'metadata')
        
    _at_rename_after_creation = True
    schema = PersonGrouping_schema
    
    relationship = None
    
    security.declareProtected(View, 'getPeople')
    def getPeople(self):
        """ Return a list of the catalog brains of people related to this grouping only
        """
        
        return self.getRefs(self.relationship)
    
    def getDeepPeople(self):
        """ Return a flat list of the catalog brains of people related to this grouping 
            and all groupings nested inside this one, recursively
            
            At this point, the list is in no way asserted to be unique.  Should we 
            be deleting duplicates?
        """
        people = []
        pc = getToolByName(self, 'portal_catalog')
        fsd_util = getUtility(IConfiguration)
        groupings = pc(path=self.absolute_url_path(), portal_type=list(fsd_util.enableMembraneTypes))
        for group in groupings:
            people.extend(group.getObject().getRefs(self.relationship))
        
        return people
        
    def getSortedPeople(self):
        """Return a list of people, sorted by SortableName."""
        people = list(self.getPeople())
        people.sort(key=lambda x: x.getSortableName)
        
        return people

    #
    # Validators
    #
    security.declarePrivate('validate_id')
    def validate_id(self, value):
        """Ensure the id is unique, also among groups globally
        """
        if value != self.getId():
            parent = aq_parent(aq_inner(self))
            if value in parent.objectIds():
                return "An object with id '%s' already exists in this folder" % value
        
            groups = getToolByName(self, 'portal_groups')
            if groups.getGroupById(value) is not None:
                return "A group with id '%s' already exists in the portal" % value
        

registerType(PersonGrouping, PROJECTNAME)
