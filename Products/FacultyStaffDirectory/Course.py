# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.FacultyStaffDirectory import config
from Products.CMFCore.permissions import View
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema, finalizeATCTSchema
from Products.FacultyStaffDirectory.interfaces.course import ICourse
from zope.interface import implements
from Products.FacultyStaffDirectory import FSDMessageFactory as _

try:
    from Products.Archetypes.Widget import TinyMCEWidget
except ImportError:
    TinyMCEWidget = atapi.RichWidget


schema = ATContentTypeSchema.copy() + atapi.Schema((

    atapi.StringField(
        name='abbreviation',
        widget=atapi.StringWidget(
            size="5",
            label=_(u"FacultyStaffDirectory_label_abbreviation", default=u"Abbreviation"),
            i18n_domain='FacultyStaffDirectory',
        ),
        searchable=True
    ),

    atapi.StringField(
        name='number',
        widget=atapi.StringWidget(
            label=_(u"FacultyStaffDirectory_label_number", default=u"Number"),
            i18n_domain='FacultyStaffDirectory',
        ),
        searchable=True
    ),

    atapi.TextField(
        name='description',
        allowable_content_types=config.ALLOWABLE_CONTENT_TYPES,
        widget=TinyMCEWidget(
            label=_(u"FacultyStaffDirectory_label_description", default=u"Description"),
            i18n_domain='FacultyStaffDirectory',
        ),
        searchable=True,
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/html',
        accessor="Description"
    ),

    atapi.StringField(
        name='suffix',
        widget=atapi.StringWidget(
            size="1",
            label=_(u"FacultyStaffDirectory_label_suffix", default=u"Suffix"),
            i18n_domain='FacultyStaffDirectory',
        )
    ),

    atapi.StringField(
        name='website',
        widget=atapi.StringWidget(
            label=_(u"FacultyStaffDirectory_label_website", default=u"Course Website"),
            description=_(u"FacultyStaffDirectory_help_website",
                          default=u"Example: http://www.example.com/"),
            i18n_domain='FacultyStaffDirectory',
        ),
        validators=('isURL',)
    ),

),
)

Course_schema = atapi.BaseSchema.copy() + schema.copy()  # + on Schemas does only a shallow copy
finalizeATCTSchema(Course_schema)

class Course(atapi.BaseContent, ATCTContent):
    """
    """
    security = ClassSecurityInfo()
    implements(ICourse)
    meta_type = portal_type = 'FSDCourse'

    # moved schema setting after finalizeATCTSchema, so the order of the fieldsets
    # is preserved. Also after updateActions is called since it seems to overwrite the schema
    # changes.
    # Move the description field, but not in Plone 2.5 since it's already in the metadata tab.
    # Although,
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

atapi.registerType(Course, config.PROJECTNAME)
# end of class Course
