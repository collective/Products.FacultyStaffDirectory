from zope.configuration.fields import MessageID
from zope.schema import TextLine
from zope.viewlet.metadirectives import IViewletDirective
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('FacultyStaffDirectory')

class IColumnarViewletDirective(IViewletDirective):

    column_heading = MessageID(
        title=_("Column heading"),
        description=u"""Heading for the column when this viewlet is displayed in a table""",
        required=False)

    column_css_classes = TextLine(
        title=_("CSS classes to be applied to the column's heading element (typically a <th>)"),
        description=u"""Heading for the column when this viewlet is displayed in a table""",
        required=False,
        default=u"""""")
