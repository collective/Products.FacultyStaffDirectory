from OFS.Folder import manage_addFolder
from Products.CMFCore.utils import getToolByName
from Products.FacultyStaffDirectory.permissions import ASSIGN_CLASSIFICATIONS_TO_PEOPLE
from Products.FacultyStaffDirectory.permissions import ASSIGN_SPECIALTIES_TO_PEOPLE
from Products.FacultyStaffDirectory.permissions import ASSIGN_COMMITTIES_TO_PEOPLE
from Products.FacultyStaffDirectory.permissions import ASSIGN_DEPARTMENTS_TO_PEOPLE
from Products.Archetypes.atapi import listTypes
from Products.FacultyStaffDirectory.config import PROJECTNAME

originalMyFolderActionId = "mystuff"
newMyFolderActionId = "fsdmystuff"
originalProfileActionId = "MemberPrefs"
newProfileActionId = "fsdMemberPrefs"
linkableKupuTypes = ['FSDPerson', 'FSDCourse', 'FSDClassification', 'FSDDepartment', 'FSDCommittee', 'FSDCommitteesFolder', 'FSDSpecialty', 'FSDSpecialtiesFolder']
mediaKupuTypes = ['FSDPerson']
collectionKupuTypes = ['FSDFacultyStaffDirectory']

def install(self, product=None, reinstall=None):
    """ Custom install tasks
    """
    pass    

def uninstall(self, product=None, reinstall=None):
    """ Custom uninstall tasks
    """
    pass       
