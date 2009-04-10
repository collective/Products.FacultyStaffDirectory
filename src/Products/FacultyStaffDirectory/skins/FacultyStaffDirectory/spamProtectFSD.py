##parameters=email

# Implement a different email obfuscating approach than the standard Plone spam
# protection.  Dots, @ etc. will be replaced with a string representation.

from Products.CMFCore.utils import getToolByName
portal = getToolByName(context, 'portal_url').getPortalObject()

if portal.restrictedTraverse('++fsdmembership++snork').getObfuscateEmailAddresses():
    email = email.replace('.', ' [ DOT ] ')
    email = email.replace('@', ' [ AT ] ')
    email = email.replace('-', ' [ DASH ] ')
    email = email.replace('_', ' [ UNDERSCORE ] ')
    return email
else:
    return context.spamProtect(email)
