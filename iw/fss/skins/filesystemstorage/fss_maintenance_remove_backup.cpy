## Controller Python Script "fss_maintenance_remove_backup"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=days=0
##title= Remove backups
# Copyright (c) Ingeniweb 2007
# $Id$

from iw.fss.utils import FSSMessageFactory as _

from Products.CMFCore.utils import getToolByName

fss_tool = getToolByName(context, 'portal_fss')

# Remove backups
fss_tool.removeBackups(days)

message = 'message_backups_removed'
context.plone_utils.addPortalMessage(_(unicode(message)))
return state.set(status='success')


