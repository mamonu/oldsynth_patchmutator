#!/usr/bin/env python3
"""
txconvert.py

(c)2012 Martin Tarenskeen <m.tarenskeenATzonnetPOINTnl>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

__license__ = 'GPL v3'

import sys
import os
from argparse import ArgumentParser
from glob import glob
from DXconvert import TXC
from DXconvert import dxcommon

MAXFILESIZE = dxcommon.MAXFILESIZE
PROGRAMNAME = TXC.PROGRAMNAME
PROGRAMVERSION = dxcommon.PROGRAMVERSION
PROGRAMDATE = dxcommon.PROGRAMDATE
ALLOWED_CHARACTERS = dxcommon.ALLOWED_CHARACTERS

############# CLI ###################

def cli_main(argv=sys.argv):
    progname = os.path.basename(argv[0])

    parser = ArgumentParser(
            description = '{}\nVersion: {} ({})'.format(PROGRAMNAME, PROGRAMVERSION, PROGRAMDATE), )
    parser.add_argument('-c', '--channel', default=0, type=int, help='Midi channel in SysEx header')
    parser.add_argument('-C', '--check', action='store_true', default=False, help='Check SysEx checksum before import') 
    parser.add_argument('-f', '--find', metavar='STRING', help='Search for STRING in patchnames')
    parser.add_argument('-mi', '--mid_in', help='select midiport MID_IN to receive data FROM synth when selecting a .req file')
    parser.add_argument('-mo', '--mid_out', help='select midiport MID_OUT to send data TO synth when choosing "MIDI" as outfile')
    parser.add_argument('-m', '--mid', help='use this option as a shortcut for "--mid_in MID_IN --mid_out MID_OUT", if MID_IN and MID_OUT have the same name MID')
    parser.add_argument('-n', '--nosplit', action='store_true', default=False, help="Don't split: save data in one file")
    parser.add_argument('-nd', '--nodupes', action='store_true', default=False, help='Remove duplicates')
    parser.add_argument('-nd2', '--nodupes2', action='store_true', default=False, help='Remove duplicates, also with different names')
    parser.add_argument('-o', '--offset', type=int, default=0, help="Ignore first OFFSET bytes in input file(s)")
    parser.add_argument('-r', '--random', metavar='NUMBER', type=int, default=-1, help="Randomize, NUMBER = a value between 0 and 300") 
    parser.add_argument('-R', '--Renata', action='store_true', default=False, help="Renata's Randomizer (same as --random=0)")
    parser.add_argument('-sp', '--split', action='store_true', default=False, help="Save each patch in a separate file")
    parser.add_argument('-s', '--select', metavar='RANGE', help='Select patch RANGE to save')
    parser.add_argument('-S', '--sort', action='store_true', default=False, help='Sort patches by name, not case-sensitive')
    parser.add_argument('-S2', '--sort2', action='store_true', default=False, help='Sort patches by name, case-sensitive')
    parser.add_argument('--copy', nargs=2, metavar=('X', 'Y'), help='Copy patch nr X to nr Y')
    parser.add_argument('--swap', nargs=2, metavar=('X', 'Y'), help='Swap patch nr X and nr Y')
    parser.add_argument('-t', '--tx7', action='store_true', default=False, help='Save with TX7 Performance data')
    parser.add_argument('-v', '--version', action='version', version='{} ({})'.format(PROGRAMVERSION, PROGRAMDATE)) 
    parser.add_argument('-y', '--yamaha', metavar='MODEL', default='tx81z', help='Specify Yamaha synth MODEL for outfile') 
    parser.add_argument('infile', nargs='+', help='Selects input file(s)')
    parser.add_argument('outfile', help='Select output file')

    args=parser.parse_args()
    infilez = args.infile
    infiles = []
    for i in infilez:
        infiles += glob(i)
    outfile = args.outfile

    mid_in = dxcommon.MID_IN
    mid_out = dxcommon.MID_OUT
    CFG = dxcommon.CFG
    if os.getenv('MID_IN'):
        mid_in = os.getenv('MID_IN')
    mid_out = os.getenv('MID_OUT')
    if os.path.exists(CFG):
        with open(CFG, 'r') as f:
            for line in f.readlines():
                l = line.split('=')
                if l[0].strip() == 'MID_IN':
                    mid_in = l[1].strip()
                if l[0].strip() == 'MID_OUT':
                    mid_out = l[1].strip()

    if args.mid:
        mid_in = args.mid
        mid_out =  args.mid
    if args.mid_in:
        mid_in = args.mid_in
    if args.mid_out:
        mid_out = args.mid_out
    if args.mid_in or args.mid_out:
        with open(CFG, 'w') as f:
            if mid_in: f.write('MID_IN = {}\n'.format(mid_in))
            if mid_out: f.write('MID_OUT = {}\n'.format(mid_out))

    nosplit = args.nosplit
    ch = args.channel
    check = args.check
    select = args.select
    sort = args.sort
    sort2 = args.sort2
    swap = args.swap
    copy = args.copy
    nodupes = args.nodupes
    nodupes2 = args.nodupes2
    offset = args.offset
    deviation = max(-1, min(300, args.random))
    if args.Renata:
        deviation = 0
    find = args.find
    yamaha = args.yamaha.lower().strip()
    FB01 = False
    if args.split:
        split = 1
    elif yamaha in ('ys100', 'ys200', 'tq5', 'b200', 'ds55', 'v50'):
        split = 25
    elif yamaha in ('dx27s', 'dx27', 'dx27s', 'dx100'):
        split = 24
    elif yamaha == 'fb01' or os.path.splitext(outfile)[1].lower() == '.fb1':
        yamaha = 'fb01'
        FB01 = True
        split = 48
    elif yamaha == 'vopm' or os.path.splitext(outfile)[1].lower() == '.opm':
        yamaha = 'vopm'
        FB01 = True
        split = 128
    else:
        split = 32

    txdata = []
    for infile in infiles:
        print("Reading {}".format(infile))
        if not os.path.exists(infile):
            print("{} not found".format(infile))
            return 1
        if os.path.getsize(infile)>MAXFILESIZE:
            if MAXFILESIZE != 0:
                print("Warning: File too large.\nOnly {} bytes will be read".format(MAXFILESIZE))
        if infile == outfile:
            print("Must have different input and output files")
            return 1

        if os.path.isfile(infile):
            txdat, channel = TXC.read(infile, offset, check, yamaha, mid_in, mid_out)
            txdata += txdat


    if ch != None:
        channel = ch-1
        channel = max(0, channel)
        channel = min(15, channel)

    if nodupes2:
        nodupes = True
            
    if nodupes or nodupes2:
        if FB01:
            txdata = TXC.fbnodupes(txdata, nodupes2)
        else:
            txdata = TXC.txnodupes(txdata, nodupes2)

    if select != None: 
        txdat = []
        for i in dxcommon.range2list(select):
            if FB01:
                txdat += txdata[64*(i-1): 64*i]
            else:
                txdat += txdata[128*(i-1): 128*i]
        txdata = txdat
    
    if args.find != None:
        if FB01:
            txdata = TXC.fbfind(txdata, find)
        else:
            txdata = TXC.txfind(txdata, find)
    
    if deviation != -1:
        if FB01:
            txdata = TXC.fbrandom(txdata, deviation)
        else:
            txdata = TXC.txrandom(txdata, deviation)

    if sort:
        if FB01:
            txdata = TXC.fbsort(txdata, False)
        else:
            txdata = TXC.txsort(txdata, False)
    if sort2:
        if FB01:
            txdata = TXC.fbsort(txdata, True)
    if copy:
        if FB01:
            txdata = TXC.fbcopy(dxcommon.range2list(copy[0]), int(copy[1]), txdata)
        else:
            txdata = TXC.txcopy(dxcommon.range2list(copy[0]), int(copy[1]), txdata)

    if swap:
        if FB01:
            txdata = TXC.fbswap(int(swap[0]), int(swap[1]), txdata)
        else:
            txdata = TXC.txswap(int(swap[0]), int(swap[1]), txdata)

    if split == 1:
        if FB01:
            for i in range(len(txdata)//64):
                outfile_name = dxcommon.list2string(txdata[64*i:64*i+7])
                for j in range(len(outfile_name)):
                    if not outfile_name[j] in ALLOWED_CHARACTERS:
                        outfile_name = outfile_name[:j] + "_" + outfile_name[j+1:]
                count = 0
                Outfile_Name = outfile_name
                while os.path.exists(Outfile_Name+outfile):
                    count += 1
                    if count>1: Outfile_Name = outfile_name + "(" + str(count) + ")"

                outfile_name = os.path.join(os.path.split(outfile)[0], Outfile_Name + os.path.split(outfile)[1])

                TXC.write(outfile_name, txdata[64*i:64*(i+1)], channel, nosplit, 1, yamaha, mid_out)
 
        else:
            for i in range(len(txdata)//128):
                outfile_name = dxcommon.list2string(txdata[128*i+57:128*i+67])
                for j in range(len(outfile_name)):
                    if not outfile_name[j] in ALLOWED_CHARACTERS:
                        outfile_name = outfile_name[:j] + "_" + outfile_name[j+1:]
                count = 0
                Outfile_Name = outfile_name
                while os.path.exists(Outfile_Name+outfile):
                    count += 1
                    if count>1: Outfile_Name = outfile_name + "(" + str(count) + ")"

                outfile_name = os.path.join(os.path.split(outfile)[0], Outfile_Name + os.path.split(outfile)[1])

                TXC.write(outfile_name, txdata[128*i:128*(i+1)], channel, nosplit, 1, yamaha, mid_out)
    else:
        TXC.write(outfile, txdata, channel, nosplit, split, yamaha, mid_out)

    return 0


################### MAIN #####################

if __name__ == '__main__':
    sys.exit(cli_main())
    

