# oldsynth_patchmutator
    a utility to read Yahaha DX7 / alpha Juno patch files and mutate then using GP (Genetic Programming)


Genetic programming (GP) is a technique whereby representations of a space are encoded as a set of genes that are then modified (evolved) using an evolutionary algorithm (often a genetic algorithm, "GA")


In this case the solution space is a DX7 synthesizer patch.

By providing "good" examples of patches and mutating/evolve/modify them new patches that are probably good will be created.

In order to not duplicate effort initially a c++ program is converting the dx7 binary patch  bank format to text will be used.
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

Once patches are in textual format with some minimal parsing the rest of the work will be done with

    pandas   (data munging powerhouse)
    DEAP     (a novel evolutionary computation framework)
    Mido     (MIDI Objects for Python)


Information of the dx7 binary format is also included in the repo for reference

another useful repo for similar work in C++ for DX7 is 

https://github.com/rogerallen/dxsyx

i would like to use python however
