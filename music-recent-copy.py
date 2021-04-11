import os
import argparse
import shutil
from datetime import datetime,timedelta

def main():
    '''
    the driver
    '''
    args = parse()
    files = get_files(args)
    if confirm(files):
        copy_files(files,args)

  
def parse():
    '''
    sets the args needed to run and returns them
    '''

    #defaults
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    output_root_default = f"./out/recent_{timestamp}/"

    parser = argparse.ArgumentParser(description='Creates copies of recently changed files or directories and places them in a local directory with the same folder structure')
    parser.add_argument('-d','--directory',dest='dir',type=str, required=True, help='the directory to find files in')
    parser.add_argument('-t','--timespan','--days', dest='timespan', required=True, help='number of days prior to the current date to search for')
    parser.add_argument('-o','--output', dest='output_root',default=output_root_default, help=f"output path (optional, defaults to {output_root_default})")
    args = parser.parse_args()

    #standardize directory
    args.dir = os.path.expanduser(args.dir) if args.dir.startswith('~') else os.path.abspath(args.dir)

    #calculate the min date to search for
    args.threshold = datetime.today() - timedelta(days=int(args.timespan))
    
    return args

    
def get_files(args):
    '''
    gets the array of files to partition
    '''
    directory = args.dir
    threshold = args.threshold

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
    music_exts = ['3gp','aa','aac','aax','act','aiff','alac','amr','ape','au','awb','dct','dss','dsd','dsf','dvf','flac','gsm','iklax','ivs','m4a','m4b','m4p','mmf','mp3','mpc','msv','nmf','ogg,','opus','ra,','raw','rf64','sln','tta','voc','vox','wav','wma','wv','webm','8svx','cda']

    return f.split('.')[-1] in music_exts


def copy_files(sources, args):
    '''
    copies files from directory to output
    '''
    directory = args.dir
    output_root = args.output_root

    os.makedirs(os.path.abspath(output_root),exist_ok=True)

    for file in sources:
        relpath = get_path_relroot(file,directory)
        newpath = os.path.abspath(os.path.join(output_root,relpath))
        os.makedirs(os.path.dirname(newpath),exist_ok=True)
        shutil.copy(file,newpath)
    
def confirm(files):
    '''
    displays info and asks for confirm
    '''
    if len(files) == 0:
        print('No files found. Exiting.')
        exit()

    totalsize = sum([os.path.getsize(f) for f in files])/1.0e6
    print("Found {0} file(s) totalling {1:.2f}MB".format(len(files),totalsize))

    print('Proceed with copying? (Y/n)')
    choice = input()
    return choice.upper() == 'Y'
    

def get_path_relroot(path,root):
    '''
    remove the root folder path we supplied earlier
    this is quick and dirty
    '''
    return  path.replace(root,'').strip(os.sep)


if __name__== "__main__": main()