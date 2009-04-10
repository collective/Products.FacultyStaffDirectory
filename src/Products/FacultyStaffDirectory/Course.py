# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.FacultyStaffDirectory.config import *
from Products.CMFCore.permissions import View
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema, finalizeATCTSchema
from Products.FacultyStaffDirectory.interfaces import ICourse
from zope.interface import implements

schema = ATContentTypeSchema.copy() + Schema((

    StringField(
        name='abbreviation',
        widget=StringWidget(
            size="5",
            label=u'Abbreviation',
            label_msgid='FacultyStaffDirectory_label_abbreviation',
            i18n_domain='FacultyStaffDirectory',
        ),
        searchable=True
    ),

    StringField(
        name='number',
        widget=StringWidget(
            label=u'Number',
            label_msgid='FacultyStaffDirectory_label_number',
            i18n_domain='FacultyStaffDirectory',
        ),
        searchable=True
    ),

    TextField(
        name='description',
        allowable_content_types=ALLOWABLE_CONTENT_TYPES,
        widget=RichWidget(
            label=u'Description',
            label_msgid='FacultyStaffDirectory_label_description',
            i18n_domain='FacultyStaffDirectory',
        ),
        searchable=True,
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/html',
        accessor="Description"
    ),

    StringField(
        name='suffix',
        widget=StringWidget(
            size="1",
            label=u'Suffix',
            label_msgid='FacultyStaffDirectory_label_suffix',
            i18n_domain='FacultyStaffDirectory',
        )
    ),

    StringField(
        name='website',
        widget=StringWidget(
            label=u"Course Website",
            description="Example: http://www.example.com/",
            label_msgid='FacultyStaffDirectory_label_website',
            description_msgid='FacultyStaffDirectory_help_website',
            i18n_domain='FacultyStaffDirectory',
        ),
        validators=('isURL',)
    ),

),
)

Course_schema = BaseSchema.copy() + schema.copy()  # + on Schemas does only a shallow copy
finalizeATCTSchema(Course_schema)

class Course(BaseContent, ATCTContent):
    """A course of study, like Anthropology 101"""
    security = ClassSecurityInfo()
    __implements__ = (BaseContent.__implements__ + ATCTContent.__implements__)
    implements(ICourse)
    meta_type = portal_type = 'FSDCourse'

    # moved schema setting after finalizeATCTSchema, so the order of the fieldsets
    # is preserved. Also after updateActions is called since it seems to overwrite the schema changes.
    # Move the description field, but not in Plone 2.5 since it's already in the metadata tab. Although, 
    # decription and relateditems are occasionally showing up in the "default" schemata. Move them
    # to "metadata" just to be safe.
    if 'categorization' in Course_schema.getSchemataNames():
        Course_schema.changeSchemataForField('description', 'categorization')
    else:
        Course_schema.changeSchemataForField('description', 'metadata')
        Course_schema.changeSchemataForField('relatedItems', 'metadata')

    _at_rename_after_creation = True
    schema = Course_schema    
    # Methods
    security.declareProtected(View, 'getRemoteUrl')
    def getRemoteUrl(self):
        return self.website

registerType(Course, PROJECTNAME)
# end of class Course

