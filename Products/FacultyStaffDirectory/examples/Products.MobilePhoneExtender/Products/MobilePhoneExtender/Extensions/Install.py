from Products.CMFCore.utils import getToolByName
from Products.FacultyStaffDirectory.extenderInstallation import localAdaptersAreSupported, installExtender, uninstallExtender
from Products.MobilePhoneExtender.person import PersonExtender

_adapterName = 'MobilePhoneExtender'

def _runProfile(profile, portal):
    setupTool = getToolByName(portal, 'portal_setup')
    setupTool.runAllImportStepsFromProfile(profile)

def install(portal):
    if localAdaptersAreSupported:
        installExtender(portal, PersonExtender, _adapterName)
    _runProfile('profile-Products.MobilePhoneExtender:default', portal)

def uninstall(portal):
    if localAdaptersAreSupported:
        uninstallExtender(portal, PersonExtender, _adapterName)
    _runProfile('profile-Products.MobilePhoneExtender:uninstall', portal)
