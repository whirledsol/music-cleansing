import sys,os,re
import audio_metadata
import argparse

def main():
    '''
    the driver
    '''
    args = parse()
    files = get_files(args.dir)
    partitions = partition(files)
    if(args.debug):
        print('#'*69 + '\n' + 'PARTITIONS' + '\n'+'#'*69)
        print([(k,len(v)) for k,v in partitions.items()])
    else:
        save(partitions, args.out)

  
def parse():
    '''
    sets the args needed to run and returns them
    '''
    dir_default = f'C:/Users/{os.getlogin()}/Music'
    parser = argparse.ArgumentParser(description='Partition Music files into subdirectories based on metadata.')
    parser.add_argument('-d','--directory',dest='dir',type=str, default=dir_default, help='the directory to find files in')
    parser.add_argument('-o','--output',dest='out',type=str, default=None, help='the directory to save the files in')
    parser.add_argument('-t','--test','--debug','--dryrun',action='store_true', dest='debug',help='If set, shows the groupings but does not execute')

    args = parser.parse_args()
    
    #default for output is what the user entered for input
    args.out = args.out or args.dir

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
    music_exts = ['mp3','flac','wav','ogg','wma','aiff','aac','ra']
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    files = [f for f in files if os.path.isfile(f) and f.split('.')[-1] in music_exts]
    return files


def partition(files):
    '''
    groups files based on metadata and returns the groupings
    '''
    partitions = {}
    for file in files:
        besttag = "UnknownType"
        try:
            meta = audio_metadata.load(file)
            tags = meta["tags"]
            #print(tags)
            key = None
            if ("album" in tags): key = "album"
            elif ("artist" in tags): key = "artist"
            elif ("genre" in tags): key = "genre"
            besttag = tags[key][0] if key is not None else "Unknown"
        except: pass
        
        #file-friendly
        besttag = slugify(besttag)

        partitions[besttag] = partitions[besttag] + [file] if besttag in partitions else [file]
    
    return partitions


def save(partitions,savedir):
    '''
    Moves files into partitions at base directory savedir
    '''
    for folder,files in partitions.items():
        if not os.path.isdir(os.path.join(savedir,folder)):
            os.mkdir(os.path.join(savedir,folder))
        for file in files:
            originaldir, filename = os.path.split(file)
            os.rename(file, os.path.join(savedir,folder,filename))
    

def slugify(value):
    """
    Normalizes string for file-friendliness
    """
    s = str(value).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)



if __name__== "__main__": main()