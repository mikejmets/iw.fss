# Zope imports
from Products.Five import BrowserView
from zope.component import queryUtility

# Products imports
from iw.fss.utils import FSSMessageFactory as _
from iw.fss.interfaces import IConf

class FSSView(BrowserView):
    
    def __init__(self, context, request):
        super(FSSView, self).__init__(context, request)
        conf_class = queryUtility(IConf, "globalconf")
        self.conf = conf_class()
         
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
    @postonly
    def UpdateFss(self, REQUEST):
        """Removed all invalid files"""
        pass
    @postonly
    def RemoveBackup(self, REQUEST):
        """Remove backup older than x day"""
        pass
    
    