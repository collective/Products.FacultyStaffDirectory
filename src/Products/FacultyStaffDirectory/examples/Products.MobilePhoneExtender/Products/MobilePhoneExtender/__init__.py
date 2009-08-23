from Products.FacultyStaffDirectory.extenderInstallation import installExtenderGloballyIfLocallyIsNotSupported

from Products.MobilePhoneExtender.person import YuppieExtender

installExtenderGloballyIfLocallyIsNotSupported(YuppieExtender, 'Products.MobilePhoneExtender')  # Put the name of your product here.
