import sys,os,re
import audio_metadata

def main():
    if len(sys.argv) <= 1:
        print("No path argument supplied.")
        return
    directory = sys.argv[1]
    savedir = sys.argv[2] if len(sys.argv) == 3 else directory
    files = [os.path.join(directory, f) for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    partitions = partition(files)
    #print([(k,len(v)) for k,v in partitions.items()])
    save(partitions, savedir)

def partition(files):
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
    #s = str(value).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

if __name__== "__main__": main()