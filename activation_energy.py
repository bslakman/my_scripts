#Script written by Pierre, and modified by Belinda.

from cclib import parser
import argparse
import collections
import os

solventList = ["", "_water", "_n-octane", "_benzene", "_pyridine", "_tetrahydrofuran", "_dichloromethane", "_acetonitrile", "_dimethylsulfoxide"]

clParser = argparse.ArgumentParser(description="""
Given a reaction family and reactants, will get TS energies from Gaussian output files in
different solvents
""")
clParser.add_argument("-f", "--family", default="H_Abs", help="Name of the family")
clParser.add_argument("-r", "--reactants", nargs='+', help="list of reactants (strings)")
clParser.add_argument("-o", "--optional", default = "", nargs='+', help="""
optional stuff that tells you about the reacting site like CH or prim...
""")
args = clParser.parse_args()
directory = os.path.join(os.getcwd(), args.family, "+".join(args.reactants), *args.optional)
r1_loc = os.path.join(os.getcwd(), "species", args.reactants[0])
if len(args.reactants) > 1:
    r2_loc = os.path.join(os.getcwd(), "species", args.reactants[1])

for solvent in solventList:
    print "Solvent: " + solvent
    reactantOutput = r1_loc + solvent + ".log"
    if len(args.reactants) > 1:
        reactant2Output = r2_loc + solvent + ".log"
    tsOutput = directory + "ts" + solvent + ".log"

    rParse = parser.Gaussian(reactantOutput)
    tsParse = parser.Gaussian(tsOutput)

    rParse = rParse.parse()
    tsParse = tsParse.parse()

    # In Hartrees
    reactantE = rParse.scfenergies[-1]/27.2113845
    tsE = tsParse.scfenergies[-1]/27.2113845
    tsVib = tsParse.vibfreqs[0]

    if reactant2Output is not None:
        r2Parse = parser.Gaussian(reactant2Output)
        r2Parse = r2Parse.parse()
        reactant2E = r2Parse.scfenergies[-1]/27.2113845
    else:
        reactant2E = 0.0

    Ea = (tsE - reactantE - reactant2E) * 2600
    if solvent is "":
        gasEa = Ea
    diffEa = Ea - gasEa

    rString = 'Reactant energy = ' + str(reactantE)
    r2String = 'Reactant 2 energy = ' + str(reactant2E)
    tEnergy = 'TS energy       = ' + str(tsE)
    EaString = 'Activation energy (in kJ/mol)     = ' + str(Ea)
    tVib    = 'TS vib          = ' + str(tsVib)
    diffString = 'Difference in activation energy from gas phase (in kJ/mol)   = ' + str(diffEa)

    outputDataFile = "SMD/H_Abs/OOH_C3OH/CH/sec/output" + solvent+ ".txt"

    with open(outputDataFile, 'w') as parseFile:
        parseFile.write('The energies of the species in Hartree are:')
        parseFile.write('\n')
        parseFile.write(rString)
        parseFile.write('\n')
        parseFile.write(r2String)
        parseFile.write('\n')
        parseFile.write(tEnergy)
        parseFile.write('\n')
        parseFile.write(tVib)
        parseFile.write('\n')
        parseFile.write(EaString)
        parseFile.write('\n')
        parseFile.write(diffString)
