# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'
# Product configuration.
#
# The contents of this module will be imported into __init__.py, the
# workflow configuration and every content type module.

from Products.CMFCore.permissions import setDefaultRoles

PROJECTNAME = "FacultyStaffDirectory"

# Permissions
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
setDefaultRoles(DEFAULT_ADD_CONTENT_PERMISSION, ('Manager', 'Owner'))
ADD_CONTENT_PERMISSIONS = {
    'Person': 'FacultyStaffDirectory: Add or Remove People',
}

setDefaultRoles('FacultyStaffDirectory: Add or Remove People', ('Manager', 'Owner', 'Personnel Manager'))

product_globals = globals()

# Dependencies of Products to be installed by quick-installer
DEPENDENCIES = ["Relations", "ATReferenceBrowserWidget"]

# Dependend products - not quick-installed - used in testcase
PRODUCT_DEPENDENCIES = []

# XXX should really be merged with list above
DEPENDENT_PRODUCTS = ['membrane',]

# You can overwrite these two in an AppConfig.py:
# STYLESHEETS = [{'id': 'my_global_stylesheet.css'},
#                {'id': 'my_contenttype.css',
#                 'expression': 'python:object.getTypeInfo().getId() == "MyType"'}]
# You can do the same with JAVASCRIPTS.
STYLESHEETS = [{'id': 'facultyStaffDirectory.css', 'media': 'all'}]
JAVASCRIPTS = []

# membrane stuff, roles we don't want groups to be able to use
INVALID_ROLES = ['Manager', 'Owner', 'Anonymous', 'Authenticated', 'User Preferences Editor']
# Annotation key used for passwords
PASSWORD_KEY = 'fsd.employee.password'
# what content types are available for membrane functionality?
MEMBRANE_ABLE_TYPES_CHOICES = [('People', 'FSDPerson'), ('Classifications', 'FSDClassification'), ('Committees', 'FSDCommittee'), ('Specialties', 'FSDSpecialty')]
MEMBRANE_ABLE_TYPES = set([v for k, v in MEMBRANE_ABLE_TYPES_CHOICES])
MEMBRANE_TYPE_ACTIVE_STATES = {'FSDPerson': ['active'],
                               'FSDClassification': ['active'],
                               'FSDCommittee': ['active'],
                               'FSDSpeciality': ['active']}

# content-types
ALLOWABLE_CONTENT_TYPES = ('text/plain', 'text/structured', 'text/html', 'application/msword', 'text/x-rst')

#catalog stuff
ADDITIONAL_CATALOG_INDEXES = [('getSortableName', 'FieldIndex'), ('getRawClassifications', 'KeywordIndex'), ('getRawSpecialties', 'KeywordIndex'), ('getRawCommittees', 'KeywordIndex'), ('getRawPeople', 'KeywordIndex')]
ADDITIONAL_CATALOG_METADATA = ["UID", "getCommitteeNames", "getSpecialtyNames", "getClassificationNames", "getResearchTopics"]
