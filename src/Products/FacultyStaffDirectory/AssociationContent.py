# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema, finalizeATCTSchema
from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.interfaces import IAssociationContent
from zope.interface import implements

schema = ATContentTypeSchema.copy() + Schema((

    StringField(
        name='title',
        default="Assocation Information",
        widget=StringWidget(
            visible={'edit':'invisible', 'view':'visible'},
            label=u'Title',
            label_msgid='FacultyStaffDirectory_label_assocation_information',
            i18n_domain='FacultyStaffDirectory',
        ),
        accessor="Title"
    ),

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

AssociationContent_schema = BaseSchema.copy() + schema.copy()
finalizeATCTSchema(AssociationContent_schema)

class AssociationContent(BaseContent, ATCTContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)
    implements(IAssociationContent)
    meta_type = portal_type = 'FSDAssociationContent'
    _at_rename_after_creation = True
    schema = AssociationContent_schema

registerType(AssociationContent, PROJECTNAME)

