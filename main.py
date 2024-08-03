
import sys
import argparse
import os
import dataclasses




parser = argparse.ArgumentParser(
    prog="lc",
    description="line counter",
    epilog=":3"
)

parser.add_argument('path', nargs='?', default=".")
parser.add_argument('-l', '--nolist', action="store_true", help="don't list individual file")
parser.add_argument('-t', '--type', help="filter file types", required=False, dest="type", nargs='*')
parser.add_argument('-v', '--verbose'      , action="store_true")
parser.add_argument('-d', '--hidden'       , action="store_true", help="include hidden directories in scan")

sortFlags = parser.add_mutually_exclusive_group()
sortFlags.add_argument('-s', '--sort'         , dest='sort' , action="store_true", help="sort path listing by line count, small to large")
sortFlags.add_argument('-S', '--sort-reverse' , dest='rsort', action="store_true", help="sort path listing by line count, large to small")

listingTypeFlags = parser.add_mutually_exclusive_group()
listingTypeFlags.add_argument('-a', '--abs', action="store_true", help="show absolute of file when listing")
listingTypeFlags.add_argument('-r', '--rel', action="store_true", help="show relative of file when listing")

args = parser.parse_args()



def blocks(file, size=(2 ** 16)):
    while True:
        data = file.read(size)
        if not data: break
        yield data


#collect
pool = []

path = os.path.abspath(args.path)
for (root, dirs, namesRaw) in os.walk(path, topdown=True):
    
    #skip hidden
    if not args.hidden and "." in root:
        continue
    
    #filter files by type
    namesFiltered = filter(
        lambda x:
            "." in x and
            (
                not args.type or 
                x.split(".")[1] in args.type
            ), 
        namesRaw)

    #render full paths
    files = [os.path.abspath(f'{root}/{x}') for x in namesFiltered]
    pool += files
    

@dataclasses.dataclass
class cEntry:
    count : int
    path  : str


listing = []

#iterate and count
total = 0
for file in pool:
    name = os.path.basename(file)

    try:
        with open(file, encoding='utf-8') as f:
            count = sum(x.count("\n") for x in blocks(f))
            total += count
            
            if not args.nolist:
                
                if   args.abs: listingPath = file
                elif args.rel: listingPath = os.path.relpath(file, path)
                else         : listingPath = name
                
                listing.append(cEntry(count=count, path=listingPath))
    
    except UnicodeDecodeError:
        if args.verbose:
            print(f"Unable to decode {name}")
            
            
#sort
if args.sort : listing.sort(key=lambda x: x.count, reverse=False)
if args.rsort: listing.sort(key=lambda x: x.count, reverse=True)

#list
for entry in listing:            
    print(f"{entry.count: <10} {entry.path}")
            
print(f"\n{total: <10} total")



