About using wav2cas with DXconvert version >= 2.1.4
==================================================

Some of the older Yamaha synths had a Cassette Tape interface. This was a 
method to store/retrieve computer/synthesizer data using a cassette tape 
recorder. The encoding/decoding technique was similar to that used by MSX 
computers.

Yamaha's DX9, TX81Z, TX7 and DX100/27/21 for example have such an 
interface. The Yamaha DX7 had RAM cartridges, which are a much faster and 
more reliable method to store patchdata. Also MIDI SysEx storage using a
(USB-)MIDI interface and a computer is a much better and safer method. 

It is now possible using DXconvert/TXconvert to convert data from the 
old cassette tapes to SysEx data files. Let's do this quickly, before 
these vulnarable magnetic tapes will be totally unreadable.

What to do and what you need
============================
1. Digitally record the audio output of the cassette recordings to WAV 
files. Carefully adjust the recording level for best S/N ratio without 
distortion.

2. Clean up the WAV files in an audio editor. Cut away irrelevant audio 
like voice announcements "shhhshshh Hi guys, recording is starting in 2
 seconds sshhhh pprrr". Save only the 1200/2400 baud beep sequence from 
the cassette interface as MONO (!) wav file. If the tape recording 
contains several dump sequences, save them to separate WAV files.

3. Get yourself the castools from this website:
http://home.kabelfoon.nl/~vincentd/
There are Windows binaries, or source code. 

If you want to compile yourself from source: 
if you want 64 bits version you might have to modify
wav2cas.c. I had it working after replacing "float" with "int" 
using gcc on a 64bits Linux system. 

4. Put the wav2cas(.exe) binary in your DXconvert directory or in your 
PATH. 

5. Try a conversion using dxconvert/txconvert directly.
   e.g. dxconvert infile.wav outfile.txt
	txconvert infile.wav outfile.txt

(you can also use the gui version if you prefer) Check the output. If 
it looks OK with a list of patchnames, you are on the right track. Then 
you can convert to syx.

6. If step 5 fails try using the wav2cas utility to convert the WAV file 
to a CAS file first. There are some commandline parameters to experiment 
with to get the best result. In your terminal type "wav2cas" and you will 
get a list of options. Important ones are -p, -t and -e. DX/TXconvert uses 
by default "-p -e 4 -t 10". But some files should be converted without -p 
and/or with other -e and -t values.

7. Convert the CAS file from step 6 to a .txt file. If not all patchnames 
look correct go back to step 6 and try other parameter settings until 
everything looks ok. Now convert the correct CAS file to sysex:
	dxconvert infile.cas outfile.syx
 	txconvert infile.cas outfile.syx


I hope this helps to save the content of your valuable cassette data tapes 
for the future!


