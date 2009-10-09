from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes.atapi import *
from zope.interface import implements, Interface
from zope.component import adapts, provideAdapter

from Products.FacultyStaffDirectory.interfaces.person import IPerson


# Any field you tack on must have ExtensionField as its first subclass:
class _StringExtensionField(ExtensionField, StringField):
    pass


class PersonExtender(object):
    """Adapter that adds a Mobile Phone field to Person.
    
    You could also change or delete existing fields (though you might violate assumptions made in other code). To do that, implement ISchemaModifier instead of ISchemaExtender.
    """
    adapts(IPerson)
    implements(ISchemaExtender)
    
    _fields = [
            _StringExtensionField('mobilePhone',
                required=False,
                searchable=True,
                schemata="Contact Information",
                widget=StringWidget(
                    label=u"Mobile Phone",
                    description=u"Demo field added by the MobilePhoneExtender product.",
                )
            )
        ]
    
    def __init__(self, context):
        self.context = context
    
    def getFields(self):
        return self._fields


# # Optional stuff to tack on more methods to Person (after you adapt it to IYuppie, anyway):
# 
# class IYuppie(Interface):
#     """A Yuppie is any person who eats tofu and has a mobile phone."""
#     
#     def textMessage(self, spam):
#         """Text message some spam to the yuppie's mobile phone."""
# 
# 
# class YuppieAdapter(object):
#     """Adapt Persons to Yuppies."""
#     adapts(IPerson)
#     implements(IYuppie)
#     
#     def __init__(self, context):
#         self.context = context  # Phillip Weitershausen says this is canonical.
#     
#     def textMessage(self, spam):
#         print "I just texted %s to the yuppie's mobile phone at %s!" % (spam, self.context.getMobilePhone())
# 
# provideAdapter(YuppieAdapter)  # This should be in ZCML. Yuck.
