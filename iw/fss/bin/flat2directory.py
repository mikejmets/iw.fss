#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Copyright (C)2008 Ingeniweb

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

"""%prog [options] SOURCEPATH DESTINATIONPATH

Converts a "flat" FSS repository in SOURCEPATH to a"directory" FSS
repository in DESTINATIONPATH.

* Purge your FSS storage area using the Plone control panel.
* Activate and regenerate the RDF files if not already done.
* Stop your Zope instance.
* Make sure your "umask" let Zope process read/write the files
  you create.
* Run this utility (use"--help" option to read all the doc).
  Note that the destination path needs free space to hold
  all files of the source space.
* Change your plone-filesystemstorage.conf accordingly (RTFM).
* Restart your Zope instance and test the content types associated
   with FSS.
* (Backup) and remove the source path in case of successful tests."""

import optparse
import os
import sys
import shutil

class BaseMigrator(object):
    """Base for all FSS migrators"""

    def loginfo(self, level, message):
        """Prints the message from the verbosity level"""

        if self.options.verbosity >= level:
            print message
        return

    def run(self):
        """Must be provided by subclasses"""

        raise NotImplementedError


class FlatToDirectoryMigrator(BaseMigrator):

    def __init__(self, options, sourcepath, destpath):
        self.options = options
        self.sourcepath = sourcepath
        self.destpath = destpath
        return

    def run(self):
        """Go baby, go..."""

        self.loginfo(
            1, "Transforming FSS flat storage in %s into directory storage in %s"
            % (self.sourcepath, self.destpath))
        for filename in os.listdir(self.sourcepath):
            self.loginfo(2, "Processing source file '%s'" % filename)
            dir1 = filename[:2]
            dir2 = filename[:4]
            file_destdir = os.path.join(self.destpath, dir1, dir2)
            if not os.path.isdir(file_destdir):
                self.loginfo(2, "Creating '%s' directory" % file_destdir)
                os.makedirs(file_destdir)
            self.loginfo(2, "Copying '%s' to %s" % (filename, file_destdir))
            file_sourcepath = os.path.join(self.sourcepath, filename)
            shutil.copy(file_sourcepath, file_destdir)
            if self.options.delete_source:
                self.loginfo(2, "Deleting original '%s'" % filename)
                os.remove(file_sourcepath)
        self.loginfo(1, "Done")
        return


class Application(object):

    def __init__(self):
        """Getting args and options"""

        parser = optparse.OptionParser(usage=__doc__, version="1.0")
        parser.add_option(
            '-v', '--verbose', action='count', dest='verbosity', default=0,
            help="Add output verbosity for each -v.")
        parser.add_option(
            '-d', '--delete-source', action='store_true', dest='delete_source', default=False,
            help=("Delete source files after being processed "
                  "(hint: make a backup of SOURCEPATH first). "
                  "Default: %default."))
        self.options, paths = parser.parse_args()

        # Controlling arguments validity
        if len(paths) != 2:
            parser.print_help()
            print "Error: SOURCEPATH and DESTINATIONPATH are required arguments."
            sys.exit(2)
        self.sourcepath, self.destpath = paths
        if not os.path.isdir(self.sourcepath):
            parser.print_help()
            print "Error: SOURCEPATH is not an existing directory."
            sys.exit(2)
        if not os.path.isdir(self.destpath):
            parser.print_help()
            print "Error: DESTINATIONPATH is not an existing directory."
            sys.exit(2)
        return


    def run(self):
        """Let's do the job"""

        migrator = FlatToDirectoryMigrator(self.options, self.sourcepath, self.destpath)
        migrator.run()
        return

if __name__ == '__main__':
    Application().run()
