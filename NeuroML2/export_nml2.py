from pyneuroml.neuron import export_to_neuroml2

import sys
import os

os.chdir("../NEURON/init_models_with_ca")
sys.path.append(".")

export_to_neuroml2("init_model2.hoc", 
                   "../../NeuroML2/init_model2.cell.nml", 
                   includeBiophysicalProperties=False,
                   known_rev_potentials={"na":60,"k":-90,"ca":140})
