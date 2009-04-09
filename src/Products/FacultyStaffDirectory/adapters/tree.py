from zope.interface import implements
from zope.component import adapts

from Products.FacultyStaffDirectory.interfaces import IPersonGrouping, IClassification, ICommittee, ISpecialty, ITree
                                                      

    
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
# class SpecialtyTree(PersonGroupingTree):
#     """ build a tree of all specialties starting from the adapted object
#     """
#     implements(ITree)
#     adapts(ISpecialty)
