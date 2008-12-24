from Products.FacultyStaffDirectory.interfaces import IConfiguration

def configuration(context):
    """Given an ISiteRoot, return an IConfiguration implementer."""
    return context.getSiteManager().getUtility(IConfiguration)
