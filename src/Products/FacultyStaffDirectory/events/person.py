from zope.component import getUtility
from Acquisition import aq_parent, aq_inner
from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces import IUserRelated
from Products.FacultyStaffDirectory.AssociationContent import AssociationContent
from Products.FacultyStaffDirectory.interfaces import IConfiguration
from plone.app.relations.interfaces import IAnnotationsContext
from plone.relations.interfaces import IContextAwareRelationship
from zope.app.annotation.interfaces import IAttributeAnnotatable    
from zope.interface import alsoProvides

def modifyPersonOwnership(event):
    """Let people own their own objects and modify their own user preferences.
    
    Stolen from Plone and CMF core, but made less picky about where users are 
    found. (and from borg, thanks, optilude!)
    
    """
    context = event.context

    # Only run this if FSDPerson is an active membrane type.
    fsd_tool = getUtility(IConfiguration)
    if 'FSDPerson' in fsd_tool.enableMembraneTypes:

        catalog = getToolByName(context, 'portal_catalog')
        userId = IUserRelated(context).getUserId()
        userFolder = getToolByName(context, 'acl_users')
        
        user = None
        while userFolder is not None:
            user = userFolder.getUserById(userId)
            if user is not None:
                break
            container = aq_parent(aq_inner(userFolder))
            parent = aq_parent(aq_inner(container))
            userFolder = getattr(parent, 'acl_users', None)
        
        if user is None:
            raise KeyError, "User %s cannot be found." % userId
        
        context.changeOwnership(user, False)

        def fixPersonRoles(context, userId):
            # Remove all other Owners of this Person object. Note that the creator will have an implicit
            # owner role. The User Preferences Editor role allows us to allow the user defined by the Person
            # to manage their own password and user preferences, but prevent the creator of the Person object
            # from modifying those fields.
            for owner in context.users_with_local_role('Owner'):
                roles = list(context.get_local_roles_for_userid(owner))
                roles.remove('Owner')
                if roles:
                    context.manage_setLocalRoles(owner, roles)
                else:
                    context.manage_delLocalRoles([owner])
                    
            # Grant 'Owner' and 'User Preferences Editor' to the user defined by this object:
            roles = list(context.get_local_roles_for_userid(userId))
            roles.extend(['Owner', 'User Preferences Editor'])
            # eliminate duplicated roles
            roles = list(set(roles))
            context.manage_setLocalRoles(userId, roles)
            
            # Grant 'Owner' only to any users listed as 'assistants':
            for assistant in context.getReferences(relationship="people_assistants"):
                pid = assistant.id
                user = userFolder.getUserById(pid)
                if user is None:
                    raise KeyError, "User %s cannot be found." % pid
                roles = list(context.get_local_roles_for_userid(pid))
                roles.append('Owner')
                context.manage_setLocalRoles(pid, roles)

        fixPersonRoles(context, user.getId())
        catalog.reindexObject(context)

def deleteAssociationContent(rel, event):
    """Delete the AssociationContent object defined for the passed relationship."""
    obj = IContextAwareRelationship(rel).getContext()
    if obj and obj.id in obj.aq_parent.objectIds():
        obj.aq_parent.manage_delObjects([obj.id])
    
def addAssociationContent(rel, event):
    """Create and assign an AssociationContent object to the passed relationship."""
    sourceObj = list(rel.sources)[0]
    targetObj = list(rel.targets)[0]
    uid = targetObj.UID()
    sourceObj.at_references._setObject(uid, AssociationContent(uid))
    # For some reason, applying the interfaces above isnt' working. For now...
    alsoProvides(rel, IAttributeAnnotatable, IAnnotationsContext)
    IContextAwareRelationship(rel).setContext(sourceObj.at_references[uid])
    
def preEditSetup(self, event):
    """ Set some edit form values/settings."""
    # Set the startup directory for the specialties field to the SpecialtiesFolder or, failing
    # that, the root of the FacultyStaffDirectory:
    urlTool = getToolByName(self, 'portal_url')
    fsd = self.getDirectoryRoot()
    # if fsd and fsd.getSpecialtiesFolder():
    #     url = urlTool.getRelativeContentURL(fsd.getSpecialtiesFolder())
    # else:
    #     url = ""
    # self.schema['specialties'].widget.startup_directory = '/%s' % url
    
    fsd_utility = getUtility(IConfiguration)
    if fsd_utility.phoneNumberRegex:
        self.schema['officePhone'].widget.description = u"Example: %s" % fsd_utility.phoneNumberDescription
    if fsd_utility.idLabel:
        self.schema['id'].widget.label = u"%s" % fsd_utility.idLabel

    # Make sure the default for the editor field is the same as the site defaut. No idea why this isn't being handled properly.
    self.schema['userpref_wysiwyg_editor'].default = getToolByName(self, 'portal_memberdata').wysiwyg_editor
    
