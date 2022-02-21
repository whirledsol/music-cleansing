import sys,os,re
import audio_metadata
import argparse
from mutagen.easyid3 import EasyID3
from mutagen.mp4 import MP4
import mutagen
'''
music_tagger.py
Populates music meta information from title

use:
python music_tagger.py -i "C:/Users/astro/Music/albumname" -r "([^-]+) - ([^-]+).mp3" -g artist,title
'''

CONTAINER_MAP = {
    'mp3':(lambda x: EasyID3(x)),
    'm4a':(lambda x: MP4(x))
}

TAG_MAP = {
    ('mp3','track'):'tracknumber',
    ('mp3','title'):'title',
    ('mp3','artist'):'artist',
    ('mp3','album'):'album',

    ('m4a','track'): 'trkn',
    ('m4a','title'):'\xa9nam',
    ('m4a','artist'):'\xa9ART',
    ('m4a','album'):'\xa9alb',
}

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
    parser.add_argument('--no-album',dest='no_album', action='store_true', required=False, help='Regex to parse titles')
    parser.add_argument('-g','--groups',dest='groups',type=str, required=True, help='CSV of groups. Valid values: track,title,artist,album')
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

def get_ext(f): return f.split('.')[-1]

def is_music(f):
    """
    returns if path, f, is a music file
    """
    return get_ext(f) in CONTAINER_MAP.keys()

def get_container(filepath):
    '''
    determines the container
    '''
    ext = get_ext(filepath)
    return CONTAINER_MAP[ext](filepath)

def tag_file(args,filepath):
    """
    tags the file
    """
    print('-------------')
    
    #file stuff
    filename = os.path.basename(filepath)
    ext = get_ext(filepath)

    #regex magic
    parsed_name = re.search(args.regex, filename)
    
    #check  if match
    group_count = len(list(parsed_name.groups()))
    if group_count != len(args.groups):
        raise Exception(f"{group_count} groups in regex do not match the specified {len(args.groups)} groups")
    
    #init
    audio = None
    try:
        audio = get_container(filepath)
    except:
        audio = mutagen.File(filepath, easy=True)
        audio.add_tags()
    
    #global
    if not args.no_album and not ('album' in args.groups):
        directory = os.path.basename(args.dir)
        tag_type = TAG_MAP[(ext,'album')]
        print('TAGGING',tag_type,directory)
        audio[tag_type] = directory
    
    #loop through
    for i,group in enumerate(args.groups):
        tag_type = TAG_MAP[(ext,group)] if (ext,group) in TAG_MAP else None
        if tag_type is not None:
            tag = parsed_name.group(i+1).strip()
            tag = clean_tag(ext,group,tag)
            print('TAGGING',tag_type,tag)
            audio[tag_type] = tag

    #save
    audio.save()


def clean_tag(ext,group,value):
    '''
    performs any tag specific cleaning
    '''
    CLEAN_MAP = {
        ('m4a','track'):(lambda x:[[int(x),0]])
    }
    return CLEAN_MAP[(ext,group)](value) if (ext,group) in CLEAN_MAP else value


if __name__== "__main__": main()