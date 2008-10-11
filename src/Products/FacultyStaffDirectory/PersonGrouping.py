# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema
from Products.FacultyStaffDirectory.config import *
from Products.CMFCore.permissions import View
from Products.CMFCore.utils import getToolByName

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

),
)

PersonGrouping_schema = OrderedBaseFolderSchema.copy() + schema.copy()  # + on Schemas does only a shallow copy

class PersonGrouping(OrderedBaseFolder, ATCTContent):
    """"""
    security = ClassSecurityInfo()
    __implements__ = (ATCTContent.__implements__,
                      getattr(OrderedBaseFolder,'__implements__', ()),                      
                     )

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

    security.declareProtected(View, 'getClassifications')
    def getClassifications(self):
        """ Ignore the default FacultyStaffDirectory getClassifications so that we can use
            PersonGrouping subclasses outside of a FacultyStaffDirectory object. Making the assumption that there
            will only be one FacultyStaffDirectory and that all Person objects will be created
            inside of it (see the README for some justification for this).
        """
        
        people = self.getPeople()
        if people:
            fsdTool = getToolByName(self, 'facultystaffdirectory_tool')
            return self.getDirectoryRoot().getClassifications()
        else:
            return []

    security.declareProtected(View, 'getSortedPeople')
    def getSortedPeople(self):
        """ Return a list of people, sorted by SortableName
        """
        people = self.getPeople()
        return sorted(people, cmp=lambda x,y: cmp(x.getSortableName(), y.getSortableName()))

registerType(PersonGrouping, PROJECTNAME)

