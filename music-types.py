import sys,os,re
import audio_metadata
import argparse

def main():
    '''
    the driver
    '''
    args = parse()
    bins = bin_files(args.dir)
    print(f"{'#'*69}\nFILES TYPES\n{'#'*69}")
    bins = [(k,v) for k,v in bins.items()]
    bins.sort(key = lambda x: x[1]) 
    print(bins)
    
  
def parse():
    '''
    sets the args needed to run and returns them
    '''
    dir_default = f'C:/Users/{os.getlogin()}/Music'
    parser = argparse.ArgumentParser(description='Show the types of files in dir')
    parser.add_argument('-d','--directory',dest='dir',type=str, default=dir_default, help='the directory to find files in')

    args = parser.parse_args()
   
    #check to see if default is ok
    if(args.dir == dir_default):
        print(f'No directory file provided. With search for files in {dir_default}. Is this ok? (Y/n)')
        response = input().upper()
        if(response != 'Y'): exit()

    return args

    
def bin_files(directory):
    '''
    gets a dictionary of ext types
    '''
    print(f'walking {directory}')
    types = {}
    for root,_,files in os.walk(directory):
        for f in files:
            ext = f.split('.')[-1]
            if ext in types:
                types[ext] +=1
            else:
                types[ext] = 1
    
    return types



if __name__== "__main__": main()