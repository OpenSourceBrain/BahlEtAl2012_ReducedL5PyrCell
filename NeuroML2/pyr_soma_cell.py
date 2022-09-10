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
from neuroml import Morphology, Segment, Point3DWithDiam
from neuroml import Network, Population
from neuroml import PulseGenerator, ExplicitInput
from pyneuroml import pynml
import numpy as np
from pyneuroml.lems import LEMSSimulation

# %%
def main():
    """Main function

    Include the NeuroML model into a LEMS simulation file, run it, plot some
    data.
    """
    # Simulation bits

    sim_id = "pyr_single_comp"
    simulation = LEMSSimulation(sim_id=sim_id, duration=700, dt=0.005, simulation_seed=123)

    # Include the NeuroML model file
    simulation.include_neuroml2_file(create_network())
    # Assign target for the simulation
    simulation.assign_simulation_target("single_pyr_cell_network")

    # Recording information from the simulation
    simulation.create_output_file(id="output0", file_name=sim_id + ".dat")
    simulation.add_column_to_output_file("output0", column_id="pop0_0_v", quantity="pop0[0]/v")

    # Recording information from the simulation
    simulation.create_output_file(id="na_m", file_name=sim_id + ".na_m.dat")
    simulation.add_column_to_output_file("na_m", column_id="pop0_0_na_m", quantity="pop0[0]/pyr_b_prop/membraneProperties/nat_channels/nat/m/q")

    simulation.create_output_file(id="na_h", file_name=sim_id + ".na_h.dat")
    simulation.add_column_to_output_file("na_h", column_id="pop0_0_na_h", quantity="pop0[0]/pyr_b_prop/membraneProperties/nat_channels/nat/h/q")

    simulation.create_output_file(id="kfast_n", file_name=sim_id + ".kfast_n.dat")
    simulation.add_column_to_output_file("kfast_n", column_id="pop0_0_kfast_n", quantity="pop0[0]/pyr_b_prop/membraneProperties/kfast_channels/kfast/n/q")

    simulation.create_output_file(id="nap_m", file_name=sim_id + ".nap_m.dat")
    simulation.add_column_to_output_file("nap_m", column_id="pop0_0_nap_m", quantity="pop0[0]/pyr_b_prop/membraneProperties/nap_channels/nap/m/q")

    simulation.create_output_file(id="kslow_a", file_name=sim_id + ".kslow_a.dat")
    simulation.add_column_to_output_file("kslow_a", column_id="pop0_0_kslow_a", quantity="pop0[0]/pyr_b_prop/membraneProperties/kslow_channels/kslow/a/q")

    simulation.create_output_file(id="kslow_b", file_name=sim_id + ".kslow_b.dat")
    simulation.add_column_to_output_file("kslow_b", column_id="pop0_0_kslow_b", quantity="pop0[0]/pyr_b_prop/membraneProperties/kslow_channels/kslow/b/q")

    simulation.create_output_file(id="ikm_m", file_name=sim_id + ".ikm_m.dat")
    simulation.add_column_to_output_file("ikm_m", column_id="pop0_0_ikm_m", quantity="pop0[0]/pyr_b_prop/membraneProperties/km_channels/km/m/q")

    # Save LEMS simulation to file
    sim_file = simulation.save_to_file()

    # Run the simulation using the default jNeuroML simulator
    pynml.run_lems_with_jneuroml(sim_file, max_memory="2G", nogui=True, plot=False)
    # Plot the data
    plot_data(sim_id)

# %%
def plot_data(sim_id):
    """Plot the sim data.

    Load the data from the file and plot the graph for the membrane potential
    using the pynml generate_plot utility function.

    :sim_id: ID of simulaton

    """
    data_array = np.loadtxt(sim_id + ".dat")
    pynml.generate_plot([data_array[:, 0]], [data_array[:, 1]], "Membrane potential", show_plot_already=False, save_figure_to=sim_id + "-v.png", xaxis="time (s)", yaxis="membrane potential (V)")

    data_array_na_m = np.loadtxt(sim_id + ".na_m.dat")
    pynml.generate_plot([data_array_na_m[:, 0]], [data_array_na_m[:, 1]], "Nat m gate", show_plot_already=False, save_figure_to=sim_id + "-na_m.png", xaxis="time (s)", yaxis="q")

    data_array_na_h = np.loadtxt(sim_id + ".na_h.dat")
    pynml.generate_plot([data_array_na_h[:, 0]], [data_array_na_h[:, 1]], "Nat h gate", show_plot_already=False, save_figure_to=sim_id + "-na_h.png", xaxis="time (s)", yaxis="q")

    data_array_kfast_n = np.loadtxt(sim_id + ".kfast_n.dat")
    pynml.generate_plot([data_array_kfast_n[:, 0]], [data_array_kfast_n[:, 1]], "Kfast n gate", show_plot_already=False, save_figure_to=sim_id + "-kfast_n.png", xaxis="time (s)", yaxis="q")

    data_array_nap_m = np.loadtxt(sim_id + ".nap_m.dat")
    pynml.generate_plot([data_array_nap_m[:, 0]], [data_array_nap_m[:, 1]], "Nap m gate", show_plot_already=False, save_figure_to=sim_id + "-nap_m.png", xaxis="time (s)", yaxis="q")

    data_array_kslow_a = np.loadtxt(sim_id + ".kslow_a.dat")
    pynml.generate_plot([data_array_kslow_a[:, 0]], [data_array_kslow_a[:, 1]], "Kslow a gate", show_plot_already=False, save_figure_to=sim_id + "-kslow_a.png", xaxis="time (s)", yaxis="q")

    data_array_kslow_b = np.loadtxt(sim_id + ".kslow_b.dat")
    pynml.generate_plot([data_array_kslow_b[:, 0]], [data_array_kslow_b[:, 1]], "Kslow b gate", show_plot_already=False, save_figure_to=sim_id + "-kslow_b.png", xaxis="time (s)", yaxis="q")

    data_array_ikm_m = np.loadtxt(sim_id + ".ikm_m.dat")
    pynml.generate_plot([data_array_ikm_m[:, 0]], [data_array_ikm_m[:, 1]], "IKM m gate", show_plot_already=False, save_figure_to=sim_id + "-ikm_m.png", xaxis="time (s)", yaxis="q")
