# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import pkg_resources


try:
    pkg_resources.get_distribution('plone.app.contenttypes')
except pkg_resources.DistributionNotFound:
    from plone.app.testing import PLONE_FIXTURE
else:
    from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE as PLONE_FIXTURE


IS_PLONE_5 = api.env.plone_version().startswith('5')


class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import Products.membrane
        self.loadZCML(package=Products.membrane)
        import Products.Relations
        self.loadZCML(package=Products.Relations)
        import Products.FacultyStaffDirectory
        self.loadZCML(package=Products.FacultyStaffDirectory)
        z2.installProduct(app, 'Products.membrane')
        z2.installProduct(app, 'Products.Relations')
        z2.installProduct(app, 'Products.FacultyStaffDirectory')

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'Products.FacultyStaffDirectory:default')
        self.applyProfile(portal, 'Products.FacultyStaffDirectory:sample-content')


FIXTURE = Fixture()

INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='Products.FacultyStaffDirectory:Integration')

FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='Products.FacultyStaffDirectory:Functional')

