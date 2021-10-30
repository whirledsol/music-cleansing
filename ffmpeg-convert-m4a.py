#!/usr/bin/python

import sys, os
import argparse
from os.path import abspath

FORMAT = "m4a"

def main():
	args = parse()
	
	#print(f"looking in {args.dir}")
	for file in get_files(args.dir):
		print(f"working on {file}")
		newfile = f"{''.join(file.split('.')[:-1])}.{FORMAT}"
		cmd = f"ffmpeg -i \"{file}\" -map 0 -c copy -map_metadata:s:a 0:s:a -loglevel error \"{newfile}\""
		print(cmd)
		os.system(cmd)

def parse():
	parser = argparse.ArgumentParser(description='Converts music files to aac')
	parser.add_argument('-d','--directory',dest='dir',type=str, required=True, help='the directory to find files in')

	args = parser.parse_args()
	args.dir = abspath(args.dir)

	print('****************\n')
	print(args)
	print('****************\n')
	return args

def get_files(directory):
	'''
	gets the array of files to partition
	'''
	exts = ['3gp','aa','aac','aax','act','aiff','alac','amr','ape','au','awb','dct','dss','dsd','dsf','dvf','flac','gsm','iklax','ivs','m4a','m4b','m4p','mmf','mp3','mpc','msv','nmf','ogg,','opus','ra,','raw','rf64','sln','tta','voc','vox','wav','wma','wv','webm','8svx','cda']
	exts = [x for x in exts if x != FORMAT]
	files = [os.path.join(directory, f) for f in os.listdir(directory)]
	files = [f for f in files if os.path.isfile(f) and f.split('.')[-1] in exts]
	return files

if __name__ == "__main__": main()