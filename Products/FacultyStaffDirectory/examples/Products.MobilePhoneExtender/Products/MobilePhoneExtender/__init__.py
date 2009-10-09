from Products.CMFCore.DirectoryView import registerDirectory
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.FacultyStaffDirectory.extenderInstallation import installExtenderGloballyIfLocallyIsNotSupported
from Products.GenericSetup import EXTENSION, profile_registry

from Products.MobilePhoneExtender.person import PersonExtender

installExtenderGloballyIfLocallyIsNotSupported(PersonExtender, 'Products.MobilePhoneExtender')  # Put the name of your product here.

registerDirectory('skins', globals())

def initialize(context):
    profile_registry.registerProfile(
        "default",
        "MobilePhoneExtender",
        "Adds a Mobile Phone field to Faculty/Staff Directory's Person type.",
        "profiles/default",
        product="Products.MobilePhoneExtender",
        profile_type=EXTENSION,
        for_=IPloneSiteRoot)
    profile_registry.registerProfile(
        "uninstall",
        "MobilePhoneExtender Uninstall",
        "Removes the Mobile Phone field from the Person type.",
        "profiles/uninstall",
        product="Products.MobilePhoneExtender",
        profile_type=EXTENSION,
        for_=IPloneSiteRoot)
