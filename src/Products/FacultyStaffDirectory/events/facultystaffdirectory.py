
def addDefaultContent(self, event):
    """Actions to perform after a FacultyStaffDirectory is added to a Plone site"""
    # Create some default content
    # Create some base classifications
    self.invokeFactory('FSDPersonGrouping', id='faculty', title='Faculty')
    self.invokeFactory('FSDPersonGrouping', id='staff', title='Staff')
    self.invokeFactory('FSDPersonGrouping', id='grad-students', title='Graduate Students')
    