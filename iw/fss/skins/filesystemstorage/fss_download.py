## Script (Python) "fss_download"
##title=Download a file keeping the original uploaded filename
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
# Copyright (c) Ingeniweb 2007
# $Id$

from Products.CMFCore.utils import getToolByName

NotFound = "NotFound"

if len(traverse_subpath) < 1:
    raise NotFound, "Unknown page."

# Get FSS Item
name = traverse_subpath[0]
fsstool = getToolByName(context, 'portal_fss')
obj = fsstool.getFSSItem(context, name)

if obj is None:
    raise NotFound, "Unknown page."

REQUEST = context.REQUEST
return obj.download(REQUEST)
