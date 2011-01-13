from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implements

class FSDNonInstallable(object):
    implements(INonInstallable)

    def getNonInstallableProfiles(self):
        return [u'Products.FacultyStaffDirectory:plone3-actions-fix',
                u'Products.FacultyStaffDirectory:default',
                u'Products.FacultyStaffDirectory:uninstall']
