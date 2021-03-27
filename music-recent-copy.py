import sys,os,re
import audio_metadata
import argparse
import shutil
from datetime import datetime,timedelta

def main():
    '''
    the driver
    '''
    args = parse()
    files = get_files(args.dir,args.threshold)
    copy_files(files,args.output_root)

  
def parse():
    '''
    sets the args needed to run and returns them
    '''
    parser = argparse.ArgumentParser(description='Creates copies of recently changed files or directories and places them in a local directory with the same folder structure')
    parser.add_argument('-d','--directory',dest='dir',type=str, required=True, help='the directory to find files in')
    parser.add_argument('-t','--timespan','--days', dest='timespan', required=True, help='number of days prior to the current date to search for')

    args = parser.parse_args()

    #standardize directory
    args.dir = os.path.expanduser(args.dir) if args.dir.startswith('~') else os.path.abspath(args.dir)

    #calculate the min date to search for
    args.threshold = datetime.today() - timedelta(days=int(args.timespan))
    timestamp = datetime.now().strftime("%Y%m/%dT%H%M%S")
    
    #output path, always the same
    args.output_root = f"./output/recent_{timestamp}/"

    return args

    
def get_files(directory,threshold):
    '''
    gets the array of files to partition
    '''
    print(f'walking {directory}')
    found = []
    for root,_,files in os.walk(directory):
        for f in files:
            path = os.path.join(root, f)
            if(is_music(path) and is_recent(path,threshold)):
                found.append(path)
    return found

def is_recent(f,threshold_date):
    """
    returns if modified date >= threshold date
    """
    modified_date = datetime.fromtimestamp(os.path.getmtime(f))
    return modified_date >= threshold_date

def is_music(f):
    """
    returns if path, f, is a music file
    """
    music_exts = ['mp3','flac','wav','ogg','wma','aiff','aac','ra','dsd','dsf']

    return f.split('.')[-1] in music_exts


def copy_files(sources, output_root):
    '''
    copies files from directory to output
    '''
    print(sources)

if __name__== "__main__": main()