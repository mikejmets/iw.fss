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
        """
        Returns stats on FileSystem storage
        valid_files_count -> Count of valid files
        not_valid_files_count -> Count of not valid files
        valid_backups_count -> Count of valid backups
        not_valid_backups_count -> Count of not valid backups
        """

        storage_brains = self.conf.getStorageBrains()
        backup_brains = self.conf.getBackupBrains()

        valid_files = [x for x in storage_brains if x['path'] is not None]
        not_valid_files = [x for x in storage_brains if x['path'] is None]
        valid_backups = [x for x in backup_brains if x['path'] is None]
        not_valid_backups = [x for x in backup_brains if x['path'] is not None]


        # Sort valid files by size
        def cmp_size(a, b):
              return cmp(a['size'], b['size'])

        valid_files.sort(cmp_size)

        # Size in octets
        total_size = 0
        largest_size = 0
        smallest_size = 0
        average_size = 0

        for x in valid_files:
            total_size += x['size']

        if len(valid_files) > 0:
            largest_size = valid_files[-1]['size']
            smallest_size = valid_files[0]['size']
            average_size = int(total_size / len(valid_files))

        stats = {
          'valid_files_count' : len(valid_files),
          'not_valid_files_count' : len(not_valid_files),
          'valid_backups_count' : len(valid_backups),
          'not_valid_backups_count' : len(not_valid_backups),
          'total_size' : total_size,
          'largest_size': largest_size,
          'smallest_size' : smallest_size,
          'average_size' : average_size,
          }

        return stats    

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

    