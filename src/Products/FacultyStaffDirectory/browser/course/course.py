from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class CourseView(BrowserView):
    """ basic code for viewing a course
    """
    
    def listing(self):
        context = self.context
        
        title = context.Title()
        number = context.getNumber()
        abbr = context.getAbbreviation() 
        suff = context.getSuffix()
        
        if suff:
            abbr = abbr + " " + suff
        
        out = number + " " + title
        if abbr:
            out = out + " (" + abbr + ")"
            
        return out
        
        