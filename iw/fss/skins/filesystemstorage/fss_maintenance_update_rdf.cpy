## Controller Python Script "fss_maintenance_update_rdf"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title= Update RDF
# Copyright (c) Ingeniweb 2007
# $Id$

from iw.fss.utils import FSSMessageFactory as _

from Products.CMFCore.utils import getToolByName
fss_tool = getToolByName(context, 'portal_fss')

# Update RDF
fss_tool.updateRDF()

message = 'message_rdf_updated'
context.plone_utils.addPortalMessage(_(unicode(message)))
return state.set(status='success')
