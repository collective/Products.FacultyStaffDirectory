from zope.interface import implements
from zope.component import adapts

from Products.FacultyStaffDirectory.interfaces import IPersonGrouping, ITree
                                                      

    
def personGroupingTree(context):
    """Build a tree of all person groupings starting from the adapted object"""
