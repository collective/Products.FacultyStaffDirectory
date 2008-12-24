from plone.app.controlpanel.form import ControlPanelForm
from plone.fieldsets.fieldsets import FormFieldsets
from Products.FacultyStaffDirectory.interfaces import IGeneralConfiguration, IMembershipConfiguration
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('FacultyStaffDirectory')

general_fieldset = FormFieldsets(IGeneralConfiguration)
general_fieldset.id = 'fsd_general'
general_fieldset.label = _(u'label_fsd_general', default=u'General')

membership_fieldset = FormFieldsets(IMembershipConfiguration)
membership_fieldset.id = 'fsd_membership'
membership_fieldset.label = _(u'label_fsd_membership', default=u'Membership')

class ConfigurationForm(ControlPanelForm):
	form_fields = FormFieldsets(general_fieldset, membership_fieldset)
	form_name = label = _(u"Faculty/Staff Directory settings")
	description = None  # crashes if this isn't here
