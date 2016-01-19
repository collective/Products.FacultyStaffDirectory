# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.FacultyStaffDirectory import config

from Products.FacultyStaffDirectory.interfaces.specialtyinformation import ISpecialtyInformation
from zope.interface import implements
from Products.FacultyStaffDirectory import FSDMessageFactory as _

try:
    from Products.Archetypes.Widget import TinyMCEWidget
except ImportError:
    TinyMCEWidget = atapi.RichWidget

schema = atapi.Schema((

    atapi.TextField(
        name='researchTopic',
        allowable_content_types=('text/plain', 'text/structured', 'text/html',),
        widget=TinyMCEWidget(
            label=_(u"FacultyStaffDirectory_label_researchTopic", default=u"Research Topic"),
            i18n_domain='FacultyStaffDirectory',
            allow_file_upload=False,
            rows=5,
        ),
        default_output_type='text/x-html-safe'
    ),

    atapi.StringField(
        name='title',
        default="Research Topic",
        widget=atapi.StringWidget(
            visible={'edit': 'invisible', 'view': 'visible'},
            label=_(u"FacultyStaffDirectory_label_title", default=u"Title"),
            i18n_domain='FacultyStaffDirectory',
        ),
        accessor="Title"
    ),

),
)

SpecialtyInformation_schema = atapi.BaseSchema.copy() + schema.copy()


class SpecialtyInformation(atapi.BaseContent):
    """
    """
    security = ClassSecurityInfo()
    implements(ISpecialtyInformation)
    meta_type = portal_type = 'FSDSpecialtyInformation'
    schema = SpecialtyInformation_schema

atapi.registerType(SpecialtyInformation, config.PROJECTNAME)
