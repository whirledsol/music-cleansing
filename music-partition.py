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
        save(partitions, args)
  
def parse():
    '''
    sets the args needed to run and returns them
    '''
    dir_default = f'C:/Users/{os.getlogin()}/Music'
    parser = argparse.ArgumentParser(description='Partition Music files into subdirectories based on metadata.')
    parser.add_argument('-d','--directory',dest='dir',type=str, default=dir_default, help='the directory to find files in')
    parser.add_argument('-o','--output',dest='out',type=str, default=None, help='the directory to save the files in')
    parser.add_argument('-c','--clean', dest='clean', type=str, default=None, help='if specified, will replace this regex in the music file with blank')
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
    exts = ['3gp','aa','aac','aax','act','aiff','alac','amr','ape','au','awb','dct','dss','dsd','dsf','dvf','flac','gsm','iklax','ivs','m4a','m4b','m4p','mmf','mp3','mpc','msv','nmf','ogg,','opus','ra,','raw','rf64','sln','tta','voc','vox','wav','wma','wv','webm','8svx','cda']
    files = [os.path.join(directory, f) for f in os.listdir(directory)]
    files = [f for f in files if os.path.isfile(f) and f.split('.')[-1] in exts]
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


def save(partitions,args):
    '''
    Moves files into partitions at base directory savedir
    '''
    savedir = args.out

    for folder,files in partitions.items():
        if not os.path.isdir(os.path.join(savedir,folder)):
            os.mkdir(os.path.join(savedir,folder))
            
        for file in files:
            originaldir, filename = os.path.split(file)
            if (args.clean or '') != '':
                filename = clean_filename(filename, args.clean)
            os.rename(file, os.path.join(savedir,folder,filename))
    
def clean_filename(filename,clean):
    """
    custom formatting for the new file name
    """
    try:
        return re.sub(clean, '', filename)
    except:
        return filename
    

def slugify_legacy(value):
    """
    Normalizes string for file-friendliness
    """
    s = str(value).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def slugify(value):
    """
    Normalizes string for file-friendliness
    """
    s = str(value).strip()
    return re.sub(r'<|>|:|"|\/|\\|\||\?|\*', '', s)



if __name__== "__main__": main()
