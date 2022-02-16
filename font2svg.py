#!/usr/bin/env python3

VERSION="0.1.0" # MAJOR.MINOR.PATCH | http://semver.org

import argparse
import os
import fontforge


def parse_commandline():
	parser = argparse.ArgumentParser(prog='font2svg', description='Extract font glyphs from font file(s) into svg files')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s v{0}'.format(VERSION))
	parser.add_argument('filename', nargs='+', help='font file(s) to extract')
 
	return parser.parse_args()


def main():
	args = parse_commandline()
	fontforge.runInitScripts()

	for fn in args.filename:
		print("Opening font file: {}".format(fn))
		font = fontforge.open(fn,('fontlint','hidewindow'))
		
		print("Extracting glyphs from font: {}".format(font.fontname))
		for glyph in font.glyphs():
			if glyph.isWorthOutputting():
				outfn = clean_filename("{}__{}.svg".format(font.fontname,glyph.glyphname))
				#print("   Export {}".format(outfn))
				glyph.export(outfn)
			else:
				print("Skipping Glyph: {}".format(glyph.glyphname))

	return


"""
Url: https://gist.github.com/wassname/1393c4a57cfcbf03641dbc31886123b8
"""
import unicodedata
import string

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
char_limit = 200

def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r,'_')
    
    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
    
    # keep only whitelisted chars
    cleaned_filename = ''.join(c for c in cleaned_filename if c in whitelist)
    if len(cleaned_filename)>char_limit:
        print("Warning, filename truncated because it was over {}. Filenames may no longer be unique".format(char_limit))
    return cleaned_filename[:char_limit]    


if __name__ == "__main__":
	main()


