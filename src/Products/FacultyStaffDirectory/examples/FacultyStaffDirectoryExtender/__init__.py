from Products.FacultyStaffDirectory.extenderInstallation import installExtenderGloballyIfLocallyIsNotSupported

from Products.FacultyStaffDirectoryExtender.person import YuppieExtender

installExtenderGloballyIfLocallyIsNotSupported(YuppieExtender, 'FacultyStaffDirectoryExtender')  # Put the name of your product here.