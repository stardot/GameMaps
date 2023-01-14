This repository contains a set of tools and modules to read and display
maps for the Acorn Electron version of Mandarin Software's Icarus.

The Tools directory contains Python tools that extract images and maps from the
data stored in a Universal Emulator Format (UEF) file. The tools are run from
the command line from within the Icarus directory itself, like this:

```
  PYTHONPATH=. ./Tools/imagemap.py Icarus_E.uef 1 /tmp/1.png
  PYTHONPATH=. ./Tools/textmap.py Icarus_E.uef A
  PYTHONPATH=. ./Tools/read_sprites.py Icarus_E.uef /tmp/sprites
```

You will also need to provide a suitable Icarus_E.uef file containing the
files for the Acorn Electron version of Icarus. This is not provided in this
package.


Copyright and License Information
---------------------------------

Copyright (C) 2016 David Boddie <david@boddie.org.uk>

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
