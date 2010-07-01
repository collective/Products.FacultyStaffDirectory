import re

from zope.app.component.hooks import getSite
from zope.interface import Interface
from zope.schema import TextLine, Bool, Set, Choice
from zope.schema.vocabulary import SimpleVocabulary
from Products.CMFCore.utils import getToolByName

from Products.FacultyStaffDirectory import FSDMessageFactory as _
from Products.FacultyStaffDirectory.config import MEMBRANE_ABLE_TYPES, MEMBRANE_ABLE_TYPES_CHOICES

class RegexLine(TextLine):
    """A regular expression with no newlines."""

    def constraint(self, value):
        """Return whether `value` compiles as a regex and contains no newlines."""
        try:
            re.compile(value)
        except re.error:
            return False
        else:
            return super(RegexLine, self).constraint(value)

class PersonIdRegexLine(RegexLine):
    """A RegexLine whose default is computed at field binding time. The default also happens to be the user ID validation regex from the portal_registration tool nearest the bound object."""
    # A more generic DynamicDefaultField, with a lambda you pass in, might be cool someday.
    
    def bind(self, object):
        cloned_field = super(PersonIdRegexLine, self).bind(object)
        pr = getToolByName(getSite(), 'portal_registration')
        cloned_field.default = unicode(pr.getIDPattern() or pr.getDefaultIDPattern())
        return cloned_field

class IGeneralConfiguration(Interface):
    phoneNumberRegex = RegexLine(
        title=_(u"Phone number format"),
        description=_(u"A regular expression that a Person's phone number must match. Leave blank to disable phone number validation."),
        default=u"^\\(\\d{3}\\) \\d{3}-\\d{4}",
        )
        
    phoneNumberDescription = TextLine(
        title=_(u"Phone number example"),
        description=_(u"Describe the above phone number rule in a human-readable format: for example, (555) 555-5555."),
        default=u"(555) 555-5555",
        )

    obfuscateEmailAddresses = Bool(
        title=_(u"Custom email obfuscation"),
        description=_(u"Format email addresses like \"someone AT here DOT com\" rather than using Plone's default spam armoring."),
        default=False,
        )
    
class IMembershipConfiguration(Interface):
    idLabel = TextLine(
        title=_(u"Person ID label"),
        description=_(u"The name of the ID used by your organization"),
        default=_("Access Account ID"),
        required=True,
        )
        
    idRegex = PersonIdRegexLine(
        title=_(u"Person ID format"),
        description=_(u"A regular expression that a Person's ID must match. Defaults to the expression Plone uses for user IDs."),
        default=None,
        required=True,
        )
        
    idRegexErrorMessage = TextLine(
        title=_(u"Person ID format error message"),
        description=_(u"The error message returned when an entered Person ID does not match the above format"),
        default=_(u"Invalid user id"),
        required=True,  
        )
    
    enableMembraneTypes = Set(
        title=_(u"Content types to integrate with Plone's users and groups"),
        value_type=Choice(vocabulary=SimpleVocabulary.fromItems(MEMBRANE_ABLE_TYPES_CHOICES)),
        default=MEMBRANE_ABLE_TYPES,
        )
    
    useInternalPassword = Bool(
        title=_(u"Person objects provide user passwords"),
        description=_(u"Should user passwords be stored as part of the Person? To have a different PAS plugin handle authorization, turn this off."),
        default=True,
        )
        
class IConfiguration(IGeneralConfiguration, IMembershipConfiguration):
	"""Combined schema for the Configuration utility."""
