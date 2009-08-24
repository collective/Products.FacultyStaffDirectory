# Feel free to reference localAdaptersAreSupported in your code. I promise not to move it for awhile.
try:
    from Products.CMFPlone.migrations import v3_0
except ImportError:  # This is Plone >= 3.0
    localAdaptersAreSupported = False
else:
    localAdaptersAreSupported = True


def installExtenderGloballyIfLocallyIsNotSupported(extenderClass, name):
    """If we're on a version of Plone that doesn't support local adapters, make it so merely putting the extender in the Products folder activates it across on all Plone sites."""
    if not localAdaptersAreSupported:
        from zope.component import provideAdapter
        provideAdapter(extenderClass, name=name)

def installExtender(portal, extenderClass, name, required=None, provided=None):
    """Register a schema extender with a Plone site."""
    # Register our extender as a local adapter at the root of the Plone site:
    sm = portal.getSiteManager()  # Local components are not per-container; they are per-sitemanager. It just so happens that every Plone site has a sitemanager. Hooray.
    #if not sm.queryUtility(interface, name=extenderName):  # Need something like this?
    sm.registerAdapter(extenderClass, required=required, provided=provided, name=name)
    return "Registered the extender at the root of the Plone site."

def uninstallExtender(portal, extenderClass, name, required=None, provided=None):
    """Unregister a schema extender so its effect is no longer seen on a particular Plone site."""
    sm = portal.getSiteManager()
    sm.unregisterAdapter(extenderClass, required=required, provided=provided, name=name)
    return "Removed the extender from the root of the Plone site."

def declareInstallRoutines(globals_, extenderClass, name):
    """Called from an extender's Install.py, makes the extender installable via the Add-on Products control panel if and only if we're on a version of Plone that support local adapters (Plone 3 or better).
    
    If this version doesn't support local adapters, installExtenderGloballyIfLocallyIsNotSupported() should kick in.
    
    If you want to do additional stuff on installation or uninstallation (like installing skin layers), don't call this; do what you have to do, and call installExtender() and uninstallExtender() yourself.
    """
    if localAdaptersAreSupported:
        def install(portal):
            installExtender(portal, extenderClass, name)
        globals_['install'] = install
        
        def uninstall(portal):
            uninstallExtender(portal, extenderClass, name)
        globals_['uninstall'] = uninstall
