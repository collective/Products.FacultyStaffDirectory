""" FacultyStaffDirectory 1.0 to 2.0 migration script. 
    To run the migration, add a new External Method to your Plone site with the following parameters:
    id: migrateFSD
    Title: Migrate FacultyStaffDirectory
    Module Name: FacultyStaffDirectory.migrate1dot0to2dot0
    Function Name: migrate
    
    To run the migration, either click the "Test" tab of the External Method in the ZMI, or call it through your browser at http://yourplonesiturl/pathtoscript/migrateFSD. """

from Products.CMFCore.utils import getToolByName
from StringIO import StringIO
try:
    from Products.ATContentTypes.migration.walker import CatalogWalker
    from Products.ATContentTypes.migration.migrator import CMFFolderMigrator, CMFItemMigrator
except ImportError:
    try:
        from Products.contentmigration.basemigrator.walker import CatalogWalker
        from Products.contentmigration.basemigrator.migrator import CMFItemMigrator
    except ImportError:
        raise ImportError, "Unable to find product: contentmigration. Faculty/Staff Directory migration could not be completed."
from Products.FacultyStaffDirectory.Extensions.Install import linkableKupuTypes, mediaKupuTypes, collectionKupuTypes, addKupuResource, removeKupuResource

        
class FacultyStaffDirectoryMigrator(CMFItemMigrator):
    walkerClass = CatalogWalker
    src_meta_type = 'FacultyStaffDirectory'
    src_portal_type = 'FacultyStaffDirectory'
    dst_meta_type = 'FSDFacultyStaffDirectory'
    dst_portal_type = 'FSDFacultyStaffDirectory'

class PersonMigrator(CMFItemMigrator):
    walkerClass = CatalogWalker
    src_meta_type = 'Person'
    src_portal_type = 'Person'
    dst_meta_type = 'FSDPerson'
    dst_portal_type = 'FSDPerson'

class ClassificationMigrator(CMFItemMigrator):
    walkerClass = CatalogWalker
    src_meta_type = 'Classification'
    src_portal_type = 'Classification'
    dst_meta_type = 'FSDClassification'
    dst_portal_type = 'FSDClassification'
   
class CourseMigrator(CMFItemMigrator):
    walkerClass = CatalogWalker
    src_meta_type = 'Course'
    src_portal_type = 'Course'
    dst_meta_type = 'FSDCourse'
    dst_portal_type = 'FSDCourse'
    
class CommitteesFolderMigrator(CMFItemMigrator):
    walkerClass = CatalogWalker
    src_meta_type = 'CommitteesFolder'
    src_portal_type = 'CommitteesFolder'
    dst_meta_type = 'FSDCommitteesFolder'
    dst_portal_type = 'FSDCommitteesFolder'

class CommitteeMigrator(CMFItemMigrator):
    walkerClass = CatalogWalker
    src_meta_type = 'Committee'
    src_portal_type = 'Committee'
    dst_meta_type = 'FSDCommittee'
    dst_portal_type = 'FSDCommittee'

class SpecialtyMigrator(CMFItemMigrator):
    walkerClass = CatalogWalker
    src_meta_type = 'Specialty'
    src_portal_type = 'Specialty'
    dst_meta_type = 'FSDSpecialty'
    dst_portal_type = 'FSDSpecialty'

class SpecialtiesFolderMigrator(CMFItemMigrator):
    walkerClass = CatalogWalker
    src_meta_type = 'SpecialtiesFolder'
    src_portal_type = 'SpecialtiesFolder'
    dst_meta_type = 'FSDSpecialtiesFolder'
    dst_portal_type = 'FSDSpecialtiesFolder'

class PersonGroupingMigrator(CMFItemMigrator):
    walkerClass = CatalogWalker
    src_meta_type = 'PersonGrouping'
    src_portal_type = 'PersonGrouping'
    dst_meta_type = 'FSDPersonGrouping'
    dst_portal_type = 'FSDPersonGrouping'

class DepartmentMigrator(CMFItemMigrator):
    walkerClass = CatalogWalker
    src_meta_type = 'Department'
    src_portal_type = 'Department'
    dst_meta_type = 'FSDDepartment'
    dst_portal_type = 'FSDDepartment'

