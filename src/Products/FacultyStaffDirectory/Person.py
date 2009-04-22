# -*- coding: utf-8 -*-

__author__ = """WebLion <support@weblion.psu.edu>"""
__docformat__ = 'plaintext'

from cStringIO import StringIO
import logging
import re
from sha import sha

from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner, aq_parent
from DateTime import DateTime
from zope.app.annotation.interfaces import IAttributeAnnotatable, IAnnotations
from zope.component import getUtility
from zope.event import notify
from zope.interface import implements, classImplements, alsoProvides
from Products.Archetypes.atapi import *
from Products.ATContentTypes.content.base import ATCTContent
from Products.ATContentTypes.content.schemata import ATContentTypeSchema, finalizeATCTSchema
from Products.ATContentTypes.lib.calendarsupport import n2rn, foldLine
from Products.CMFCore.permissions import View, ModifyPortalContent, SetOwnPassword, SetOwnProperties
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import buildFolderTree
from Products.CMFPlone.CatalogTool import getObjPositionInParent
from Products.membrane.interfaces import IUserAuthProvider, IPropertiesProvider, IGroupsProvider, IGroupAwareRolesProvider, IUserChanger
from Products.validation import validation
from ZPublisher.HTTPRequest import HTTPRequest

from Products.FacultyStaffDirectory.config import *
from Products.FacultyStaffDirectory.interfaces import IPerson, IConfiguration, IPersonModifiedEvent, IPersonToPersonGroupingRelationship
from Products.FacultyStaffDirectory.permissions import MANAGE_GROUP_MEMBERSHIP, CHANGE_PERSON_IDS
from Products.FacultyStaffDirectory.validators import SequenceValidator
from Products.FacultyStaffDirectory.AssociationContent import AssociationContent

from plonerelations.ATField.ploneRelationsATField import PloneRelationsATField
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from plone.app.relations.interfaces import IAnnotationsContext, IRelationshipSource
from plone.relations.interfaces import IContextAwareRelationship

logger = logging.getLogger('FacultyStaffDirectory')

