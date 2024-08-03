
import sys
import argparse
import os





parser = argparse.ArgumentParser(
    prog="lc",
    description="line counter",
    epilog=":3"
)

parser.add_argument('path', nargs='?', default=".")
parser.add_argument('-l', '--list', default=True, action="store_true", help="list files and line counts")
parser.add_argument('-t', '--type', help="filter file types", required=False, dest="type", nargs='*')

args = parser.parse_args()



#collect
pool = []

for (root,dirs,namesRaw) in os.walk(args.path ,topdown=True):
    
    #filter files by type
    namesFiltered = (
        filter(
            lambda x: 
                "." in x and
                x.split(".")[1] in args.type, 
            namesRaw)
        if args.type else namesRaw
    )

    #render full paths
    files = [root + x for x in namesFiltered]
    pool += files
    
    

print(pool)











