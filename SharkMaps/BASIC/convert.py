#!/usr/bin/env python

import os, sys

if len(sys.argv) != 2:

    sys.stderr.write("Usage: %s <BASIC file>\n" % sys.argv[0])
    sys.exit(1)

t = open(sys.argv[1]).read()
t = t.replace("\n", "\r")
lines = t.rstrip().split("\r")

i = 5
new_lines = []
for line in lines:

    j = 0
    for c in line:
        if ord(c) < 48 or ord(c) > 57:
            break
        j += 1
    
    new_lines.append(str(i) + line[j:])
    i += 5

t = "\r".join(new_lines) + "\r"
open(sys.argv[1], "w").write(t)
file_name = os.path.split(sys.argv[1])[1]
open(sys.argv[1]+".inf", "w").write(
    "$.%s	ffff0e00	ffff802b	%x" % (file_name, len(t))
    )

sys.exit()
