# oldsynth_patchmutator
    a utility to read Yahaha DX7 / alpha Juno patch files and mutate then using GP (Genetic Programming)


Genetic programming (GP) is a technique whereby representations of a space are encoded as a set of genes that are then modified (evolved) using an evolutionary algorithm (often a genetic algorithm, "GA")


In this case the solution space is a DX7/ a-juno synthesizer patch.

By providing "good" examples of patches and mutating/evolve/modify them new patches that are probably good will be created.


# DX7


In order to not duplicate effort initially a compiled c++ program that is converting the dx7 binary patch  bank format to text will be used.
This was created by Ted Felix (for more info have a look here -> http://tedfelix.com/yamaha-dx7/index.html)

the output looks a bit like this:
Sample output:

    - Filename:romfaves.syx
    - Voice #: 1
    - Name: MOOGBASS1
    - Algorithm: 5
    - Feedback: 1
    - LFO
    - LFOWave: Square
    - LFOSpeed: 35
    - LFODelay: 0
    - LFOPitch Mod Depth: 0
    - LFOAM Depth: 0
    - LFOSync: Off
    - LFOPitch Modulation Sensitivity: 0
    - Oscillator Key Sync: On
    - Pitch Envelope Generator
    - PEGRate 1: 0
    - PEGRate 2: 0
    - PEGRate 3: 0
    - PEGRate 4: 0
    - PEGLevel 1: 50

etc...


# a-juno


Function

     0 DCO Env. Mode [0=Normal, 1=Inverted, 2=Normal-Dynamic, 3=Inverted-Dynamic]
     1 VCF Env. Mode [0=Normal, 1=Inverted, 2=Normal-Dynamic, 3=Dynamic]
     2 VCA Env. Mode [0=Normal, 1=Gate, 2=Normal-Dynamic, 3=Gate-Dynamic]
     3 DCO Wave Pulse [0..3]
     4 DCO Wave Saw   [0..5]
     5 DCO Wave Sub   [0..5]
     6 DCO Range      [0=4', 1=8', 2=16', 3=32']
     7 DCO Sub Level  [0..3]
     8 DCO Noise      [0..3]
     9 HPF Cutoff     [0..3]
    10 Chorus Switch  [0=Off, 1=On]
    11 DCO LFO Mod.   [0..127]
    12 DCO ENV Mod.   [0..127]
    13 DCO After Mod. [0..127]
    14 DCO PWM Depth  [0..127]
    15 DCO PWM Rate   [0..127] 0 = Pulse Width Manual 1..127=PW LFO Rate
    16 VCF Cutoff     [0..127]
    17 VCF Resonance  [0..127]
    18 VCF LFO Mod.   [0..127]
    19 VCF ENV Mod.   [0..127]
    20 VCF Key Follow [0..127]
    21 VCF Aftertouch [0..127]
    22 VCA Level      [0..127]
    23 VCA Aftertouch [0..127]
    24 LFO Rate       [0..127]
    25 LFO Delay      [0..127]
    26 ENV T1         [0..127] Attack Time
    27 ENV L1         [0..127] Attack Level
    28 ENV T2         [0..127] Break Time
    29 ENV L2         [0..127] Break Level
    30 ENV T3         [0..127] Decay Time
    31 ENV L3         [0..127] Sustain Level
    32 ENV T4         [0..127] Release Time
    33 ENV Key Follow [0..127]
    34 Chorus Rate    [0..127]
    35 Bender Range   [0..12]








Once patches are in textual format with some minimal parsing the rest of the work will be done with

    pandas   (data munging powerhouse)
    DEAP     (a novel evolutionary computation framework)
    Mido     (MIDI Objects for Python)


Information of the dx7 binary format is also included in the repo for reference

another useful repo for similar work in C++ for DX7 is 

https://github.com/rogerallen/dxsyx

i would like to use python however
