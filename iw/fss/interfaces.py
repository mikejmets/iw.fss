## -*- coding: utf-8 -*-
## Copyright (C) 2008 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.

# $Id$
"""
Interfaces exposed here
"""
__author__  = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'

from zope.interface import Interface

class IFSSTool(Interface):
    """Marker for FSS tool"""
    pass

class IConf(Interface):
    """Main configuration for fss"""
    def globalConfigInfo():
        """Get global Configuration"""
    def initProperties():
        """Init properties"""
    def isRDFEnabled():
        """Returns true if RDF is automaticaly generated when file added"""
    def enableRDF(enabled):
        """Enable rdf or not"""
    def getRDFScript():
        """Returns rdf script used to generate RDF on files"""
    def setRDFScript(rdf_script):
        """Set rdf script used to generate RDF on files"""
    def getStorageStrategy():
        """Returns the storage strategy"""
    def getUIDToPathDictionnary():
        """Returns a dictionnary"""
    def getPathToUIDDictionnary():
        """Returns a dictionnary"""
    def getFSSBrains(items):
        """Returns a dictionnary."""
    def getStorageBrains():
        """Returns a list of brains in storage path"""
    def getStorageBrainsByUID(uid):
        """ Returns a list containing all brains related to fields stored
        on filesystem of object having the specified uid"""
    def getBackupBrains():
        """Returns a list of brains in backup path"""
    def updateFSS():
        """Update FileSystem storage"""
    def removeBackups(max_days):
        """Remove backups older than specified days"""
    def updateRDF():
        """Add RDF files to fss files"""
    def getFSSItem(instance, name):
        """Get value of fss item.
        This method is called from fss_get script."""
    def configletTabs(template_id):
        """Data for drawing tabs in FSS config panel"""
    def getFSStats():
        """Returns stats on FileSystem storage"""
    def patchedTypesInfo():
        """A TALES friendly summary of content types with storage changed to FSS"""
    def siteConfigInfo():
        """A TALES friendly configuration info mapping for this Plone site"""
    def globalConfigInfo():
        """A TALES friendly configuration info mapping for global configuration"""
    def formattedReadme():
        """README.txt (reStructuredText) transformed to HTML"""
        
