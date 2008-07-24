# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.interfaces.departmentalmembership import IDepartmentalMembership
from zope.interface import implements

schema = Schema((

    StringField(
        name='position',
        widget=StringWidget(
            label=u'Position',
            label_msgid='FacultyStaffDirectory_label_position',
            i18n_domain='FacultyStaffDirectory',
        )
    ),

    StringField(
        name='title',
        widget=StringWidget(
            label=u'Title',
            label_msgid='FacultyStaffDirectory_label_title',
            i18n_domain='FacultyStaffDirectory',
            visible={'edit': 'invisible', 'view': 'invisible' },
        )
    ),
),
)

DepartmentalMembership_schema = BaseSchema.copy() + schema.copy()

class DepartmentalMembership(BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(BaseContent,'__implements__',()),)
    meta_type = portal_type = 'FSDDepartmentalMembership'
    _at_rename_after_creation = True
    schema = DepartmentalMembership_schema
       
    aliases = {
        '(Default)' : '(dynamic view)',
        'view' : '(selected layout)',
        'index.html' : '(dynamic view)',
        'edit' : 'departmentalmembership_edit',
    }

registerType(DepartmentalMembership, PROJECTNAME)
