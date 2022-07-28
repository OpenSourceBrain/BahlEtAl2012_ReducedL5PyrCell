from pyneuroml.neuron import export_to_neuroml2

import sys
import os

os.chdir("../NEURON/test")
sys.path.append(".")

export_to_neuroml2("Test_example1.hoc", 
                   "../../NeuroML2/init_model2.cell.nml", 
                   includeBiophysicalProperties=True,
                   known_rev_potentials={"na":60,"k":-90,"ca":140})
