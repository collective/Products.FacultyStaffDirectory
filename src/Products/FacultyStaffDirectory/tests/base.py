__docformat__ = 'plaintext'
"""Base class for integration tests, based on ZopeTestCase and PloneTestCase.

Note that importing this module has various side-effects: it registers a set of
products with Zope, and it sets up a sandbox Plone site with the appropriate
products installed.
"""
from Testing import ZopeTestCase
from Globals import package_home
from random import choice, sample

from Products.CMFCore.utils import getToolByName

from Products.FacultyStaffDirectory.config import DEPENDENCIES
from Products.FacultyStaffDirectory.config import DEPENDENT_PRODUCTS
from Products.FacultyStaffDirectory.config import PROJECTNAME

PACKAGE_HOME = package_home(globals())

# Let Zope know about the products we require above-and-beyond a basic
# Plone install (PloneTestCase takes care of these).
PRODUCTS = list()
PRODUCTS += DEPENDENCIES
PRODUCTS.append('FacultyStaffDirectory')
for dependency in PRODUCTS:
    ZopeTestCase.installProduct(dependency)
for dependency in DEPENDENT_PRODUCTS:
    ZopeTestCase.installProduct(dependency)
ZopeTestCase.installProduct('FacultyStaffDirectory')

# Manually add plone.app.relations
from OFS.Application import install_package
app = ZopeTestCase.app()
import plone.app.relations
install_package(app, plone.app.relations, plone.app.relations.initialize)

# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase.PloneTestCase import PloneTestCase
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite


# Set up a Plone site, and apply the Library enquiry extension profile
# to make sure they are installed.
setupPloneSite(extension_profiles=('Products.FacultyStaffDirectory:default',))