class CommitteeMembershipMigrator(CMFItemMigrator):
    walkerClass = CatalogWalker
    src_meta_type = 'CommitteeMembership'
    src_portal_type = 'CommitteeMembership'
    dst_meta_type = 'FSDCommitteeMembership'
    dst_portal_type = 'FSDCommitteeMembership'

class SpecialtyInformationMigrator(CMFItemMigrator):
    walkerClass = CatalogWalker
    src_meta_type = 'SpecialtyInformation'
    src_portal_type = 'SpecialtyInformation'
    dst_meta_type = 'FSDSpecialtyInformation'
    dst_portal_type = 'FSDSpecialtyInformation'

class DepartmentalMembershipMigrator(CMFItemMigrator):
    walkerClass = CatalogWalker
    src_meta_type = 'DepartmentalMembership'
    src_portal_type = 'DepartmentalMembership'
    dst_meta_type = 'FSDDepartmentalMembership'
    dst_portal_type = 'FSDDepartmentalMembership'

class FacultyStaffDirectoryToolMigrator(CMFItemMigrator):
    walkerClass = CatalogWalker
    src_meta_type = 'FacultyStaffDirectoryTool'
    src_portal_type = 'FacultyStaffDirectoryTool'
    dst_meta_type = 'FSDFacultyStaffDirectoryTool'
    dst_portal_type = 'FSDFacultyStaffDirectoryTool'

def migrate(self):
    """Run the migration"""

    out = StringIO()
    print >> out, "Starting migration"
    
    print >> out, "Removing Kupu customizations"
    oldLinkableKupuTypes = ['Person', 'Course', 'Classification', 'Department', 'Committee', 'CommitteesFolder', 'Specialty', 'SpecialtiesFolder']
    oldMediaKupuTypes = ['Person']
    oldCollectionKupuTypes = ['FacultyStaffDirectory']

    for type in oldLinkableKupuTypes:
        removeKupuResource(self, 'linkable', type)
    for type in oldMediaKupuTypes:
        removeKupuResource(self, 'mediaobject', type)
    for type in oldCollectionKupuTypes:
        removeKupuResource(self, 'collection', type)

    portal_url = getToolByName(self, 'portal_url')
    portal = portal_url.getPortalObject()
    cat = getToolByName(self, 'portal_catalog')
  
    migrators = FacultyStaffDirectoryMigrator, ClassificationMigrator, PersonMigrator, CourseMigrator, CommitteesFolderMigrator, CommitteeMigrator, SpecialtyMigrator, SpecialtiesFolderMigrator, PersonGroupingMigrator, DepartmentMigrator, CommitteeMembershipMigrator, SpecialtyInformationMigrator, DepartmentalMembershipMigrator, FacultyStaffDirectoryToolMigrator
  
    for migrator in migrators:
        walker = migrator.walkerClass(portal, migrator)
        print >> out, "Migrating %s..." % migrator.src_portal_type
        walker.go(out=out)
        print >> out, walker.getOutput()
        # Update the portal_type since the migrator doesn't seem to be doing it. Jackass.
        results = cat(portal_type=migrator.src_portal_type)
        for brain in results:
            ob = brain.getObject()
            ob._setPortalTypeName(migrator.dst_portal_type)
            ob.reindexObject(['portal_type'])
  
    # Force an update of person images so that member portraits are set.    
    print >> out, "Updating member portraits"
    results = cat(portal_type="FSDPerson")
    for brain in results:
        person = brain.getObject() 
        person.setImage(person.getImage())
      
    # And let's also update workflows
    print >> out, "Updating workflow"
    wf = getToolByName(self, 'portal_workflow')
    wf.updateRoleMappings()

    # Update Kupu settings
    print >> out, "Applying Kupu customizations"
    for type in linkableKupuTypes:
        addKupuResource(self, 'linkable', type)
    for type in mediaKupuTypes:
        addKupuResource(self, 'mediaobject', type)        
    for type in collectionKupuTypes:
        addKupuResource(self, 'collection', type)
    
     
    print >> out, "Migration finished"
    return out.getvalue()