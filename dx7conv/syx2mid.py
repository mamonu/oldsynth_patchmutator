#!/usr/bin/env python3
import sys
import array
import os

def syx2mid(syx):
    #####  HEADER CHUNK #####
    # format 0, 1 track, 96 ticks/quarter
    mid = [0x4d, 0x54, 0x68, 0x64, 0, 0, 0, 6, 0, 0, 0, 1, 0, 0x60]
    
    ##### TRACK CHUNK #####
    mid += [0x4d, 0x54, 0x72, 0x6b]
    mid += [0, 0, 0, 0] # tracklength=mid[18:22]
    
    ##### TRACK events #####
    # text meta event "SysEx Data"
    mid += [0x00, 0xff, 0x01]
    mid += [10, ord('S'), ord('y'), ord('s'), ord('E'), ord('x'), 
            ord(' '), ord('D'), ord('a'), ord('t'), ord('a')]
    # trackname meta event
    mid += [0x00, 0xff, 0x03]
    mid += [10, ord('S'), ord('y'), ord('s'), ord('E'), ord('x'), 
            ord(' '), ord('D'), ord('a'), ord('t'), ord('a')]

    # SysEx events
    mid.append(0) # delta time before first sysex event
    for i in range(len(syx)):
        if syx[i] == 0xf0:
            count = 0
            syxevent = []
            while syx[i] != 0xf7:
                i += 1
                count += 1
                syxevent.append(syx[i])
            mid += [0xf0] + varlen(count + 1) + syxevent + [0xf7]
            mid += varlen(ticks(int(10 + 0.32 * count))) # delta time before next event + 10ms


    # End of Track meta event
    mid += [0xff, 0x2f, 0x00]
    
    trlen = len(mid[22:])
    mid[18] = (trlen&0xff000000)>>24
    mid[19] = (trlen&0xff0000)>>16
    mid[20] = (trlen&0xff00)>>8
    mid[21] = trlen&0xff

    return mid


def varlen(i):
    vl = []
    if i <= 0b1111111:
        vl.append(i)
    elif i <= 0b11111111111111:
        vl.append(128 + ((i&0b11111110000000)>>7))
        vl.append(i&0b1111111)
    elif i <= 0b111111111111111111111:
        vl.append(128 + ((i&0b111111100000000000000)>>24))
        vl.append(128 + ((i&0b11111110000000)>>7))
        vl.append(i&0b1111111)
    else:
        vl.append(128 + ((i&0b1111111000000000000000000000)>>21))
        vl.append(128 + ((i&0b111111100000000000000)>>14))
        vl.append(128 + ((i&0b11111110000000)>>7))
        vl.append(i&0b1111111)
    return vl

def ticks(ms):
    bpm = 120
    res = 96
    return ms * bpm * res // 60000


try:
    indat = array.array('B')
    infile = sys.argv[1]
    if len(sys.argv) == 3:
        outfile = sys.argv[2]
    else:
        outfile = infile[:infile.rfind('.')] + ".mid"

    with open(infile, "rb") as f:
        indat.fromfile(f, os.path.getsize(infile))

    outdat = array.array('B')
    outdat.fromlist(syx2mid(indat))

    with open(outfile, "wb") as f:
        outdat.tofile(f)
    
    print("{} succesfully converted to {}".format(infile, outfile))
except:
    print("Usage: {} infile.syx [outfile.mid]".format(os.path.basename(sys.argv[0])))

quit()

