# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.FacultyStaffDirectory.config import *

from Products.FacultyStaffDirectory.interfaces import ISpecialtyInformation
from zope.interface import implements

schema = Schema((

    TextField(
        name='researchTopic',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',),
        widget=RichWidget(
            label=u"Research Topic",
            label_msgid='FacultyStaffDirectory_label_researchTopic',
            i18n_domain='FacultyStaffDirectory',
            allow_file_upload=False,
            rows=5,
        ),
        default_output_type='text/x-html-safe'
    ),

    StringField(
        name='title',
        default="Research Topic",
        widget=StringWidget(
            visible={'edit': 'invisible', 'view': 'visible'},
            label=u'Title',
            label_msgid='FacultyStaffDirectory_label_title',
            i18n_domain='FacultyStaffDirectory',
        ),
        accessor="Title"
    ),

),
)

SpecialtyInformation_schema = BaseSchema.copy() + schema.copy()

class SpecialtyInformation(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)
    implements(ISpecialtyInformation)
    meta_type = portal_type = 'FSDSpecialtyInformation'
    schema = SpecialtyInformation_schema
registerType(SpecialtyInformation, PROJECTNAME)
