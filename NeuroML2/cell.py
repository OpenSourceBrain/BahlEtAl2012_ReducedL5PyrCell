# %%
import math
from neuroml import NeuroMLDocument
from neuroml import Cell
from neuroml import BiophysicalProperties
from neuroml import MembraneProperties
from neuroml import IncludeType
from neuroml import ChannelDensity
from neuroml import SpikeThresh
from neuroml import SpecificCapacitance
from neuroml import InitMembPotential
from neuroml import IntracellularProperties
from neuroml import Resistivity
from neuroml import Resistivity
from neuroml import Morphology, Segment, Point3DWithDiam
from pyneuroml import pynml
from pyneuroml.lems import LEMSSimulation
import os

# %%
print(os.getcwd())

# %%
def create_cell():
    pyr_cell_doc = NeuroMLDocument(id='cell', notes="Layer 5 Pyramidal cell")
    pyr_cell_fn = "pyr5_cell.nml"
    print(os.getcwd())
    pyr_cell_doc.includes.append(IncludeType("kfast.channel.nml"))
    pyr_cell_doc.includes.append(IncludeType("pas.channel.nml"))
    # pyr_cell_doc.includes.append(IncludeType("kslow.channel.nml"))
    # pyr_cell_doc.includes.append(IncludeType("nat.channel.nml"))
    # pyr_cell_doc.includes.append(IncludeType("nap.channel.nml"))
    # pyr_cell_doc.includes.append(IncludeType("Km.channel.nml"))

    # Define a cell
    pyr_cell = Cell(id="pyr_cell", notes="A single compartment Layer 5 Pyramidal cell")

    # Define its biophysical properties
    bio_prop = BiophysicalProperties(id="pyr_b_prop")
    #  notes="Biophysical properties for Layer 5 Pyramidal cell")

    # Membrane properties are a type of biophysical properties
    mem_prop = MembraneProperties()
    # Add membrane properties to the biophysical properties
    bio_prop.membrane_properties = mem_prop

    # Append to cell
    pyr_cell.biophysical_properties = bio_prop

    # Channel density for kfast channel
    kfast_channel_density = ChannelDensity(id="kfast_channels", cond_density="67.2 S_per_m2", erev="-80.39 mV", ion="kfast", ion_channel="kfast_channel")
    mem_prop.channel_densities.append(kfast_channel_density)

    kslow_channel_density = ChannelDensity(id="kslow_channels", cond_density="475.82 S_per_m2", erev="-80.39 mV", ion="kslow", ion_channel="kslow_channel")
    mem_prop.channel_densities.append(kslow_channel_density)

    nat_channel_density = ChannelDensity(id="nat_channels", cond_density="236.62 S_per_m2", erev="-80.39 mV", ion="nat", ion_channel="nat_channel")
    mem_prop.channel_densities.append(nat_channel_density)

    nap_channel_density = ChannelDensity(id="nap_channels", cond_density="1.44 S_per_m2", erev="-80.39 mV", ion="nap", ion_channel="nap_channel")
    mem_prop.channel_densities.append(nap_channel_density)

    km_channel_density = ChannelDensity(id="km_channels", cond_density="475.82 S_per_m2", erev="-80.39 mV", ion="km", ion_channel="km_channel")
    mem_prop.channel_densities.append(km_channel_density)

    # Other membrane properties
    mem_prop.spike_threshes.append(SpikeThresh(value="-20mV"))
    mem_prop.specific_capacitances.append(SpecificCapacitance(value="2.23 uF_per_cm2"))
    mem_prop.init_memb_potentials.append(InitMembPotential(value="-65mV"))

    intra_prop = IntracellularProperties()
    intra_prop.resistivities.append(Resistivity(value="0.1 kohm_cm"))

    # Add to biological properties
    bio_prop.intracellular_properties = intra_prop

    # Morphology
    morph = Morphology(id="pyr_cell_morph")
    #  notes="Simple morphology for the HH cell")
    seg = Segment(id="0", name="soma", notes="Soma segment")
    # We want a diameter such that area is 1000 micro meter^2
    # surface area of a sphere is 4pi r^2 = 4pi diam^2
    diam = math.sqrt(1682 / math.pi)
    proximal = distal = Point3DWithDiam(x="0", y="0", z="0", diameter=str(diam))
    seg.proximal = proximal
    seg.distal = distal
    morph.segments.append(seg)
    pyr_cell.morphology = morph

    pyr_cell_doc.cells.append(pyr_cell)
    pynml.write_neuroml2_file(nml2_doc=pyr_cell_doc, nml2_file_name=pyr_cell_fn, validate=True)
    return pyr_cell_fn


# %%
create_cell()


