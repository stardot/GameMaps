#! /usr/bin/python
"""
	moonmap.py - A Moon Raider level convertor
	(C) David Boddie 2001
"""

# History
#
# 0.10 (Sun 21st January 2001)
# 
# Initial version.
# 
# 0.11 (Tue 23rd January 2001)
# 
# Modified version of 0.10 which allows empty lines to denote no floor or ceiling.
# 
# 0.12 (Mon 13th August 2001)
#
# Tidied up multi-platform support.
#
# 0.13 (Thu 06th September 2001)
#
# Now patches the UEF file directly using UEFfile objects.
#


import os, string, sys, UEFfile

version = '0.13 (Thu 06th September 2001)'

# Global variables

start_level = 3
screen_height = 27


def count_left(s):

	i = 0
	l = 0
	while i < len(s):

		if s[i] == '#':
			l = l + 1
			i = i + 1
		else:
			break

	return l, s[i:]


def count_right(s):

	i = len(s)-1
	l = 0
	while i >= 0:

		if s[i] == '#':
			l = l - 1
			i = i - 1
		else:
			break

	return l, s[:i+1]


def check_length(bin, level_offset, line_no):

	if (len(bin) - level_offset) > 0xff:
		print 'Level too long (or too detailed) at line %i.' % line_no
		sys.exit()


# Read a map file and produce a binary description which can be understood
# by Moon Raider

def read_map(map):

	building_level = start_level
	ceiling_level = 0
	level_offset = 0x000

	line_no = 1

	bin = ''

	while 1:

		line = map.readline()
		if not line:
			break

		line = string.strip(line)

		# Determine the presence of aliens or fireballs
		code = 0

		if line != '':

			if line[-1] == '@':
				code = code | 0x40
				line = line[:-1]
			elif line[-1] == '*':
				code = code | 0x20
				line = line[:-1]

		# Count the building level
		blevel, line = count_left(line)

		if blevel > (screen_height+ceiling_level-1):
			print 'Floor is too high at line %i.' % line_no
			sys.exit()

		if blevel > building_level:
			if (blevel-building_level) < 32:
				bin = bin + chr(0x80 | (blevel-building_level))
				check_length(bin, level_offset, line_no)
			else:
				print 'Step is too high at line %i.' % line_no
				sys.exit()

			building_level = blevel

		elif blevel < building_level:
			if (building_level-blevel) < 32:
				bin = bin + chr(0xa0 | (building_level-blevel))
				check_length(bin, level_offset, line_no)
			else:
				print 'Step is too high at line %i.' % line_no
				sys.exit()

			building_level = blevel

		else:
			# Do nothing (same level)
			pass

		# Count the ceiling level
		clevel, line = count_right(line)

		if clevel < (-screen_height+building_level+1):
			print 'Ceiling is too low at line %i.' % line_no
			sys.exit()

		if clevel < ceiling_level:
			if (ceiling_level-clevel) < 32:
				bin = bin + chr(0xe0 | (ceiling_level-clevel))
				check_length(bin, level_offset, line_no)
			else:
				print 'Step is too high at line %i.' % line_no
				sys.exit()

			ceiling_level = clevel

		elif clevel > ceiling_level:
			if (clevel-ceiling_level) < 32:
				bin = bin + chr(0xc0 | (clevel-ceiling_level))
				check_length(bin, level_offset, line_no)
			else:
				print 'Step is too high at line %i.' % line_no
				sys.exit()

			ceiling_level = clevel

		else:
			# Do nothing (same level)
			pass

                # The rest of the information must be the object present
		line = string.strip(line)

		if line == 'E':
			bin = bin + chr(0xff)
			chars = level_offset + 0x100 - len(bin)

			if chars > 0:
				bin = bin + (chars * '\000')

			level_offset = level_offset + 0x100
			if level_offset == 0x700:
				break
                else:
			if line == '!':
				code = code | 0x00
			elif line == 'm':
				code = code | 0x01
			elif line == 'f':
				code = code | 0x02
			elif line == '>':
				building_level = building_level + 1
				code = code | 0x03
			elif line == '<':
				building_level = building_level - 1
				code = code | 0x04
			elif line == '\\':
				building_level = building_level + 2
				code = code | 0x05
			elif line == '/':
				building_level = building_level - 2
				code = code | 0x06
			elif line == 'r':
				code = code | 0x07
			elif line == 't':
				code = code | 0x08
			elif line == 'x':
				code = code | 0x09
			elif line == '|':
				code = code | 0x0a
			elif line == '?':
				code = code | 0x0b
			elif line == '':
				code = code | 0x0c
			elif line == 'F':
				code = code | 0x0d
