from Products.FacultyStaffDirectory.extenderInstallation import installExtenderGloballyIfLocallyIsNotSupported

from Products.FacultyStaffDirectoryExtenderDas.person import YuppieExtender # Put the name of your product here.

installExtenderGloballyIfLocallyIsNotSupported(YuppieExtender, 'FacultyStaffDirectoryExtenderDas')  # Put the name of your product here.
