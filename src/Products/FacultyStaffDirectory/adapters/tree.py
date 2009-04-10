from zope.interface import implements
from zope.component import adapts

from Products.FacultyStaffDirectory.interfaces import IPersonGrouping, IClassification, ITree
                                                      

    
def personGroupingTree(context):
    """build a tree of all person groupings starting from the adapted object"""

def classificationTree(context):
    """build a tree of all classifications starting from the adapted object"""