#			elif line == '|':
#				code = code | 0x0e
#			elif line == '|':
#				code = code | 0x0f
			elif line == 'H':
				code = code | 0x10
			elif line == '1':
				code = code | 0x11
			elif line == '2':
				code = code | 0x12

			bin = bin + chr(code)
	
			check_length(bin, level_offset, line_no)

		line_no = line_no + 1

	# Return the binary map information
	return bin


def hex2num(s):
	"""Convert a string of hexadecimal digits to an integer."""

	n = 0

	for i in range(0,len(s)):

		a = ord(s[len(s)-i-1])
		if (a >= 48) & (a <= 57):
			n = n | ((a-48) << (i*4))
		elif (a >= 65) & (a <= 70):
			n = n | ((a-65+10) << (i*4))
		elif (a >= 97) & (a <= 102):
			n = n | ((a-97+10) << (i*4))
		else:
			return None

	return n


def get_leafname(path):
	"""Get the leafname of the specified file."""

	pos = string.rfind(path, os.sep)
	if pos != -1:
		return path[pos+1:]
	else:
		return path


# Main program

if __name__ == '__main__':

	if os.sep != '.':
		suffix = '.'
	else:
		suffix = '/'
	
	if len(sys.argv) < 4:

		print 'Syntax: moonmap'+suffix+'py <map file> <original UEF file> <new UEF file>'
		print
		print 'MoonMap - a Moon Raider level convertor'
		print '(C) David Boddie 2001'
		print
		print 'Version '+version
		print
		print '<map file> is a .map file containing a textual description of Moon Raider levels.'
		print 'This is converted to a binary description and is added to the relevant file'
		print 'contained within the Moon Raider UEF file specified by <original UEF file>.'
		print 'A new version is written to the file specified by <new UEF file>.'
		print
		sys.exit()
	
	map_file = sys.argv[1]
	in_uef_file = sys.argv[2]
	out_uef_file = sys.argv[3]

	try:
		input = open(map_file, 'r')
	except IOError:
		print "Couldn't open "+map_file+' for input.'
		sys.exit()
		
	# Convert the textual description to a binary format
	map_data = read_map(input)

	# Close the input file		
	input.close()

	# Read the UEF file
	try:
		uef = UEFfile.UEFfile(in_uef_file)
	except UEFfile_error:
		print "Couldn't open %s" % in_uef_file
		sys.exit()

	# Find the executable containing the map
	f = 0
	while f < len(uef.contents):

		if uef.contents[f]['load'] == 0x1900:
			break
		else:
			f = f + 1

	if f == len(uef.contents):

		# Failed to find executable
		print """Couldn't find the correct executable. Please ensure
		that this is the correct UEF file."""
		sys.exit()

	# Export the file from the UEF file
	name, load, exe, data = uef.export_files(f)

	if len(data) != 0x3f00:

		print 'The executable in %s is incorrect in length.' % execfile
		sys.exit()

	# Replace the old map
	new_data = data[:0x5000 - 0x1900] + map_data + data[0x5700 - 0x1900:]

	# Create a new UEF file
	n = UEFfile.UEFfile(creator = 'MoonMap '+version)
	# of version 0.6
	n.minor = 6

	# Copy the files before the executable into the new file
	n.import_files(0, uef.export_files(range(0,f)))
	# Add the new executable
	n.import_files(f, (name, load, exe, new_data))
	# Copy the files after the executable into the new file
	n.import_files(f+1, uef.export_files(range(f+1,len(uef.contents))))

	# Write the new executable
	try:
		n.write(out_uef_file)
	except UEFfile_error:
		print "Couldn't write the new executable to %s." % out_uef_file
		sys.exit()

	print 'Replaced the map data in %s.' % out_uef_file
	
	# Exit
	sys.exit()
