# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner, aq_parent
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.interfaces import IConfiguration
from Products.FacultyStaffDirectory.interfaces import IPersonGrouping
from Products.FacultyStaffDirectory.interfaces import IPersonToPersonGroupingRelationship
from Products.FacultyStaffDirectory.permissions import MANAGE_GROUP_MEMBERSHIP
from Products.CMFCore.permissions import View, ModifyPortalContent
from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IPropertiesProvider
from zope.component import getUtility
from zope.interface import implements

from plonerelations.ATField.ploneRelationsATField import ReversePloneRelationsATField
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

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

    ReversePloneRelationsATField(
        name='people',
        widget=ReferenceBrowserWidget(
            label=u'Members',
            label_msgid='FacultyStaffDirectory_label_members',
            i18n_domain='FacultyStaffDirectory',
            base_query={'portal_type':'FSDPerson', 'sort_on':'sortable_title'},
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1,
        ),
        write_permission = MANAGE_GROUP_MEMBERSHIP,
        allowed_types=('FSDPerson',),
        multiValued=True,
        relationship='PersonGroupingAssociation', 
        relationship_interface=IPersonToPersonGroupingRelationship,        
    ),

),
)

PersonGrouping_schema = OrderedBaseFolderSchema.copy() + schema.copy()  # + on Schemas does only a shallow copy

class PersonGrouping(OrderedBaseFolder, ATCTContent):
    """ This is my docstring"""
    security = ClassSecurityInfo()
    __implements__ = (ATCTContent.__implements__,
                      getattr(OrderedBaseFolder,'__implements__', ()),                      
                     )
    implements(IPersonGrouping, IPropertiesProvider)

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
    
    relationship = schema['people'].relationship
    
    def getPeopleAsBrains(self):
        """ Return a list of catalog brains representing the Persons associated with this object. """
        pc = getToolByName(self, 'portal_catalog')
        brains = []
        for uid in self.getRawPeople():
            result = pc(UID=uid)
            if result:
                brains.append(result[0])
        return brains
        
    def getDeepPeople(self):
        """Return a flat list of the catalog brains of people related to this grouping 
            and all groupings nested inside this one, recursively
            
            At this point, the list is in no way asserted to be unique.  Should we 
            be deleting duplicates?
        
        """
        people = []
        pc = getToolByName(self, 'portal_catalog')
        fsd_util = getUtility(IConfiguration)
        groupings = pc(path=self.absolute_url_path(), portal_type=list(fsd_util.enableMembraneTypes))
        for group in groupings:
            people.extend(group.getObject().getPeople())
        
        return people
        
    security.declareProtected(View, 'getSortedPeople')
    def getSortedPeople(self):
        """Return a list of people, sorted by sortableName."""
        people = list(self.getPeople())
        people.sort(key=lambda p: p.getSortableName())
        return people

    #
    # Validators
    #
    security.declarePrivate('validate_id')
    def validate_id(self, value):
        """Ensure the id is unique, also among groups globally"""
        if value != self.getId():
            parent = aq_parent(aq_inner(self))
            if value in parent.objectIds():
                return "An object with id '%s' already exists in this folder" % value
        
            groups = getToolByName(self, 'portal_groups')
            if groups.getGroupById(value) is not None:
                return "A group with id '%s' already exists in the portal" % value
        

registerType(PersonGrouping, PROJECTNAME)
