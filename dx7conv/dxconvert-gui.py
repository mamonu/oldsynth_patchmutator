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
from DXconvert import DXC
from DXconvert import dxcommon
MAXFILESIZE=dxcommon.MAXFILESIZE
PROGRAMNAME=DXC.PROGRAMNAME
PROGRAMVERSION=dxcommon.PROGRAMVERSION
PROGRAMDATE=dxcommon.PROGRAMDATE
ALLOWED_CHARACTERS=dxcommon.ALLOWED_CHARACTERS

LOGO='DXconvert/dxconvert.gif'
HELP='DXconvert/dxconvert.help'
MIDILOGO='DXconvert/midi.gif'
for p in ['DXconvert']+sys.path:
    _logo = os.path.join(p, 'DXconvert/dxconvert.gif')
    if os.path.exists(_logo):
        LOGO=_logo
        break
for p in ['DXconvert']+sys.path:
    _help = os.path.join(p, 'DXconvert/dxconvert.help')
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


class dx7ConvertDialog(tkinter.Frame):
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
        self.inpath.grid(row=ROW, column=COLUMN, columnspan=4, sticky=W)
        button = tkinter.Button(body, text="...", command=self.get_inpath)
        button.grid(row=ROW, column=5)

        ROW+=1
        tkinter.Label(body, text='Output file:').grid(row=ROW, sticky=W)
        self.outpath = tkinter.Entry(body, width=50)
        self.outpath.grid(row=ROW, column=COLUMN, columnspan=4, sticky=W)
        button = tkinter.Button(body, text="...", command=self.get_outpath)
        button.grid(row=ROW, column=5)
    
        ROW+=1
        tkinter.Label(body, text='Options:').grid(row=ROW, sticky=W)
        self.dx72 = tkinter.BooleanVar()

        self.dx72_button = tkinter.Checkbutton(body, text="--dx72", variable=self.dx72)
        self.dx72_button.grid(row=ROW, column=COLUMN, pady=5, sticky=W)

        ROW+=1
        self.TX7=tkinter.BooleanVar()
        self.tx7_button=tkinter.Checkbutton(body, text="--tx7", variable=self.TX7)
        self.tx7_button.grid(row=ROW, column=COLUMN, pady=5, sticky=W)

        ROW+=1
        self.split=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--split", variable=self.split).grid(row=ROW, column=COLUMN, pady=5, sticky=W)

        ROW+=1
        self.nosplit=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--nosplit", variable=self.nosplit).grid(row=ROW, column=COLUMN, pady=5, sticky=W)

        ROW=3
        COLUMN+=1
        self.check=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--check", variable=self.check).grid(row=ROW, column=COLUMN, pady=5, sticky=W)

        ROW+=1
        self.sort=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--sort", variable=self.sort).grid(row=ROW, column=COLUMN, pady=5, sticky=W)

        ROW+=1
        self.nodupes=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--nodupes", variable=self.nodupes).grid(row=ROW, column=COLUMN, pady=5, sticky=W)

        ROW+=1
        self.nodupes2=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--nodupes2", variable=self.nodupes2).grid(row=ROW, column=COLUMN, pady=5, sticky=W)
 
        ROW=3
        COLUMN+=1
        self.bc2at=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--bc2at", variable=self.bc2at).grid(row=ROW, column=COLUMN, pady=5, sticky=W)

        ROW+=1
        self.fc1=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--fc1", variable=self.fc1).grid(row=ROW, column=COLUMN, pady=5, sticky=W)

        ROW+=1
        self.fc2=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--fc2", variable=self.fc2).grid(row=ROW, column=COLUMN, pady=5, sticky=W)

        ROW+=1
        self.bc=tkinter.BooleanVar()
        tkinter.Checkbutton(body, text="--bc", variable=self.bc).grid(row=ROW, column=COLUMN, pady=5, sticky=W)
 
        ROW=3
        COLUMN+=1
        tkinter.Label(body, text="--select <RANGE>:").grid(row=ROW, column=COLUMN, pady=5, sticky=W)
        self.select = tkinter.Entry(body, width=5)
        self.select.grid(row=ROW, column=COLUMN+1, sticky=W)

        ROW+=1
        tkinter.Label(body, text="--channel <1~16>:").grid(row=ROW, column=COLUMN, pady=5, sticky=W)
        self.channel = tkinter.Entry(body, width=5)
        self.channel.grid(row=ROW, column=COLUMN+1, sticky=W)
 
        ROW+=1
        tkinter.Label(body, text="--offset <value>:").grid(row=ROW, column=COLUMN, pady=5, sticky=W)
        self.offset = tkinter.Entry(body, width=5)
        self.offset.grid(row=ROW, column=COLUMN+1, sticky=W)
      
        ROW+=1
        tkinter.Label(body, text="--random <0~300>:").grid(row=ROW, column=COLUMN, pady=5, sticky=W)
        self.random = tkinter.Entry(body, width=5)
        self.random.grid(row=ROW, column=COLUMN+1, sticky=W)
        
        ROW+=1
        COLUMN=2
        tkinter.Label(body, text='--find <string>:').grid(row=ROW, column=COLUMN, columnspan=2, pady=2, sticky=W)
        self.dxfind = tkinter.Entry(body, width=10)
        self.dxfind.grid(row=ROW, column=COLUMN+1, sticky=W, pady=5)

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
            parent=None, title='Select DX/TX file(s) to convert', 
            defaultextension='.syx', 
            filetypes=[('All files', '.*'), 
                ('System Exclusive', '.syx'), 
                ('raw DX7 headerless', '.dx7'), 
                ('Sysex in MIDI file', '.mid')]
            )

        if inpath:
            self.inpath.delete(0, END)
            self.inpath.insert(0, inpath)
        return

    def get_outpath(self):
        outpath = tkinter.filedialog.asksaveasfilename(
            parent=None, title='Select DX7 export name/filetype', 
            defaultextension='.syx', 
            filetypes=[('All files', '.*'), 
                ('System Exclusive', '.syx'), 
                ('Raw DX7 (4096 bytes)', '.dx7'), 
                ('Midifile format 0', '.mid'), 
                ('Voicelist or Parameterlist', '.txt')]
            )

        if outpath:
            outpath = os.path.normpath(outpath)
            self.outpath.delete(0, END)
            self.outpath.insert(0, outpath)
            if outpath[-4:].lower() == '.dx7':
                self.dx72_button.config(state=DISABLED)
                self.tx7_button.config(state=DISABLED)
            else:
                self.dx72_button.config(state=NORMAL)
                self.tx7_button.config(state=NORMAL)
        return

    def convert(self):
        self.status['text'] = '......'
        
        inpath = self.inpath.get()
        if not inpath:
           message = 'No input file(s) selected'
           tkinter.messagebox.showerror("DXconvert-{}".format(PROGRAMVERSION), message)
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
            tkinter.messagebox.showerror("DXconvert-{}".format(PROGRAMVERSION), message)
            self.status['text'] = 'Select file(s) for conversion'
            return

        self.status['text'] = 'Reading ...'
        self.update()
        dx7data = []
        dx72data = []
        tx7data = []
        offset = 0
        channel=0
        if self.offset.get():
            offset = max(0, int(self.offset.get()))

        for inp in inpath:
            inp = os.path.normpath(inp)
            if os.path.isfile(inp):

                if os.path.getsize(inp)>MAXFILESIZE: 
                    if MAXFILESIZE != 0:
                        self.status['text'] =  "Warning: only {} bytes will be read".format(MAXFILESIZE)

                dx7dat, dx72dat, tx7dat, channel=DXC.read(inp, offset, self.check.get, self.mid_in, self.mid_out)
                dx7data += dx7dat
                dx72data += dx72dat
                tx7data += tx7dat
                self.status['text'] = 'Read {}'.format(inp)
                self.update()

        if self.channel.get():
            channel = min(15, max(0, int(self.channel.get())-1))

        if self.select.get():
            dx7dat, dx72dat, tx7dat = [], [], []
            for i in dxcommon.range2list(self.select.get()):
                dx7dat += dx7data[128*(i-1):128*i]
                dx72dat += dx72data[35*(i-1):35*i]
                tx7dat += dx7data[64*(i-1):64*i]
            dx7data, dx72data, tx7data = dx7dat, dx72dat, tx7dat

        if self.dxfind.get():
            self.status['text'] = 'Searching names ...'
            self.update()
            dx7data, dx72data, tx7data = DXC.dxfind(dx7data, dx72data, tx7data, self.dxfind.get())

        if self.random.get():
            self.status['text'] = "Randomizing voices ..."
            self.update()
            deviation = max(0, min(300, int(self.random.get())))
            dx7data = DXC.dxrandom(dx7data, deviation)

        if self.nodupes2.get() == True:
            nodupes2 = True
        else:
            nodupes2 = False

        if (self.nodupes.get() == True) or (self.nodupes2.get() == True):
            self.status['text'] = "Removing duplicates ..."
            self.update()
            dx7data, dx72data, tx7data = DXC.dxnodupes(dx7data, dx72data, tx7data, self.dx72.get(), self.TX7.get(), nodupes2)

        if self.sort.get() == True:
            self.status['text'] = "Sorting voices by name ..."
            self.update()
            dx7data, dx72data, tx7data = DXC.dxsort(dx7data, dx72data, tx7data, self.dx72.get(), self.TX7.get())
        
        for i in range(len(dx7data)//128):
            if self.bc2at.get() == True:
                dx72data[20+35*i:24+35*i] = dx72data[16+35*i:20+35*i]
            if self.fc1.get() == False:
                dx72data[12+35*i:16+35*i] = [0, 0, 0, 0]
            if self.fc2.get() == False:
                dx72data[26+35*i:30+35*i] = [0, 0, 0, 0]
            if self.bc.get() == False:
                dx72data[16+35*i:20+35*i] = [0, 0, 0, 50]

        if self.split.get() == True:
            count = 0
            for i in range(len(dx7data)//128):
                outfile_name = dxcommon.list2string(dx7data[128*i+118:128*i+128])
                for j in range(len(outfile_name)):
                    if not outfile_name[j] in ALLOWED_CHARACTERS:
                        outfile_name = outfile_name[:j] + "_" + outfile_name[j+1:]
                Outfile_Name = outfile_name
                while os.path.exists(Outfile_Name+outpath):
                    count += 1
                    if count>1: Outfile_Name = outfile_name + "(" + str(count) + ")"

                outfile_name = os.path.join(os.path.split(outpath)[0], Outfile_Name + os.path.split(outpath)[1])


                DXC.write(outfile_name, dx7data[128*i:128*(i+1)], dx72data[35*i:35*(i+1)], tx7data[64*i:64*(i+1)], self.dx72.get(), self.TX7.get(), channel, self.nosplit.get(), self.mid_out)
            message = "Ready. {} Patches written.".format(len(dx7data)//128)
        else:
            message = DXC.write(outpath, dx7data, dx72data, tx7data, self.dx72.get(), self.TX7.get(), channel, self.nosplit.get(), self.mid_out)

        self.status['text'] = 'Converting ...'
        self.update()

        tkinter.messagebox.showinfo("DXconvert-{}".format(PROGRAMVERSION), message)
        self.status['text'] = 'Select file(s) for conversion'
        self.update()
        return
    
    def info(self):
        mw = tkinter.Tk()
        mw.title('HELP') 
        txt = ScrolledText(mw, width=85, height=35)
        txt.pack()
        with open(HELP) as f:
            txt.insert(END, '\n    DXconvert-{} ({})\n'.format(PROGRAMVERSION, PROGRAMDATE))
            for line in f:
                txt.insert(END, line)
        txt.config(state=DISABLED)
        return

def gui_main():
    root = tkinter.Tk()
    root.title("{}-{}".format(PROGRAMNAME, PROGRAMVERSION))
    root.resizable(True, False)
    root.minsize(300, 0)
    dx7ConvertDialog(root).pack(fill=X, expand=1)
    root.mainloop()
    return 0


################### MAIN #####################

if __name__ == '__main__':
    sys.exit(gui_main())
    

