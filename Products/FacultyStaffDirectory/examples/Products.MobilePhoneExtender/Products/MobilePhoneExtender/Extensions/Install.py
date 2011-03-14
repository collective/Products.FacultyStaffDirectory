from Products.CMFCore.utils import getToolByName

def _runProfile(profile, portal):
    setupTool = getToolByName(portal, 'portal_setup')
    setupTool.runAllImportStepsFromProfile(profile)

def install(portal):
    _runProfile('profile-Products.MobilePhoneExtender:default', portal)

def uninstall(portal):
    _runProfile('profile-Products.MobilePhoneExtender:uninstall', portal)
