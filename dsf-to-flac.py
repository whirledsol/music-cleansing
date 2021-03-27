#!/usr/bin/python

import sys, os
import argparse
from os.path import abspath

def main():
	args = parse()
	
	#print(f"looking in {args.dir}")
	for file in os.listdir(args.dir):
		if file.endswith(".dsf"):
			fileagnostic = f"{args.dir}\\{file[:-4]}"
			print(f"working on {fileagnostic}")
			os.system(f"ffmpeg -i \"{fileagnostic}.dsf\" -af aformat={args.format} -compression_level {args.compression_level} \"{fileagnostic}.flac\"")

def parse():
	parser = argparse.ArgumentParser(description='Converts dsf to flac')
	parser.add_argument('-d','--directory',dest='dir',type=str, required=True, help='the directory to find files in')
	parser.add_argument('-l','--low',dest='low',action='store_true', help='if supplied, uses 16bit. defaults to 24bit.')
	parser.add_argument('-c','--compression_level',dest='compression_level',type=str, default='12', help='value from 0-12 with 12 taking more time to compress')

	args = parser.parse_args()
	args.dir = abspath(args.dir)
	args.format = "s16:44100" if args.low else "s32:176000"

	print('****************\n\n')
	print(args)
	print('****************\n\n')
	return args

if __name__ == "__main__": main()