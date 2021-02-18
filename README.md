# music-cleansing
Various python projects to help maintain music library.

## music-partition
Python app which takes a flat directory of music files and partitions them into folders based on metadata. Useful for Google Music downloads.

### Usage
```dos
python music-partition.py -d "C:/Users/Will/Music/Google Music" -c "^[^-]*-\s" -t
```