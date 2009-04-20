from zope.configuration.fields import MessageID
from zope.schema import TextLine, Bool
from zope.viewlet.metadirectives import IViewletDirective
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('FacultyStaffDirectory')

class ITabularViewletDirective(IViewletDirective):

    table_heading = MessageID(
        title=_("Table heading"),
        description=u"""Heading for the column, row, or whatever when this viewlet is displayed in a table""",
        required=False)

    sortable = Bool(
        title=_("Sortable"),
        description=u"""Whether the user should be able to click-to-sort a table by this field""",
        required=True,
        default=True)
