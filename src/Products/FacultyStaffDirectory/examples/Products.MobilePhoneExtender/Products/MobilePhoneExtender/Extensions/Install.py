from Products.FacultyStaffDirectory.extenderInstallation import declareInstallRoutines

from Products.MobilePhoneExtender.person import YuppieExtender

declareInstallRoutines(globals(), YuppieExtender, 'Products.MobilePhoneExtender')  # Put the name of your product here.
# If you need to do further things at installation, declare your own install() and uninstall() rather than using declareInstallRoutines(). Do what you need to, and also call extenderInstallation.installExtender() (and uninstallExtender(), respectively) if extenderInstallation.localAdaptersAreSupported is True.