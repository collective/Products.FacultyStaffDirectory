from Products.Five.browser import BrowserView
from zope.interface import Interface

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

    def getKssClasses(self, field_name, template, macro):
        kss = self.getKssView()

        # choose appropriate kss class generator depending on rendering mode
        if self.request.get('URL').endswith('/replaceField'):
            f = kss.getKssClasses
        else:
            f = kss.getKssClassesInlineEditable
        
        editing_classes = f(field_name,
                            templateId=template,
                            macro=macro,
                            target="%s-%s" % (self.getUniqueIdentifier(), field_name))
        uid_class = kss.getKssUIDClass()
        return editing_classes + " " + uid_class