# %%
def create_cell():
    pyr_cell_doc = NeuroMLDocument(id='cell', notes="Layer 5 Pyramidal cell")
    pyr_cell_fn = "pyr_soma_cell.nml"
    # print(os.getcwd())
    pyr_cell_doc.includes.append(IncludeType("kfast.channel.nml"))
    pyr_cell_doc.includes.append(IncludeType("pas.channel.nml"))
    pyr_cell_doc.includes.append(IncludeType("kslow.channel.nml"))
    pyr_cell_doc.includes.append(IncludeType("nat.channel.nml"))
    pyr_cell_doc.includes.append(IncludeType("nap.channel.nml"))
    pyr_cell_doc.includes.append(IncludeType("IKM.channel.nml"))

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


    pas_channel_density = ChannelDensity(id="pas_channels", cond_density="0.485726 S_per_m2", erev="-80.3987 mV", ion="non_specific", ion_channel="pas")
    mem_prop.channel_densities.append(pas_channel_density)

    # Channel density for kfast channel
    kfast_channel_density = ChannelDensity(id="kfast_channels", cond_density="67.197508 S_per_m2", erev="-80 mV", ion="k", ion_channel="kfast")
    mem_prop.channel_densities.append(kfast_channel_density)

    kslow_channel_density = ChannelDensity(id="kslow_channels", cond_density="475.82 S_per_m2", erev="-80 mV", ion="k", ion_channel="kslow")
    mem_prop.channel_densities.append(kslow_channel_density)

    nat_channel_density = ChannelDensity(id="nat_channels", cond_density="236.616175 S_per_m2", erev="55 mV", ion="na", ion_channel="nat")
    mem_prop.channel_densities.append(nat_channel_density)

    nap_channel_density = ChannelDensity(id="nap_channels", cond_density="1.44 S_per_m2", erev="55 mV", ion="na", ion_channel="nap")
    mem_prop.channel_densities.append(nap_channel_density)

    km_channel_density = ChannelDensity(id="km_channels", cond_density="10.459916 S_per_m2", erev="-80 mV", ion="k", ion_channel="km")
    mem_prop.channel_densities.append(km_channel_density)

    # Other membrane properties
    mem_prop.spike_threshes.append(SpikeThresh(value="-20mV"))
    mem_prop.specific_capacitances.append(SpecificCapacitance(value="2.23041 uF_per_cm2"))
    mem_prop.init_memb_potentials.append(InitMembPotential(value="-65mV"))

    intra_prop = IntracellularProperties()
    intra_prop.resistivities.append(Resistivity(value="0.082 kohm_cm"))

    # Add to biological properties
    bio_prop.intracellular_properties = intra_prop

    # Morphology
    morph = Morphology(id="pyr_cell_morph")
    #  notes="Simple morphology for the HH cell")
    seg = Segment(id="0", name="soma", notes="Soma segment")
    # We want a diameter such that area is 1000 micro meter^2
    # surface area of a sphere is 4pi r^2 = 4pi diam^2
    # diam = math.sqrt(1682 / math.pi)
    proximal = Point3DWithDiam(x="0", y="0", z="0", diameter=str(23.1453))
    distal = Point3DWithDiam(x="0", y="23.1453", z="0", diameter=str(23.1453))
    seg.proximal = proximal
    seg.distal = distal
    morph.segments.append(seg)
    pyr_cell.morphology = morph

    pyr_cell_doc.cells.append(pyr_cell)
    pynml.write_neuroml2_file(nml2_doc=pyr_cell_doc, nml2_file_name=pyr_cell_fn, validate=True)
    return pyr_cell_fn

create_cell()

# %%
def create_network():
    """Create the network

    :returns: name of network nml file
    """
    net_doc = NeuroMLDocument(id="network",
                              notes="Pyramidal cell network")
    net_doc_fn = "pyr_soma.net.nml"
    net_doc.includes.append(IncludeType(href=create_cell()))
    # Create a population: convenient to create many cells of the same type
    pop = Population(id="pop0", notes="A population for pyramidal cell", component="pyr_cell", size=1)
    # Input
    pulsegen = PulseGenerator(id="pg", notes="Simple pulse generator", delay="100ms", duration="500ms", amplitude="0.4nA")

    exp_input = ExplicitInput(target="pop0[0]", input="pg")

    net = Network(id="single_pyr_cell_network",
                  type="networkWithTemperature",
                  temperature = "37 degC",
                  note="A network with a single population")
    net_doc.pulse_generators.append(pulsegen)
    net.explicit_inputs.append(exp_input)
    net.populations.append(pop)
    net_doc.networks.append(net)

    pynml.write_neuroml2_file(nml2_doc=net_doc, nml2_file_name=net_doc_fn, validate=True)
    return net_doc_fn

# %%
if __name__ == "__main__":
    main()