schema = ATContentTypeSchema.copy() + Schema((
    
    StringField(
        name='firstName',
        widget=StringWidget(
            label=u"First Name",
            label_msgid='FacultyStaffDirectory_label_firstName',
            i18n_domain='FacultyStaffDirectory',
        ),
        required=True,
        schemata="Basic Information",
        searchable=True
    ),
    
    StringField(
        name='middleName',
        widget=StringWidget(
            label=u"Middle Name",
            label_msgid='FacultyStaffDirectory_label_middleName',
            i18n_domain='FacultyStaffDirectory',
        ),
        required=False,
        schemata="Basic Information",
        searchable=True
    ),
    
    StringField(
        name='lastName',
        widget=StringWidget(
            label=u"Last Name",
            label_msgid='FacultyStaffDirectory_label_lastName',
            i18n_domain='FacultyStaffDirectory',
        ),
        required=True,
        schemata="Basic Information",
        searchable=True
    ),
    
    StringField(
        name='suffix',
        widget=StringWidget(
            label=u"Suffix",
            description="Academic, professional, honorary, and social suffixes.",
            label_msgid='FacultyStaffDirectory_label_suffix',
            description_msgid='FacultyStaffDirectory_description_suffix',
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Basic Information",
        searchable=True
    ),
    
    StringField(
        name='email',
        user_property=True,
        widget=StringWidget(
            label=u'Email',
            label_msgid='FacultyStaffDirectory_label_email',
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Contact Information",
        searchable=True,
        validators=('isEmail',)
    ),
    
    LinesField(
        name='jobTitles',
        widget=LinesField._properties['widget'](
            label=u"Job Titles",
            description="One per line",
            label_msgid='FacultyStaffDirectory_label_jobTitles',
            description_msgid='FacultyStaffDirectory_description_jobTitles',
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Professional Information",
        searchable=True
    ),
    
    StringField(
        name='officeAddress',
        widget=TextAreaWidget(
            label=u"Office Street Address",
            label_msgid='FacultyStaffDirectory_label_officeAddress',
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Contact Information",
        searchable=True
    ),
    
    StringField(
        name='officeCity',
        widget=StringWidget(
            label=u"Office City",
            label_msgid='FacultyStaffDirectory_label_officeCity',
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Contact Information",
        searchable=True
    ),
    
    StringField(
        name='officeState',
        widget=StringWidget(
            label=u"Office State",
            label_msgid='FacultyStaffDirectory_label_officeState',
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Contact Information"
    ),
    
    StringField(
        name='officePostalCode',
        widget=StringWidget(
            label=u"Office Postal Code",
            label_msgid='FacultyStaffDirectory_label_officePostalCode',
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Contact Information"
    ),
    
    StringField(
        name='officePhone',
        widget=StringWidget(
            label=u"Office Phone",
            description="",
            label_msgid='FacultyStaffDirectory_label_officePhone',
            description_msgid='FacultyStaffDirectory_description_officePhone',
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Contact Information",
        searchable=True,
    ),
    
    ImageField(
        name='image',
        schemata="Basic Information",
        widget=ImageWidget(
            label=u'Image',
            label_msgid='FacultyStaffDirectory_label_image',
            i18n_domain='FacultyStaffDirectory',
            default_content_type='image/gif',
        ),
        storage=AttributeStorage(),
        original_size=(400, 500),
        sizes={'thumb': (100, 125), 'normal': (200, 250)},
        default_output_type='image/jpeg',
        allowable_content_types=('image/gif','image/jpeg','image/png'),
    ),
    
    TextField(
        name='biography',
        allowable_content_types=ALLOWABLE_CONTENT_TYPES,
        widget=RichWidget(
            label=u'Biography',
            label_msgid='FacultyStaffDirectory_label_biography',
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Professional Information",
        searchable=True,
        validators=('isTidyHtmlWithCleanup',),
        default_output_type='text/x-html-safe',
        user_property='description'
    ),
    
    LinesField(
        name='education',
        widget=LinesField._properties['widget'](
            label=u'Education',
            label_msgid='FacultyStaffDirectory_label_education',
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Professional Information",
        searchable=True
    ),
    
    LinesField(
        name='websites',
        widget=LinesField._properties['widget'](
            label=u"Web Sites",
            description="One per line. Example: http://www.example.com/",
            label_msgid='FacultyStaffDirectory_label_websites',
            description_msgid='FacultyStaffDirectory_description_websites',
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Professional Information",
        validators = SequenceValidator('isURLs', validation.validatorFor('isURL'))
    ),
    
    StringField(
        name='id',
        widget=StringWidget(
            description=u"Example: abc123",
            label=u"Access Account ID",
            label_msgid='FacultyStaffDirectory_label_id',
            description_msgid='FacultyStaffDirectory_description_id',
            i18n_domain='FacultyStaffDirectory',
        ),
        required=True,
        user_property=True,
        schemata="Basic Information",
        write_permission=CHANGE_PERSON_IDS,
    ),
    
    ComputedField(
        name='title',
        widget=ComputedField._properties['widget'](
            label=u"Full Name",
            visible={'edit': 'invisible', 'view': 'visible'},
            label_msgid='FacultyStaffDirectory_label_fullName',
            i18n_domain='FacultyStaffDirectory',
        ),
        schemata="Basic Information",
        accessor="Title",
        user_property='fullname',
        searchable=True
    ),
    
    StringField('password',
        languageIndependent=True,
        required=False,
        mode='w',
        write_permission=SetOwnPassword,
        widget=PasswordWidget(
            label=u'Password',
            description=u"Password for this person " \
                         "(Leave blank if you don't want to change the password.)",
            label_msgid='FacultyStaffDirectory_label_password',
            description_msgid='FacultyStaffDirectory_description_password',
            i18n_domain='FacultyStaffDirectory',
            condition="python:portal.restrictedTraverse('++fsdmembership++snork').useInternalPassword and 'FSDPerson' in portal.restrictedTraverse('++fsdmembership++snork').enableMembraneTypes"
        ),
        schemata="Basic Information",
    ),
    
    StringField('confirmPassword',
        languageIndependent=True,
        required=False,
        mode='w',
        write_permission=SetOwnPassword,
        widget=PasswordWidget(
            label=u'Confirm password',
            description=u"Please re-enter the password. " \
                         "(Leave blank if you don't want to change the password.)",
            label_msgid='FacultyStaffDirectory_label_confirmPassword',
            description_msgid='FacultyStaffDirectory_description_confirmPassword',
            i18n_domain='FacultyStaffDirectory',
            condition="python:portal.restrictedTraverse('++fsdmembership++snork').useInternalPassword and 'FSDPerson' in portal.restrictedTraverse('++fsdmembership++snork').enableMembraneTypes"
        ),
        schemata="Basic Information",
    ),
    
    StringField('userpref_language',
        widget=SelectionWidget(
            label=u"Language",
            label_msgid="label_language",
            description=u"Your preferred language.",
            description_msgid="help_preferred_language",
            i18n_domain='plone',
            condition="python:'FSDPerson' in portal.restrictedTraverse('++fsdmembership++snork').enableMembraneTypes"
        ),
        write_permission=SetOwnProperties,
        schemata="User Settings",
        vocabulary="_availableLanguages",
        user_property='language',
    ),
    
    StringField('userpref_wysiwyg_editor',
        widget=SelectionWidget(
            label=u"Content editor",
            label_msgid="label_content_editor",
            description=u"Select the content editor that you would like to use. Note that content editors often have specific browser requirements.",
            description_msgid="help_content_editor",
            i18n_domain='plone',
            format="select",
            condition="python:'FSDPerson' in portal.restrictedTraverse('++fsdmembership++snork').enableMembraneTypes"
        ),
        write_permission=SetOwnProperties,
        schemata="User Settings",
        vocabulary="_availableEditors",
        user_property='wysiwyg_editor',
    ),
    
    BooleanField('userpref_ext_editor',
        widget=BooleanWidget(
            label=u"Enable external editing",
            label_msgid="label_ext_editor",
            description=u"When checked, an icon will be made visible on each page which allows you to edit content with your favorite editor instead of using browser-based editors. This requires an additional application called ExternalEditor installed client-side. " \
                         "Ask your administrator for more information if needed.",
            description_msgid="help_content_ext_editor",
            i18n_domain='plone',
            condition="python:here.portal_properties.site_properties.ext_editor and 'FSDPerson' in portal.restrictedTraverse('++fsdmembership++snork').enableMembraneTypes",
            ),
            write_permission=SetOwnProperties,
            schemata="User Settings",
            user_property='ext_editor',
    ),
    
    StringField('userpref_portal_skin',
        widget=SelectionWidget(
            label=u"Look",
            label_msgid="label_look",
            description=u"Appearance of the site.",
            description_msgid="help_look",
            i18n_domain='plone',
            format="select",
            condition="python:here.portal_skins.allow_any and 'FSDPerson' in portal.restrictedTraverse('++fsdmembership++snork').enableMembraneTypes",
        ),
        write_permission=SetOwnProperties,
        schemata="User Settings",
        vocabulary="_skinSelections",
        user_property='look',
    ),
    
    BooleanField('userpref_invisible_ids',
        widget=BooleanWidget(
            label=u"Allow editing of Short Names",
            label_msgid="label_edit_short_names",
            description=u"Determines if Short Names (also known as IDs) are changable when editing items. If Short Names are not displayed, they will be generated automatically.",
            description_msgid="help_display_names",
            i18n_domain='plone',
            condition="python:here.portal_properties.site_properties.visible_ids and 'FSDPerson' in portal.restrictedTraverse('++fsdmembership++snork').enableMembraneTypes"
            ),
            write_permission=SetOwnProperties,
            schemata="User Settings",
            user_property='invisible_ids',
    ),
    
    PloneRelationsATField(
        name='assistants',
        widget=ReferenceBrowserWidget
        (
            label=u'Personal Assistant(s)',
            label_msgid='FacultyStaffDirectory_label_assistants',
            i18n_domain='FacultyStaffDirectory',
            base_query={'portal_type': 'FSDPerson', 'sort_on': 'sortable_title'},
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1,
        ),
        write_permission="Modify portal content",
        schemata="Basic Information",
        multiValued=True,
        relationship='hasAssistant',
        allowed_types=('FSDPerson'),
    ),
    
    PloneRelationsATField(
        name='groupings',
        widget=ReferenceBrowserWidget
        (
            label=u'Group Associations',
            label_msgid='FacultyStaffDirectory_label_groupassocations',
            i18n_domain='FacultyStaffDirectory',
            base_query={'portal_type': 'FSDPersonGrouping', 'sort_on': 'sortable_title'},
            allow_browse=0,
            allow_search=1,
            show_results_without_query=1,
        ),
        # write_permission=ASSIGN_GOUPINGS_TO_PEOPLE,
        schemata="Basic Information",
        allowed_types=('FSDPersonGrouping'),
        multiValued=True,
        relationship='PersonGroupingAssociation',
        relationship_interface=IPersonToPersonGroupingRelationship,
        ),
    ))

Person_schema = OrderedBaseFolderSchema.copy() + schema.copy()  # + on Schemas does only a shallow copy

finalizeATCTSchema(Person_schema, folderish=True)

class PersonModifiedEvent(object):
    """Event that happens when edits to a Person have been saved"""
    implements(IPersonModifiedEvent)
    
    def __init__(self, context):
        self.context = context

class Person(OrderedBaseFolder, ATCTContent):
    """A person in the Faculty/Staff directory"""
    meta_type = portal_type = "FSDPerson"
    security = ClassSecurityInfo()
    __implements__ = (ATCTContent.__implements__, getattr(OrderedBaseFolder,'__implements__', ()),)
    # zope3 interfaces
    implements(IPerson,
               IUserAuthProvider,
               IPropertiesProvider,
               IGroupsProvider,
               IGroupAwareRolesProvider,
               IAttributeAnnotatable,
               IUserChanger)
    
    # moved schema setting after finalizeATCTSchema, so the order of the fieldsets
    # is preserved. Also after updateActions is called since it seems to overwrite the schema changes.
    # Move the description field, but not in Plone 2.5 since it's already in the metadata tab. Although,
    # decription and relateditems are occasionally showing up in the "default" schemata. Move them
    # to "metadata" just to be safe.
    if 'categorization' in Person_schema.getSchemataNames():
        Person_schema.changeSchemataForField('description', 'settings')
    else:
        Person_schema.changeSchemataForField('description', 'metadata')
        Person_schema.changeSchemataForField('relatedItems', 'metadata')
    
    _at_rename_after_creation = True
    schema = Person_schema
    # Methods
    security.declareProtected(View, 'at_post_create_script')
    def at_post_create_script(self):
        """Notify that the Person has been modified."""
        notify(PersonModifiedEvent(self))

    security.declareProtected(View, 'at_post_edit_script')
    def at_post_edit_script(self):
        """Notify that the Person has been modified."""
        notify(PersonModifiedEvent(self))
    
    def __call__(self, *args, **kwargs):
        return self.getId()
    
    security.declareProtected(View, 'vcard_view')
    def vcard_view(self, REQUEST, RESPONSE):
        """vCard 3.0 output"""
        RESPONSE.setHeader('Content-Type', 'text/x-vcard')
        RESPONSE.setHeader('Content-Disposition', 'attachment; filename="%s.vcf"' % self.getId())
        out = StringIO()
        
        # Get the fields using the accessors, so they're properly Unicode encoded.
        out.write("BEGIN:VCARD\nVERSION:3.0\n")
        out.write("FN:%s\n" % self.Title())
        out.write("N:%s;%s\n" % (self.getLastName(), self.getFirstName()))
        out.write(foldLine("TITLE:%s\n" % '\\n'.join(self.getJobTitles())))
        out.write(foldLine("ADR;TYPE=dom,postal,parcel,work:;;%s;%s;%s;%s\n" % (self.getOfficeAddress().replace('\r\n','\\n'), self.getOfficeCity(), self.getOfficeState(), self.getOfficePostalCode())))
        out.write("TEL;WORK:%s\n" % self.getOfficePhone())
        out.write("EMAIL;TYPE=internet:%s\n" % self.getEmail())
        
        #Add the Person page to the list of URLs
        urls = list(self.getWebsites())
        urls.append(self.absolute_url())
        for url in urls:
            out.write(foldLine("URL:%s\n" % url))
        if self.getImage():
            encData = self.image_thumb.data.encode('base-64')
            # indent the data block:
            indentedData = '\n  '.join(encData.strip().split('\n'))
            out.write("PHOTO;ENCODING=BASE64;TYPE=JPEG:\n  %s\n" % indentedData)
        out.write("REV:%s\n" % DateTime(self.ModificationDate()).ISO8601())
        out.write("PRODID:WebLion Faculty/Staff Directory\nEND:VCARD")
        return n2rn(out.getvalue())
    
    security.declareProtected(View, 'getSortableName')
    def getSortableName(self):
        """Return a tuple of the person's name for sorting purposes, as lowercase so that names like 'von Whatever' sort properly."""
        return (self.lastName.lower(), self.firstName.lower())
    
    security.declareProtected(View, 'Title')
    def Title(self):
        """Return the Title as firstName middleName(when available) lastName, suffix(when available)"""
        try:
            # Get the fields using the accessors, so they're properly Unicode encoded.
            # We also can't use the %s method of string concatentation for the same reason.
            # Is there another way to manage this?
            fn = self.getFirstName()
            ln = self.getLastName()
        except AttributeError:
            return u"new person" # YTF doesn't this display on the New Person page?  # Couldn't call superclass's Title() for some unknown reason
        
        if self.getMiddleName():
            mn = " " + self.getMiddleName() + " "
        else:
            mn = " "
        
        t = fn + mn + ln
        if self.getSuffix():
            t = t + ", " + self.getSuffix()
        
        return t
    
    security.declarePrivate('_availableEditors')
    def _availableEditors(self):
        """Return a list of the available WYSIWYG editors for the site."""
        props = getToolByName(self, 'portal_properties')
        return props['site_properties'].available_editors
    
    security.declarePrivate('_availableLanguages')
    def _availableLanguages(self):
        """Return a list of the available languages for the site."""
        props = getToolByName(self, 'portal_properties')
        return props.availableLanguages()
    
    security.declarePrivate('_skinSelections')
    def _skinSelections(self):
        """Return a list of the available skins for the site."""
        skins = getToolByName(self, 'portal_skins')
        return skins.getSkinSelections()
    
    security.declareProtected(View, 'getCourses')
    def getCourses(self):
        """Return a listing of Courses contained by this Person."""
        portal_catalog = getToolByName(self, 'portal_catalog')
        return portal_catalog(path='/'.join(self.getPhysicalPath()), portal_type='FSDCourse', depth=1, sort_on="getObjPositionInParent")
    
    # security.declareProtected(View, 'getClassificationNames')
    # def getClassificationNames(self):
    #     """Return a list of the titles of the classifications attached to this person.
    #     
    #     Mainly used for pretty-looking metadata in SmartFolder tables.
    #     
    #     """
    #     cList = [(getObjPositionInParent(c)+1, c.Title()) for c in self.getClassifications()]
    #     cList.sort()
    #     return [c[-1] for c in cList]
    
    # security.declareProtected(View, 'getSpecialtyTree')
    # def getSpecialtyTree(self):
    #     """Return a tree-shaped dict of catalog brains of this person's specialties. The topmost level of the tree consists of SpecialtiesFolders; the remainder, of Specialties.
    #     
    #     The format of the dict is a superset of what buildFolderTree() returns (see its docstring for details). Consequently you can use a recursive macro similar to portlet_navtree_macro to render the results.
    #     
    #     Even if a person is mapped to a specialty but not to a superspecialty of it, the superspecialty will be returned. However, it will lack a 'reference' key, where explicitly mapped specialties will have one set to the reference from the Person to the Specialty. (All SpecialtiesFolders also lack 'reference' keys.) Thus, the template author can decide whether to consider people to implicitly belong to superspecialties of their explicitly mapped specialties, simply by deciding how to present the results.
    #     """
    #     def buildSpecialtiesFolderTree():
    #         """Return a buildFolderTree-style tree representing every SpecialtiesFolder and its descendents.
    #         
    #         More specifically, do a buildFolderTree for each SpecialtiesFolder, then merge the results into one big tree.
    #         """
    #         portal_catalog = getToolByName(self, 'portal_catalog')
    #         tree = {'children': []}
    #         for specialtiesFolder in portal_catalog(portal_type='FSDSpecialtiesFolder'):
    #             subtree = buildFolderTree(self, query={'path': {'query': specialtiesFolder.getPath()}, 'portal_type': 'FSDSpecialty'})
    #             subtree['currentItem'] = False
    #             subtree['currentParent'] = False
    #             subtree['item'] = specialtiesFolder
    #             subtree['depth'] = 0  # Let's see if that drives the stylesheets crazy. Otherwise, I'm going to have to increment the 'depth' keys in the whole rest of the tree.
    #             tree['children'].append(subtree)
    #         return tree
    #     
    #     # Walk the tree, killing everything not in reffedUids, except for the ancestors of reffed things.
    #     reffedUids = dict([(ref.targetUID, ref) for ref in getToolByName(self, 'reference_catalog').getReferences(self, relationship='people_specialties')])
    #     def pruneUnreffed(tree):
    #         """Prune all subtrees from `tree` where no descendent is in `reffedUids`. Return whether `tree` itself should be pruned off. While we're at it, add 'reference' keys."""
    #         keptChildren = []
    #         for child in tree['children']:
    #             if not pruneUnreffed(child):  # If that child shouldn't be completely pruned away,
    #                 keptChildren.append(child)  # keep it.
    #         tree['children'] = keptChildren
    #         
    #         if 'item' in tree:  # 'item' is not in the root node.
    #             try:
    #                 ref = reffedUids.get(tree['item'].UID)
    #             except TypeError:
    #                 # Catch the 'unhashable type' error we're getting in rare cases (seems to be mostly on uninstall/reinstall when catalog reindexing goes awry).
    #                 ref = reffedUids.get(tree['item'].getObject().UID())
    #             if ref:
    #                 tree['reference'] = ref
    #                 return False  # I don't care if you pruned all my children off. I myself am reffed, so I'm staying.
    #         return not keptChildren  # My children are the only thing keeping me here. Prune me if there aren't any. (Sounds so dramatic, doesn't it?)
    #     
    #     tree = buildSpecialtiesFolderTree()
    #     pruneUnreffed(tree)
    #     return tree
    
    # security.declareProtected(View, 'getSpecialties')
    # def getSpecialties(self):
    #     """Return an iterable of tuples representing the specialties explicitly attached to this person. The first item of the tuple is a catalog brain of a specialty; the second, the reference pointing from the Person to the Specialty.
    #     
    #     Results are ordered by the position of the specialties in their containers (SpecialtiesFolders or other Specialties) and by the order of SpecialtiesFolders themselves if there is more than one.
    #     
    #     To get a Specialties object from a result, call result.getTargetObject(). To get a SpecialtyInformation object, call result.getContentObject().
    #     """
    #     items = []
    #     def depthFirst(tree):
    #         """Append, in depth-first pre order, a tuple of ('item' value, 'reference' value) from `tree` for every node that has a 'reference' value."""
    #         if 'reference' in tree:
    #             items.append((tree['item'], tree['reference']))  # There's always an 'item' key where there's a 'reference' key. How can you have a reference if there's no item to reference?
    #         for child in tree['children']:
    #             depthFirst(child)
    #     depthFirst(self.getSpecialtyTree())
    #     return items
    # 
    # security.declareProtected(View, 'getSpecialtyNames')
    # def getSpecialtyNames(self):
    #     """Return a list of the titles of the specialties explicitly attached to this person.
    #     
    #     Results are ordered as in getSpecialties().
    #     
    #     Mainly used for pretty-looking metadata in SmartFolder tables.
    #     """
    #     return [x.Title for x, _ in self.getSpecialties()]
    
    # security.declareProtected(View, 'getResearchTopics')
    # def getResearchTopics(self):
    #     """Return a list of the research topics of the specialties explicitly attached to this person.
    #     
    #     Results are ordered as in getSpecialties(). Specialties whose references have no content object (which doesn't happen) or where the content object has an empty research topic are omitted.
    #     
    #     Mainly used for pretty-looking metadata in SmartFolder tables.
    #     """
    #     topics = []
    #     for _, ref in self.getSpecialties():
    #         refContent = ref.getContentObject()  # TODO: probably slow: wakes up all those SpecialtyInformation objects
    #         if refContent:  # This is usually true, because reference-dwelling objects are always created when the reference is created. However, it's false sometimes; run testSpecialties for an example.
    #             researchTopic = refContent.getResearchTopic()
    #             if researchTopic:
    #                 topics.append(researchTopic)
    #     return topics
    
    # security.declareProtected(View, 'getCommitteeNames')
    # def getCommitteeNames(self):
    #     """Returns a list of the titles of the committees attached to this person.
    #         Mainly used for pretty-looking metadata in SmartFolder tables. Returns an
    #         alphabetically-sorted list since Committees can be located throughout the site,
    #         which makes using any other sort order somewhat problematic.
    #     """
    #     dList = [d.Title() for d in self.getCommittees()]
    #     dList.sort()
    #     return dList
    
    security.declareProtected(ModifyPortalContent, 'pre_edit_setup')
    def pre_edit_setup(self):
        """I hate myself for doing this, but until we can get ReferenceBrowserWidget to accept proper relative paths (../../) or functions, this is what we get.
            
        Can't do it on __init__ since it doesn't recognize any of the portal tools for some reason.
        
        """
        # Set the startup directory for the specialties field to the SpecialtiesFolder or, failing
        # that, the root of the FacultyStaffDirectory:
        urlTool = getToolByName(self, 'portal_url')
        fsd = self.getDirectoryRoot()
        # if fsd and fsd.getSpecialtiesFolder():
        #     url = urlTool.getRelativeContentURL(fsd.getSpecialtiesFolder())
        # else:
        #     url = ""
        # self.schema['specialties'].widget.startup_directory = '/%s' % url
        
        fsd_utility = getUtility(IConfiguration)
        if fsd_utility.phoneNumberRegex:
            self.schema['officePhone'].widget.description = u"Example: %s" % fsd_utility.phoneNumberDescription
        if fsd_utility.idLabel:
            self.schema['id'].widget.label = u"%s" % fsd_utility.idLabel

        # Make sure the default for the editor field is the same as the site defaut. No idea why this isn't being handled properly.
        self.schema['userpref_wysiwyg_editor'].default = getToolByName(self, 'portal_memberdata').wysiwyg_editor
        
        return self.base_edit()
    
    security.declareProtected(View, 'tag')
    def tag(self, **kwargs):
        """Pass along the 'tag' method to the Person's image."""
        return self.getWrappedField('image').tag(self, **kwargs)
    
    security.declareProtected(View, 'getImageOfSize')
    def getImageOfSize(self, height, width, **kwargs):
        """Return the person's image sized to the given dimensions."""
        return self.getWrappedField('image').tag(self, width=width, height=height, **kwargs)
    
    security.declareProtected(View, 'getScaledImageByWidth')
    def getScaledImageByWidth(self, preferredWidth, **kwargs):
        """Return the person's image sized to the given width and a height scaled according to the original image ratio. Fail nicely, returning no image tag. This seems to occur when TIFF images are used."""
        if not (self.image.height or self.image.width):
            logger.error("There was an error resizing the image for person %s" % self)
            return ''
        hwratio = float(self.image.height)/float(self.image.width)
        calcHeight = int(preferredWidth * hwratio)
        return self.getImageOfSize(calcHeight, preferredWidth, **kwargs)
    
    security.declareProtected(ModifyPortalContent, 'setImage')
    def setImage(self, value, **kwargs):
        field = self.getField('image')
        
        # If the image exists in portal memberdata's portraits folder, delete it
        md = getToolByName(self, 'portal_memberdata')
        if md.portraits.has_key(self.id):
            md.portraits._delObject(self.id)
        
        # Assign the image to the field
        field.set(self, value)
        
        # If there is an image value (not the empty string that seems to get sent on object creation)
        # and it's not a delete command, create a member portrait
        if value and value != 'DELETE_IMAGE':
            # Add the new portrait
            md.portraits._setObject(id=self.id, object=self.getImage())
    
    security.declareProtected(SetOwnPassword, 'setPassword')
    def setPassword(self, value):
        """"""
        if value:
            annotations = IAnnotations(self)
            annotations[PASSWORD_KEY] = sha(value).digest()
    
    security.declareProtected(SetOwnPassword, 'setConfirmPassword')
    def setConfirmPassword(self, value):
        """"""
        # Do nothing - this value is used for verification only
        pass

    
    security.declarePrivate('validate_id')
    def validate_id(self, value):
        """Make sure the Person's ID jibes with the regex defined in the configlet and isn't a duplicate."""
        # Ensure the ID is unique in this folder:
        if value != self.getId():
            parent = aq_parent(aq_inner(self))
            if value in parent.objectIds():
                return "An object with ID '%s' already exists in this folder" % value
        
        # Make sure the ID fits the regex defined in the configuration:
        fsd_utility = getUtility(IConfiguration)
        if not re.match(fsd_utility.idRegex, value):
            return fsd_utility.idRegexErrorMessage
    
    security.declarePrivate('validate_officePhone')
    def validate_officePhone(self, value=None):
        """Make sure the phone number fits the regex defined in the configuration."""
        if value:
            fsd_utility = getUtility(IConfiguration)
            regexString = fsd_utility.phoneNumberRegex
            if regexString and not re.match(regexString, value):
                return "Please provide the phone number in the format %s" % fsd_utility.phoneNumberDescription

    
    security.declarePrivate('post_validate')
    def post_validate(self, REQUEST, errors):
        form = REQUEST.form
        if form.has_key('password') or form.has_key('confirmPassword'):
            password = form.get('password', None)
            confirm = form.get('confirmPassword', None)
            
            annotations = IAnnotations(self)
            passwordDigest = annotations.get(PASSWORD_KEY, None)
            
            if not passwordDigest:
                if not password and not confirm:
                    errors['password'] = u'An initial password must be set'
                    return
            if password or confirm:
                if password != confirm:
                    errors['password'] = errors['confirmPassword'] = u'Passwords do not match'


    security.declareProtected(View, 'getGroupingAssociationContent')
    def getGroupingAssociationContent(self, **kwargs):
        """ Get the AssocationContent objects attached to this person related to all PersonGroupings. 
            Keywords passed are included in the getRelationships lookup. Typically this would be a 
            target=, with the relevant object being passed.
        """
        source = IRelationshipSource(self)
        relationshipName = self.schema['groupings'].relationship
        contexts = []
        for relationship in source.getRelationships(relation=relationshipName, **kwargs):
            contexts.append(IContextAwareRelationship(relationship).getContext())
        return contexts
        
# # Implementing IMultiPageSchema forces the edit template to render in the more Plone 2.5-ish manner,
# with actual links at the top of the page instead of Javascript tabs. This allows us to direct people
# immediately to a specific fieldset with a ?fieldset=somethingorother query string. Plus, it also
# gives the next/previous links at the bottom of the form.
try:
    from Products.Archetypes.interfaces import IMultiPageSchema
except ImportError:
    # It doesn't exist, do nothing
    pass
else:
    classImplements(Person, IMultiPageSchema)

registerType(Person, PROJECTNAME)  # generates accessor and mutators, among other things
