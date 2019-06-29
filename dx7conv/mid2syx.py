#!/usr/bin/env python3
import sys
import array
import os

def mid2syx(mid):
    syx = []
    for i in range(len(mid)):
        if mid[i] == 0xf0:
            syx.append(0xf0)
            while mid[i]&0b10000000==0b10000000:
                i+=1
            i += 1
            while mid[i] != 0xf7:
                syx.append(mid[i])
                i += 1
            syx.append(0xf7)
    return syx

try:
    indat = array.array('B')
    infile = sys.argv[1]
    if len(sys.argv) == 3:
        outfile = sys.argv[2]
    else:
        outfile = infile[:infile.rfind(".")]+".syx"

    with open(infile, "rb") as f:
        indat.fromfile(f, os.path.getsize(infile))

    outdat = array.array('B')
    outdat.fromlist(mid2syx(indat))

    with open(outfile, "wb") as f:
        outdat.tofile(f)

    print("{} succesfully converted to {} !".format(infile, outfile))
except:
    print("Usage: {} infile.mid outfile.syx".format(os.path.basename(sys.argv[0])))


quit()

