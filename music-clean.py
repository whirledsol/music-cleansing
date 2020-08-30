import sys,os,re
import audio_metadata
import argparse

def main():
    '''
    the driver
    '''
    args = parse()
    files = get_files(args.dir)
    print(f"{'#'*69}\nFILES TO DELETE ({len(files)})\n{'#'*69}")
    print(files)
    if(not args.debug):
       for f in files:
           os.remove(f)
  
def parse():
    '''
    sets the args needed to run and returns them
    '''
    dir_default = f'C:/Users/{os.getlogin()}/Music'
    parser = argparse.ArgumentParser(description='Removes music files based on logic (currently if filename ends with _1 and original exists)')
    parser.add_argument('-d','--directory',dest='dir',type=str, default=dir_default, help='the directory to find files in')
    parser.add_argument('-t','--test','--debug','--dryrun',action='store_true', dest='debug',help='If set, shows the groupings but does not execute')

    args = parser.parse_args()
   
    #check to see if default is ok
    if(args.dir == dir_default):
        print(f'No directory file provided. With search for files in {dir_default}. Is this ok? (Y/n)')
        response = input().upper()
        if(response != 'Y'): exit()

    return args

    
def get_files(directory):
    '''
    gets the array of files to partition
    '''
    print(f'walking {directory}')
    found = []
    for root,_,files in os.walk(directory):
        for f in files:
            if is_music(f) and is_deletable(root,f):
                #print(f)
                found.append(os.path.join(root, f))
    
    return found

def is_music(f):
    """
    returns if path, f, is a music file
    """
    music_exts = ['mp3','flac','wav','ogg','wma','aiff','aac','ra','dsd','dsf']

    return f.split('.')[-1] in music_exts

def is_deletable(r,f):
    """
    here be business logic
    """

    if not '_1.' in f: return False
    
    o = os.path.join(r,f.replace('_1.','.'))
    f = os.path.join(r,f)
    
    if not os.path.isfile(o): return False

    size_f = os.path.getsize(f)
    size_o = os.path.getsize(o)

    return size_o == size_f




if __name__== "__main__": main()