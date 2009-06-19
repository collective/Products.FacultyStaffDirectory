from plone.app.layout.viewlets.common import ViewletBase        


class EmailViewlet(ViewletBase):

    def update(self):
        self.email = self.context.getEmail()
        
    def mungedEmail(self):
        return self.context.spamProtectFSD(self.email)
    