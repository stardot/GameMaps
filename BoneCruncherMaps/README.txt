The BoneCruncherMaps project is a set of tools and modules to read, edit and
write maps for the Acorn Electron version of Superior Software's BoneCruncher.

The main tool is a GUI editor for editing levels in an existing BoneCruncher
executable and level files, stored in a Universal Emulator Format (UEF) file.
This depends on the cross-platform PyQt4 GUI framework. This tool is typically
run from the command line from within the BoneCruncherMaps directory itself,
like this:

  PYTHONPATH=. ./tools/editor.py BoneCruncher.uef

You will also need to provide a suitable BoneCruncher.uef file containing the
files for the Acorn Electron version of BoneCruncher. This is not provided in
this package. It is recommended that you save modified levels to a new UEF file
and keep the original as a backup.


Copyright and License Information
---------------------------------

Copyright (C) 2013 David Boddie <david@boddie.org.uk>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
