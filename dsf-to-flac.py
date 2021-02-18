#!/usr/bin/python

import sys, os
import argparse
from os.path import abspath

def main(argv):
	args = parse()
	
	print(f"looking in {args.dir}")
	for file in os.listdir(args.dir):
		if file.endswith(".dsf"):
			fileagnostic = f"{args.dir}\\{file[:-4]}"
			print(f"working on {fileagnostic}")
			os.system(f"ffmpeg -i \"{fileagnostic}.dsf\" -af aformat={args.format} -compression_level {args.compression_level} \"{fileagnostic}.wav\"")

def parse():
	parser = argparse.ArgumentParser(description='Converts dsf to flac')
    parser.add_argument('-d','--directory',dest='dir',type=str, default=dir_default, help='the directory to find files in')
    parser.add_argument('-h','--hq',dest='hq',action='store_false', help='if present, uses 32bit. defaults: 16bit.')
	parser.add_argument('-c','--compression_level',dest='compression_level',type=str, default='12', help='value from 0-12 with 12 taking more time to compress')

	args = parser.parse_args()

	args.dir = abspath(dir)
	args.format = "s32:176000" if args.hq else "s16:44100" 

	return args

if __name__ == "__main__": main()