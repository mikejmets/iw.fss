#Python imports
import logging

# Zope imports
from Products.Five import BrowserView
from zope.component import getUtility
from AccessControl import ClassSecurityInfo

try:
    from AccessControl.requestmethod import postonly
except ImportError:
    # For Zope <2.8.9, <2.9.7 and <2.10.3                                                           
    def postonly(func):
        return func

# Products imports
from Products.CMFCore.permissions import ManagePortal
from iw.fss.utils import FSSMessageFactory as _
from iw.fss.interfaces import IConf

class FSSView(BrowserView):
    
    security = ClassSecurityInfo()
    
    def __init__(self, context, request):
        super(FSSView, self).__init__(context, request)
        conf_class = getUtility(IConf, "globalconf")
        self.conf = conf_class()
        self.stats = self.conf.getFSStats()
         
    def mytry(self):
        return "OK"
    def rdf_enabled(self):
        return True
 
    def configletTabs(self, template_id):
        """Data for drawing tabs in FSS config panel"""

        tab_infos = [
            {'label': _(u'management_tab', default=u"Management"),
             'template': 'fss_management_form',
             'css_class': None},
            {'label': _(u'maintenance_tab', default=u"Maintenance"),
             'template': 'fss_maintenance_form',
             'css_class': None}
            ]
        for ti in tab_infos:
            if ti['template'] == template_id:
                ti['css_class'] = 'selected'
        return tab_infos
        
    def config_file(self):
        return self.conf.globalConfigInfo()['config_file']
    
    def storage_path(self):
        return self.conf.globalConfigInfo()['storage_path']
    
    def strategy(self):
        return self.conf.globalConfigInfo()['strategy']
    
    def backup_path(self):
        return self.conf.globalConfigInfo()['backup_path']
    
    def stats(self):
        return self.stats    

    @postonly
    def updateFSS(self, REQUEST):
        """Removed all invalid files"""
        self.conf.updateFSS()

    @postonly
    def removeBackups(self, REQUEST):
        """Remove backup older than x day"""
        max_days = REQUEST.get("max_days", None)
        if max_days is None:
            max_days = 0
        self.conf.removeBackups(max_days)

    @postonly
    def updateRDF(self, REQUEST):
        self.conf.updateRDF()
    
    def fss_get(self):

        NotFound = "NotFound"
        
        if len(traverse_subpath) < 1:
            raise NotFound, "Unknown page."
        
        # Get FSS Item
        name = traverse_subpath[0]
        obj = self.conf.getFSSItem(context, name)
        
        if obj is None:
            raise NotFound, "Unknown page."
        
        if len(traverse_subpath) > 1:
            # Maybe call method of object
            cmd_name = traverse_subpath[1]
            cmd = getattr(obj, 'evalCmd')
            return cmd(cmd_name)
        else:
            REQUEST = context.REQUEST

    def fss_download(self):
        NotFound = "NotFound"

        if len(traverse_subpath) < 1:
            raise NotFound, "Unknown page."
        
        # Get FSS Item
        name = traverse_subpath[0]
        obj = self.conf.getFSSItem(context, name)
        
        if obj is None:
            raise NotFound, "Unknown page."
        
        REQUEST = context.REQUEST
        return obj.download(REQUEST)

    