class FacultyStaffDirectoryTestCase(PloneTestCase):
    """Base class for integration tests for the 'FacultyStaffDirectory' product. This may
    provide specific set-up and tear-down operations, or provide convenience
    methods."""

    #Utility methods

    def reinstallProduct(self):
        """Reinstall the product"""
        portal_setup = getToolByName(self.portal, 'portal_setup')
        self.setRoles(('Manager',))
        portal_setup.runAllImportStepsFromProfile('profile-Products.%s:default' % PROJECTNAME)
        self.setRoles(('Member',))

    def getEmptyDirectory(self, id="facstaffdirectory", portal=None):
        """Return a FacultyStaffDirectory (creating it first if necessary)."""
        portal = portal or self.portal
        if 'facstaffdirectory' not in portal.contentIds():
            self.setRoles(('Manager',))
            portal.invokeFactory(type_name="FSDFacultyStaffDirectory", id=id)
            self.setRoles(('Member',))
        return portal[id]

    def getPopulatedDirectory(self, id="facstaffdirectory"):
        """Create a FSD containing some stuff, including..."""
        fsd = self.getEmptyDirectory(id)
        # Run the post-create script for some auto-generated content:
        fsd.at_post_create_script()
        return fsd

    def getPerson(self, directory=None, id="abc123", firstName="Test", lastName="Person", portal=None):
        """Create a Person, using only the required fields."""
        portal = portal or self.portal
        if not directory:
            directory = self.getEmptyDirectory(portal=portal)
        directory.invokeFactory(type_name="FSDPerson", id=id, firstName=firstName, lastName=lastName)
        return directory[id]

    # Commented out for now, it gets blasted at the moment anyway.
    # Place it in the protected section if you need it.
    #def afterSetup(self):
    #    """
    #    """
    #    pass

    def interact(self, locals=None):
        """Provides an interactive shell aka console inside your testcase.

        It looks exact like in a doctestcase and you can copy and paste
        code from the shell into your doctest. The locals in the testcase are
        available, because you are in the testcase.

        In your testcase or doctest you can invoke the shell at any point by
        calling::

            >>> self.interact( locals() )

        locals -- passed to InteractiveInterpreter.__init__()
        
        """
        savestdout = sys.stdout
        sys.stdout = sys.stderr
        sys.stderr.write('='*70)
        console = code.InteractiveConsole(locals)
        console.interact("""
ZopeTestCase Interactive Console
(c) BlueDynamics Alliance, Austria - 2005

Note: You have the same locals available as in your test-case.
""")
        sys.stdout.write('\nend of ZopeTestCase Interactive Console session\n')
        sys.stdout.write('='*70+'\n')
        sys.stdout = savestdout
        
    def getLargeDirectory(self, directory=None, numPersons=100):
        """Generate a large number of persons in a directory."""
        
        firstNames = ("Jacob","Michael","Ethan","Joshua","Daniel","Christopher","Anthony","William",
                      "Matthew","Andrew","Alexander","David","Joseph","Noah","James","Ryan",
                      "Logan","Jayden","John","Nicholas","Tyler","Christian","Jonathan","Nathan",
                      "Samuel","Benjamin","Aiden","Gabriel","Dylan","Elijah","Brandon","Gavin",
                      "Jackson","Angel","Jose","Caleb","Mason","Jack","Kevin","Evan",
                      "Isaac","Zachary","Isaiah","Justin","Jordan","Luke","Robert","Austin",
                      "Landon","Cameron","Thomas","Aaron","Lucas","Aidan","Connor","Owen",
                      "Hunter","Diego","Jason","Luis","Adrian","Charles","Juan","Brayden",
                      "Adam","Julian","Jeremiah","Xavier","Wyatt","Carlos","Hayden","Sebastian",
                      "Alex","Ian","Sean","Jaden","Jesus","Bryan","Chase","Carter",
                      "Brian","Nathaniel","Eric","Cole","Dominic","Kyle","Tristan","Blake",
                      "Liam","Carson","Henry","Caden","Brady","Miguel","Cooper","Antonio",
                      "Steven","Kaden","Richard","Timothy","Girls","Name","Emily","Isabella",
                      "Emma","Ava","Madison","Sophia","Olivia","Abigail","Hannah","Elizabeth",
                      "Addison","Samantha","Ashley","Alyssa","Mia","Chloe","Natalie","Sarah",
                      "Alexis","Grace","Ella","Brianna","Hailey","Taylor","Anna","Kayla",
                      "Lily","Lauren","Victoria","Savannah","Nevaeh","Jasmine","Lillian","Julia",
                      "Sofia","Kaylee","Sydney","Gabriella","Katherine","Alexa","Destiny","Jessica",
                      "Morgan","Kaitlyn","Brooke","Allison","Makayla","Avery","Alexandra","Jocelyn",
                      "Audrey","Riley","Kimberly","Maria","Evelyn","Zoe","Brooklyn","Angelina",
                      "Andrea","Rachel","Madeline","Maya","Kylie","Jennifer","Mackenzie","Claire",
                      "Gabrielle","Leah","Aubrey","Arianna","Vanessa","Trinity","Ariana","Faith",
                      "Katelyn","Haley","Amelia","Megan","Isabelle","Melanie","Sara","Sophie",
                      "Bailey","Aaliyah","Layla","Isabel","Nicole","Stephanie","Paige","Gianna",
                      "Autumn","Mariah","Mary","Michelle","Jada","Gracie","Molly","Valeria",
                      "Caroline","Jordan",)
        
        lastNames = ("Smith","Johnson","Williams","Jones","Brown","Davis","Miller","Wilson",
                     "Moore","Taylor","Anderson","Thomas","Jackson","White","Harris","Martin",
                     "Thompson","Garcia","Martinez","Robinson","Clark","Rodriguez","Lewis","Lee",
                     "Walker","Hall","Allen","Young","Hernandez","King","Wright","Lopez",
                     "Hill","Scott","Green","Adams","Baker","Gonzalez","Nelson","Carter",
                     "Mitchell","Perez","Roberts","Turner","Phillips","Campbell","Parker","Evans",
                     "Edwards","Collins","Stewart","Sanchez","Morris","Rogers","Reed","Cook",
                     "Morgan","Bell","Murphy","Bailey","Rivera","Cooper","Richardson","Cox",
                     "Howard","Ward","Torres","Peterson","Gray","Ramirez","James","Watson",
                     "Brooks","Kelly","Sanders","Price","Bennett","Wood","Barnes","Ross",
                     "Henderson","Coleman","Jenkins","Perry","Powell","Long","Patterson","Hughes",
                     "Flores","Washington","Butler","Simmons","Foster","Gonzales","Bryant","Alexander",
                     "Russell","Griffin","Diaz","Hayes",)
                     
        lcLetters = [chr(x) for x in range(ord('a'), ord('z'))]
        ucLetters = [chr(x) for x in range(ord('A'), ord('Z'))]
        digits = [chr(x) for x in range(ord('0'), ord('9'))]
        
        if not directory:
            portal = portal or self.portal
            directory = self.getEmptyDirectory(portal=portal)
               
        generated_ids = []
        i = 0
        while i < numPersons:
            i += 1
            
            #build an id, make sure it is unique
            good_id = None
            while not good_id:
                candidate_id = "".join(sample(lcLetters + ucLetters + digits, 8))
                if candidate_id not in generated_ids:
                    generated_ids.append(candidate_id)
                    good_id = candidate_id
            
            fn = choice(firstNames)
            ln = choice(lastNames)
            
            directory.invokeFactory(type_name="FSDPerson", id=good_id, firstName=fn, lastName=ln)
            
        return generated_ids

