from AccessControl import ClassSecurityInfo
from Acquisition import Implicit
from Globals import InitializeClass
from persistent import Persistent
from zope.app.component.hooks import getSite
from zope.event import notify
from zope.i18nmessageid import MessageFactory
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from Products.CMFCore.utils import getToolByName
from Products.membrane.config import TOOLNAME as MEMBRANE_TOOL
from Products.FacultyStaffDirectory.interfaces import IConfiguration, IMembraneIntegrationModifiedEvent

class MembraneTypesModifiedEvent(object):
    implements(IMembraneIntegrationModifiedEvent)

    def __init__(self, context):
        self.context = context

class ConfigurationUtility(Persistent, Implicit):
    """A mindless rewriting of the FSDTool as a utility.
    
    Next step: break this up into little utilities that can be overridden separately.
    
    """
    implements(IConfiguration)
    
    security = ClassSecurityInfo()
    
    # I couldn't get a for loop to do this. I wildly guess that it's due to some metaclass weirdness due to Persistent.
    phoneNumberRegex = FieldProperty(IConfiguration["phoneNumberRegex"])
    phoneNumberDescription = FieldProperty(IConfiguration["phoneNumberDescription"])
    
    idLabel = FieldProperty(IConfiguration["idLabel"])
    idRegex = FieldProperty(IConfiguration["idRegex"])
    idRegexErrorMessage = FieldProperty(IConfiguration["idRegexErrorMessage"])
    
    security.declarePublic('obfuscateEmailAddresses')
    obfuscateEmailAddresses = FieldProperty(IConfiguration["obfuscateEmailAddresses"])
    
    security.declarePublic('useInternalPassword')
    useInternalPassword = FieldProperty(IConfiguration["useInternalPassword"])
    
    
    # Wrap setting enableMembraneType to fire an event:
    _enableMembraneTypes = FieldProperty(IConfiguration["enableMembraneTypes"])
    
    def _getEnableMembraneTypes(self):
        return self._enableMembraneTypes
    
    def _setEnableMembraneTypes(self, value):
        self._enableMembraneTypes = value
        notify(MembraneTypesModifiedEvent(self))
    
    security.declarePublic('enableMembraneTypes')
    enableMembraneTypes = property(_getEnableMembraneTypes, _setEnableMembraneTypes)
    
    del _getEnableMembraneTypes, _setEnableMembraneTypes
    

    security.declarePublic('fsdMemberProfile')
    def fsdMemberProfile(self):
        """Distinguish between an fsd user and a regular acl_users user and return the appropriate link for their 'personal profile' page.
        
        For membrane users, this will be the Person object that defines them.  For acl_users users it will be 'personalize_form'.
        
        """
        # TODO: perhaps turn this into an adapter on the user: IPersonalProfileLink(user) or something. Or maybe not--it's called from templates and CMF Expressions all the time.
        site = getSite()
        mt = getToolByName(site, 'portal_membership')
        mb = getToolByName(site, MEMBRANE_TOOL)
        
        if not mt.isAnonymousUser():
            member = mt.getAuthenticatedMember().getUser()
            foundUsers = mb.searchResults(getUserName=member.getUserName())
            if foundUsers:
                user = foundUsers[0] # grab the first match
                if user.portal_type == 'FSDPerson':
                    # this is an FSD Person , get its url and go there
                    return user.getURL() + '/edit?fieldset=User%20Settings'
            return getToolByName(site, 'portal_url')() + '/personalize_form'

    security.declarePublic('fsdMyFolder')
    def fsdMyFolder(self, id=None):
        """This method attempts to distinguish between a membrane user and a regular
        acl_users user and send them to the appropriate user folder"""
        site = getSite()
        mt = getToolByName(site, 'portal_membership')
        mb = getToolByName(site, MEMBRANE_TOOL)
        if id:
            # an id has been passed in, find the user object for that id in acl_users
            member = mt.getMemberById(id).getUser()
        else:
            member = mt.getAuthenticatedMember().getUser()
        try:
            user = mb.searchResults(getUserName=member.getUserName())[0]
            if user.portal_type == 'FSDPerson':
                # This is an FSD Person; get its url and go there:
                return user.getURL()
            else:
                # This is a user defined by membrane, but not an FSDPerson; do the regular thing:
                return mt.getHomeUrl(id)
        except (IndexError, AttributeError):
            # This user is not a membrane user at all; do the regular thing:
            return mt.getHomeUrl(id)
            
    security.declarePublic('fsdShowMyFolder')
    def fsdShowMyFolder(self, id=None):
        """A test to be used as the condition for the fsdMyFolder action, it will distinguish
        between a membrane user and a non-membrane user, and act accordingly"""
        site = getSite()
        mt = getToolByName(site, 'portal_membership')
        mb = getToolByName(site, MEMBRANE_TOOL)
        # We need to protect against the edge-case of an anonymous viewer opening the author
        # page directly, which throws an error in this script.
        if mt.isAnonymousUser():
            # anonymous user should never see the 'MY Folder' link at all.
            return False
        else:
            if id:
                member = mt.getMemberById(id).getUser()
            else:
                member = mt.getAuthenticatedMember().getUser()
            try:
                user = mb.searchResults(getUserName=member.getUserName())[0]
                if user.portal_type == 'FSDPerson':
                    # this is an FSDPerson, always return true
                    return True
                else:
                    # this is a membrane user, but not an FSDPerson, check conditions before allowing
                    if mt.getMemberareaCreationFlag() and mt.getHomeFolder(id) is not None:
                        return True
                    else:
                        return False
            except (IndexError, AttributeError):
                # this is not a membrane user at all, let's check some conditions
                if mt.getMemberareaCreationFlag() and mt.getHomeFolder(id) is not None:
                    return True
                else:
                    return False

InitializeClass(ConfigurationUtility)  # Make security declarations work.