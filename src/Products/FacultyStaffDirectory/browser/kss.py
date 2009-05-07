from Products.Five.browser import BrowserView
from zope.interface import Interface
from zope.component import queryMultiAdapter
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class IKSSHelper(Interface):
    def getUniqueIdentifier():
        pass

    def getKssView():
        pass

    def getKssClasses(field_name):
        pass

class KSSHelper(BrowserView):
    """To better support various Plone environments we implement
    this view to help generate the right inline-editing bindings."""

    

    def getUniqueIdentifier(self):
        return self.context.UID()
        
    def getKssView(self):
        return self.context.restrictedTraverse('@@kss_field_decorator_view')

    def getKssClasses(self, field_name, templateId, macro, target=None):
        kss = self.getKssView()
        # person = self.context.aq_base
        # format = self.context.format.aq_base
        # grouping = self.context.grouping.aq_base
        # vw = queryMultiAdapter((person, grouping, format, self.request), name='view')
        # vw = vw.__of__(self.context)
        import pdb; pdb.set_trace( )
        # # choose appropriate kss class generator depending on rendering mode
        if self.request.get('URL').endswith('/replaceField'):
            f = kss.getKssClasses
        else:
            f = kss.getKssClassesInlineEditable
        editing_classes = f(field_name,
                            templateId='templateWrapper/widgets/string',
                            macro=macro,
                            target="%s-%s" % (self.getUniqueIdentifier(), field_name))
        uid_class =  kss.getKssUIDClass()
        return editing_classes + " " + uid_class

    def getKssClassesInlineEditable(self, fieldname, templateId, macro=None, target=None):
        classstring = self.getKssClasses(fieldname, templateId, macro, target)
        global_kss_inline_editable = self.getKssView()._global_kss_inline_editable()
        if global_kss_inline_editable and classstring:
            classstring += ' inlineEditable'
        return classstring

class templateWrapper(BrowserView):
    
    @property
    def __call__(self):
        view = queryMultiAdapter((self.context.staff, self.request), name='tabular')
        return view.index
        # # # return self.context.aq_inner.aq_parent.render
        # This is where we'd look up the particular viewlet, based on person, grouping, and format.

from archetypes.kss.fields import FieldsView
class PersonFieldsView(FieldsView):
    view_field_wrapper = ZopeTwoPageTemplateFile('person/view_field_wrapper.pt')
    edit_field_wrapper = ZopeTwoPageTemplateFile('person/edit_field_wrapper.pt')
    
    @property
    def __call__(self):
        import pdb; pdb.set_trace( )
        
    def getTemplate(self, templateId, context=None):
        """
        traverse/search template
        """
        import pdb; pdb.set_trace( )
        if not context:
            context = self.context
        template = context.restrictedTraverse(templateId)
        
        if IBrowserView.providedBy(template):
            view = template
            for attr in ('index', 'template', '__call__'):
                template = getattr(view, attr, None)
                if template is not None and hasattr(template, 'macros'):
                    break
            if template is None:
                raise KeyError("Unable to find template for view %s" % templateId)
        return template    
    
    def replaceField(self, fieldname, templateId, macro, uid=None, target=None, edit=False):
        FieldsView.replaceField(self, fieldname, templateId, macro, uid=uid, target=target, edit=edit)
        return self.render()

    def replaceWithView(self, fieldname, templateId, macro, uid=None, target=None, edit=False):
        FieldsView.replaceWithView(self, fieldname, templateId, macro, uid=uid, target=target, edit=edit)
        return self.render()
    
    def saveField(self, fieldname, value=None, templateId=None, macro=None, uid=None, target=None):
        FieldsView.saveField(self, fieldname,
                value = value,
                templateId = templateId,
                macro = macro,
                uid = uid,
                target = target,
                )
        return self.render()