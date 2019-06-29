#!/usr/bin/env python3
"""
dxconvert-gui.py

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
from DXconvert import TXC
from DXconvert import dxcommon

MAXFILESIZE=dxcommon.MAXFILESIZE
PROGRAMNAME=TXC.PROGRAMNAME
PROGRAMVERSION=dxcommon.PROGRAMVERSION
PROGRAMDATE=dxcommon.PROGRAMDATE
ALLOWED_CHARACTERS=dxcommon.ALLOWED_CHARACTERS

LOGO='DXconvert/txconvert.gif'
HELP='DXconvert/txconvert.help'
MIDILOGO='DXconvert/midi.gif'
for p in ['DXconvert']+sys.path:
    _logo = os.path.join(p, 'DXconvert/txconvert.gif')
    if os.path.exists(_logo):
        LOGO=_logo
        break
for p in ['DXconvert']+sys.path:
    _help = os.path.join(p, 'DXconvert/txconvert.help')
    if os.path.exists(_help):
        HELP=_help
        break
for p in ['DXconvert']+sys.path:
    _midilogo = os.path.join(p, 'DXconvert/midi.gif')
    if os.path.exists(_midilogo):
        MIDILOGO=_midilogo
        break

############ GUI ##############

import tkinter
from tkinter.constants import *
import tkinter.filedialog
import tkinter.messagebox
from tkinter.scrolledtext import ScrolledText


class txConvertDialog(tkinter.Frame):
    def __init__(self, root):
        tkinter.Frame.__init__(self, root, border=5)
        self.status = tkinter.Label(self, text='Select file(s) for conversion')
        self.status.pack(fill=X, expand=1)
        body = tkinter.Frame(self)
        body.pack(fill=X, expand=1)
        sticky = E + W
        body.grid_columnconfigure(1, weight=2)

        ROW=1
        COLUMN=1
        tkinter.Label(body, text='Input file(s):').grid(row=ROW, sticky=W)
        self.inpath = tkinter.Entry(body, width=50)
        self.inpath.grid(row=ROW, column=COLUMN, columnspan=5, sticky=W)
        button = tkinter.Button(body, text="...", command=self.get_inpath)
        button.grid(row=ROW, column=5)

        ROW+=1
        tkinter.Label(body, text='Output file:').grid(row=ROW, sticky=W)
        self.outpath = tkinter.Entry(body, width=50)
        self.outpath.grid(row=ROW, column=COLUMN, columnspan=5, sticky=W)
        button = tkinter.Button(body, text="...", command=self.get_outpath)
        button.grid(row=ROW, column=5)
    
        ROW+=1
        tkinter.Label(body, text='Options:').grid(row=ROW, sticky=W)

        
        ROW=3
        COLUMN=1

        SYNTHS = ('DX100', 'DX27', 'DX21', 'TX81Z', 'WT11', 'DX11', 'FB01', 
                    'YS100', 'YS200', 'TQ5', 'B200', 'DS55', 'V50', 'VOPM')
        self.yamaha = tkinter.StringVar()
        self.yamaha.set('tx81z')
        for s in SYNTHS:
            if s == 'YS100':
                ROW=3
                COLUMN += 1
            self.yamaha_rb = tkinter.Radiobutton(body, text=s, variable=self.yamaha, value=s.lower()) 
            self.yamaha_rb.grid(row=ROW, column=COLUMN, pady=5, sticky=W)
            ROW += 1


        ROW = 3
        COLUMN = 3
        self.check=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--check", variable=self.check).grid(row=ROW, column=COLUMN, pady=5, sticky=W)

        ROW += 1
        self.sort=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--sort", variable=self.sort).grid(row=ROW, column=COLUMN, pady=5, sticky=W)

        ROW += 1
        self.nodupes=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--nodupes", variable=self.nodupes).grid(row=ROW, column=COLUMN, pady=5, sticky=W)

        ROW += 1
        self.nodupes2=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--nodupes2", variable=self.nodupes2).grid(row=ROW, column=COLUMN, pady=5, sticky=W)
        
        ROW += 1
        self.nosplit=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--nosplit", variable=self.nosplit).grid(row=ROW, column=COLUMN, pady=5, sticky=W)
        
        ROW += 1
        self.split=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--split", variable=self.split).grid(row=ROW, column=COLUMN, pady=5, sticky=W)
        
        ROW = 3
        COLUMN = 4

        tkinter.Label(body, text="--select RANGE:").grid(row=ROW, column=COLUMN, pady=5, sticky=W)
        self.select = tkinter.Entry(body, width=5)
        self.select.grid(row=ROW, column=COLUMN+1, sticky=W)

        ROW += 1
        tkinter.Label(body, text="--channel <1~16>:").grid(row=ROW, column=COLUMN, pady=5, sticky=W)
        self.channel = tkinter.Entry(body, width=5)
        self.channel.grid(row=ROW, column=COLUMN+1, sticky=W)
 
        ROW += 1
        tkinter.Label(body, text="--offset <value>:").grid(row=ROW, column=COLUMN, pady=5, sticky=W)
        self.offset = tkinter.Entry(body, width=5)
        self.offset.grid(row=ROW, column=COLUMN+1, sticky=W)
      
        ROW += 1
        tkinter.Label(body, text="--random <0~300>:").grid(row=ROW, column=COLUMN, pady=5, sticky=W)
        self.random = tkinter.Entry(body, width=5)
        self.random.grid(row=ROW, column=COLUMN+1, sticky=W)
        
        ROW = 9
        COLUMN = 3
        tkinter.Label(body, text='--find <string>: ').grid(row=ROW, column=COLUMN, columnspan=1, pady=2, padx=10, sticky=W)
        self.txfind = tkinter.Entry(body, width=10)
        self.txfind.grid(row=ROW, column=COLUMN+1, columnspan=2, sticky=W, pady=5)


        buttons = tkinter.Frame(self)
        buttons.pack()
        tkinter.Frame(buttons, width=15).pack(side=LEFT)

        button = tkinter.Button(
            buttons, text="Help?", width=8, activeforeground='blue', command=self.info)
        button.pack(side=LEFT, pady=15, padx=15)
        
        if os.path.exists(LOGO):
            picture = tkinter.PhotoImage(file=LOGO)
            button = tkinter.Button(buttons, image=picture, width=100, height=45, command=self.convert)
            button.picture = picture
            button.pack(side=LEFT)
        else:
            button = tkinter.Button(
                buttons, text="CONVERT!", width=8, fg='green', command=self.convert)
            button.pack(side=LEFT, pady=15, padx=15)

        if dxcommon.ENABLE_MIDI:
            self.mid_in = dxcommon.MID_IN
            self.mid_out = dxcommon.MID_OUT
            if os.getenv('MID_IN'):
                self.mid_in = os.getenv('MID_IN')
            self.mid_out = os.getenv('MID_OUT')
            if os.path.exists('dxtxmidi.cfg'):
                with open('dxtxmidi.cfg', 'r') as f:
                    for line in f.readlines():
                        l = line.split('=')
                        if l[0].strip() == 'MID_IN':
                            self.mid_in = l[1].strip()
                        if l[0].strip() == 'MID_OUT':
                            self.mid_out = l[1].strip()
        
            if os.path.exists(MIDILOGO):
                picture = tkinter.PhotoImage(file=MIDILOGO)
                button = tkinter.Button(
                        buttons, image=picture, width=32, height=32, relief='flat', command=self.midiconf)
                button.picture = picture
                button.pack(side=LEFT, pady=15, padx=15)
            else:
                button = tkinter.Button(
                        buttons, text="MIDI", width=8, command=self.midiconf)
                button.pack(side=LEFT, pady=15, padx=15)
        else:
            self.mid_in = None
            self.mid_out = None

        button = tkinter.Button(
                buttons, text="Quit", width=8, activeforeground='red', command=self.quit)
        button.pack(side=LEFT, pady=15, padx=15)


        return
        
    def midiconf(self):
        dxcommon.Midiconf()
        if os.path.exists('dxtxmidi.cfg'):
            with open('dxtxmidi.cfg', 'r') as f:
                for line in f.readlines():
                    l = line.split('=')
                    if l[0].strip() == 'MID_IN':
                        self.mid_in = l[1].strip()
                    if l[0].strip() == 'MID_OUT':
                        self.mid_out = l[1].strip()
 
        return


    def get_inpath(self):
        inpath = tkinter.filedialog.askopenfilenames(
            parent=None, title='Select DX/TX/FB file(s) to convert', 
            defaultextension='.syx', 
            filetypes=[('All files', '.*'), 
                ('System Exclusive', '.syx'), 
                ('Sysex in MIDI file', '.mid')]
            )

        if inpath:
            self.inpath.delete(0, END)
            self.inpath.insert(0, inpath)
        return

    def get_outpath(self):
        if self.yamaha.get().lower() == 'fb01':
            outpath = tkinter.filedialog.asksaveasfilename(
                parent=None, title='Select FB01 export name/filetype', 
                defaultextension='.syx', 
                filetypes=[('All files', '.*'), 
                    ('System Exclusive', '.syx'), 
                    ('Raw FB01 (3072 bytes)', '.fb1'), 
                    ('Midifile format 0', '.mid'), 
                    ('Voicelist or Parameterlist', '.txt')]
                )
        elif self.yamaha.get().lower() == 'vopm':
            outpath = tkinter.filedialog.asksaveasfilename(
                parent=None, title='VOPM export name/filetype', 
                defaultextension='.opm', 
                filetypes=[('VOPM voice data', '.opm'), 
                    ('All files', '.*')]
                )
        else:
            outpath = tkinter.filedialog.asksaveasfilename(
                parent=None, title='Select DX/TX export name/filetype', 
                defaultextension='.syx', 
                filetypes=[('All files', '.*'), 
                    ('System Exclusive', '.syx'), 
                    ('Raw VMEM data file (4096 bytes)', '.dxx'), 
                    ('Midifile format 0', '.mid'), 
                    ('Voicelist or Parameterlist', '.txt')]
                )

        if outpath:
            outpath = os.path.normpath(outpath)
            self.outpath.delete(0, END)
            self.outpath.insert(0, outpath)
        return

    def convert(self):
        self.status['text'] = '......'
        
        inpath = self.inpath.get()
        if not inpath:
           message = 'No input file(s) selected'
           tkinter.messagebox.showerror("TXconvert-{}".format(PROGRAMVERSION), message)
           self.status['text'] = 'Select file(s) for conversion'
           return
       
        # Workaround for tkFileDialog.askopenfilesnames bug
        # Hopefully one day this will not be needed anymore
        if type(inpath) == str:
            master = tkinter.Tk()
            master.withdraw()
            inpath = master.tk.splitlist(inpath)

        outpath = self.outpath.get()
        if not outpath:
            message = 'No output files selected'
            tkinter.messagebox.showerror("TXconvert-{}".format(PROGRAMVERSION), message)
            self.status['text'] = 'Select file(s) for conversion'
            return

        self.status['text'] = 'Reading ...'
        self.update()
        txdata = []
        offset = 0
        channel=0

        if self.offset.get():
            offset = max(0, int(self.offset.get()))

        FB01 = False
        if self.yamaha.get():
            yamaha = self.yamaha.get().lower()
        if yamaha in ('dx100', 'dx27', 'dx27s'):
            split = 24
        elif yamaha in ('ds55', 'ys100', 'ys200', 'tq5', 'b200', 'v50'):
            split = 25
        elif yamaha == 'fb01':
            split = 48
            FB01 = True
        elif yamaha == 'vopm':
            split == 128
            FB01 = True
        else:
            split = 32


        for inp in inpath:
            inp = os.path.normpath(inp)
            if os.path.isfile(inp):

                if os.path.getsize(inp)>MAXFILESIZE: 
                    if MAXFILESIZE != 0:
                        self.status['text'] =  "Warning: only {} bytes will be read".format(MAXFILESIZE)

                txdat, channel=TXC.read(inp, offset, self.check.get(), yamaha, self.mid_in, self.mid_out)
                txdata += txdat
                self.status['text'] = 'Read {}'.format(inp)
                self.update()

        if self.channel.get():
            channel = min(15, max(0, int(self.channel.get())-1))

        if self.nodupes2.get() == True:
            nodupes2 = True
        else:
            nodupes2 = False

        if self.select.get():
            txdat = []
            for i in dxcommon.range2list(self.select.get()):
                if FB01:
                    txdat += txdata[64*(i-1):64*i]
                else:
                    txdat += txdata[128*(i-1):128*i]
            txdata = txdat

        if self.txfind.get():
            self.status['text'] = 'Searching names ...'
            self.update()
            if FB01:
                txdata = TXC.fbfind(txdata, self.txfind.get())
            else:
                txdata = TXC.txfind(txdata, self.txfind.get())

        if self.random.get():
            self.status['text'] = "Randomizing voices ..."
            self.update()
            deviation = max(0, min(300, int(self.random.get())))
            if FB01:
                txdata = TXC.fbrandom(txdata, deviation)
            else:
                txdata = TXC.txrandom(txdata, deviation)

        if (self.nodupes.get() == True) or (self.nodupes2.get() == True):
            self.status['text'] = "Removing duplicates ..."
            self.update()
            if FB01:
                txdata = TXC.fbnodupes(txdata, nodupes2)
            else:
                txdata = TXC.txnodupes(txdata, nodupes2)
        
        if self.sort.get() == True:
            self.status['text'] = "Sorting voices by name ..."
            self.update()
            if FB01:
                txdata = TXC.fbsort(txdata)
            else:
                txdata = TXC.txsort(txdata)
        
        if self.split.get() == True:
            if FB01:
                count = 0
                for i in range(len(txdata)//64):
                    outfile_name = dxcommon.list2string(txdata[64*i:64*i+7])
                    for j in range(len(outfile_name)):
                        if not outfile_name[j] in ALLOWED_CHARACTERS:
                            outfile_name = outfile_name[:j] + "_" + outfile_name[j+1:]
                    Outfile_Name = outfile_name
                    while os.path.exists(Outfile_Name+outpath):
                        count += 1
                        if count>1: Outfile_Name = outfile_name + "(" + str(count) + ")"

                    outfile_name = os.path.join(os.path.split(outpath)[0], Outfile_Name + os.path.split(outpath)[1])
                    TXC.write(outfile_name, txdata[64*i:64*(i+1)], channel, self.nosplit.get(), 1, yamaha, self.mid_out)
                message = "Ready. {} Patches written.".format(len(txdata)//128)
            else:
                count = 0
                for i in range(len(txdata)//128):
                    outfile_name = dxcommon.list2string(txdata[128*i+57:128*i+67])
                    for j in range(len(outfile_name)):
                        if not outfile_name[j] in ALLOWED_CHARACTERS:
                            outfile_name = outfile_name[:j] + "_" + outfile_name[j+1:]
                    Outfile_Name = outfile_name
                    while os.path.exists(Outfile_Name+outpath):
                        count += 1
                        if count>1: Outfile_Name = outfile_name + "(" + str(count) + ")"

                    outfile_name = os.path.join(os.path.split(outpath)[0], Outfile_Name + os.path.split(outpath)[1])
                    TXC.write(outfile_name, txdata[128*i:128*(i+1)], channel, self.nosplit.get(), 1, yamaha, self.mid_out)
                message = "Ready. {} Patches written.".format(len(txdata)//128)
        else:
            message = TXC.write(outpath, txdata, channel, self.nosplit.get(), split, yamaha, self.mid_out)


        self.status['text'] = 'Converting ...'
        self.update()

        tkinter.messagebox.showinfo("TXconvert-{}".format(PROGRAMVERSION), message)
        self.status['text'] = 'Select file(s) for conversion'
        self.update()
        return

    def info(self):
        mw = tkinter.Tk()
        mw.title('HELP') 
        txt = ScrolledText(mw, width=85, height=34)
        txt.pack()
        with open(HELP) as f:
            txt.insert(END, '\n    TXconvert-{} ({})\n'.format(PROGRAMVERSION, PROGRAMDATE))
            for line in f:
                txt.insert(END, line)
        txt.config(state=DISABLED)
        return

def gui_main():
    root = tkinter.Tk()
    root.title("{}-{}".format(PROGRAMNAME, PROGRAMVERSION))
    root.resizable(True, False)
    root.minsize(300, 0)
    txConvertDialog(root).pack(fill=X, expand=1)
    root.mainloop()
    return 0


################### MAIN #####################

if __name__ == '__main__':
    sys.exit(gui_main())
    

