import sys,os,re
import audio_metadata
import argparse
from mutagen.easyid3 import EasyID3

def main():
    '''
    the driver
    '''
    args = parse()
    files = get_files(args.dir)
    print(f"{'#'*69}\nFILES TO TAG ({len(files)})\n{'#'*69}")
    print(files)
    if(not args.debug):
       for f in files:
           tag_file(args,f)
  
def parse():
    '''
    sets the args needed to run and returns them
    '''
    parser = argparse.ArgumentParser(description='Populates music metadata based on consistent filename')
    parser.add_argument('-i','--dir',dest='dir',type=str, required=True, help='the directory to find files in')
    parser.add_argument('-r','--regex',dest='regex',type=str, required=True, help='Regex to parse titles')
    parser.add_argument('-g','--groups',dest='groups',type=str, required=True, help='CSV of groups. Valid values: tracknumber,title,artist,album')
    parser.add_argument('-d','--test','--debug','--dryrun',action='store_true', dest='debug',help='If set, shows the groupings but does not execute')
    args = parser.parse_args()
    args.groups = args.groups.split(',')
    return args

    
def get_files(directory):
    '''
    gets the array of files to partition
    '''
    print(f'walking {directory}')
    found = []
    for root,_,files in os.walk(directory):
        for f in files:
            if is_music(f):
                found.append(os.path.join(root, f))
    
    return found

def is_music(f):
    """
    returns if path, f, is a music file
    """
    music_exts = ['mp3'] #,'flac','wav','ogg','wma','aiff','aac','ra','dsd','dsf'] #TODO

    return f.split('.')[-1] in music_exts


def tag_file(args,filepath):
    """
    tags the file
    """

    #file stuff
    filename = os.path.basename(filepath)
    
    #regex magic
    parsed_name = re.search(args.regex, filename)
    
    #check  if match
    group_count = len(list(parsed_name.groups()))
    if group_count != len(args.groups):
        raise Exception(f"{group_count} groups in regex do not match the specified {len(args.groups)} groups")
    
    #init
    audio = EasyID3(filepath)
    
    #global
    if not ('album' in args.groups):
        directory = os.path.basename(args.dir)
        audio['album'] = directory
    
    #loop through
    for i,group in enumerate(args.groups):
        audio[group] = parsed_name.group(i+1).strip()

    #save
    audio.save()

if __name__== "__main__": main()