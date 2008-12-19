from zope.interface import implements
from zope.component import adapts

from Products.FacultyStaffDirectory.interfaces.tree import ITree
from Products.FacultyStaffDirectory.interfaces.persongrouping import IPersonGrouping
from Products.FacultyStaffDirectory.interfaces.classification import IClassification
from Products.FacultyStaffDirectory.interfaces.committee import ICommittee
from Products.FacultyStaffDirectory.interfaces.department import IDepartment
from Products.FacultyStaffDirectory.interfaces.specialty import ISpecialty
                                                      

    
def personGroupingTree(context):
    """ build a tree of all person groupings starting from the adapted object
    """

def classificationTree(context):
    """ build a tree of all classifications starting from the adapted object
    """
    
    
#     
#     
# class CommitteeTree(PersonGroupingTree):
#     """ build a tree of all committees starting from the adapted object
#     """
#     implements(ITree)
#     adapts(ICommittee)
#     
# class DepartmentTree(PersonGroupingTree):
#     """ build a tree of all departments starting from the adapted object
#     """
#     implements(ITree)
#     adapts(IDepartment)
#     
# class SpecialtyTree(PersonGroupingTree):
#     """ build a tree of all specialties starting from the adapted object
#     """
#     implements(ITree)
#     adapts(ISpecialty)
