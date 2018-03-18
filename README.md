# dx7patchmutator
    a utility to read a yahaha dx7 patch file and mutate it using GP (Genetic Programming)


Genetic programming (GP) is a technique whereby representations of a space are encoded as a set of genes that are then modified (evolved) using an evolutionary algorithm (often a genetic algorithm, "GA")


In this case the solution space is a DX7 synthesizer patch.

By providing "good" examples of patches and mutating/evolve/modify them new patches that are probably good will be created.

In order to not duplicate effort initially a c++ program is converting the dx7 binary patch  bank format to text will be used.

Once patches are in textual format the rest of the work will be done with
* pandas   (data munging powerhouse)
* DEAP     (a novel evolutionary computation framework)
* Mido     (MIDI Objects for Python)



