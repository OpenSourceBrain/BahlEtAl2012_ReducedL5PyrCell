import math
from neuroml import NeuroMLDocument
from neuroml import Cell
from neuroml import BiophysicalProperties
from neuroml import MembraneProperties
from neuroml import IncludeType, Include, Property
from neuroml import ChannelDensity, ChannelDensityNonUniform, ChannelDensityNernst, ChannelDensityGHK2, ChannelDensityVShift
from neuroml import SpikeThresh
from neuroml import SpecificCapacitance
from neuroml import InitMembPotential
from neuroml import IntracellularProperties, Species
from neuroml import Resistivity
from neuroml import Morphology, Segment, Point3DWithDiam, SegmentGroup
from neuroml import Network, Population, InhomogeneousParameter, ProximalDetails
from neuroml import PulseGenerator, ExplicitInput, Input, InputList
from neuroml import InhomogeneousParameter, InhomogeneousValue, VariableParameter
from pyneuroml import pynml
import numpy as np
from pyneuroml.lems import LEMSSimulation
from CellBuilder import (create_cell, add_segment, add_channel_density, set_init_memb_potential, set_resistivity, set_specific_capacitance, get_seg_group_by_id)
import typing
import xml.etree.ElementTree as ET

def plot_data(sim_id, start, end, title):
    """Plot the sim data.

    Load the data from the file and plot the graph for the membrane potential
    using the pynml generate_plot utility function.

    :sim_id: ID of simulaton

    """
    #  Generate plot, for single compartmental cell model
    data_array = np.loadtxt(sim_id + ".dat")

    #  For multi compartmental cell model:
    pynml.generate_plot([data_array[start:end, 0], data_array[start:end, 0], data_array[start:end, 0]],
                         [data_array[start:end, 1], data_array[start:end, 2], data_array[start:end, 3]], title, ["Soma", "Apical", "Tuft"], show_plot_already=False,
                          xaxis="time (s)", yaxis="membrane potential (V)", title_above_plot=True)

class BahlPyramidal():
    """Full Hodgkin-Huxley Model implemented in Python"""

    """ __init__ uses optional arguments """
    """ when no argument is passed default values are used """

    def __init__(self, e_pas, Rm_axosomatic, axosomatic_list_cm, spinefactor, soma_gbar_nat, soma_gbar_kfast,
                soma_gbar_kslow, soma_gbar_nap, soma_gbar_km, basal_gbar_ih, tuft_gbar_ih, tuft_gbar_nat,
                decay_kfast, decay_kslow, hillock_gbar_nat, iseg_gbar_nat, iseg_vshift2_nat, Ra_apical,
                tuft_gbar_sca, tuft_vshift_sca, tuft_gbar_kca,
                amplitude_soma_pulse, duration_soma_pulse, amplitude_dendritic_pulse, modelname):
        
        self.e_pas = str(e_pas)+" mV"                               
        """ membrane capacitance, in uF/cm^2 """
        
        self.soma_gbar_nat = str(soma_gbar_nat)+" S_per_m2"                             
        """ Sodium (Na) maximum conductances, in S/m^2 """
        
        self.soma_gbar_kfast = str(soma_gbar_kfast)+" S_per_m2"
        self.soma_gbar_kslow = str(soma_gbar_kslow)+" S_per_m2"
        self.soma_gbar_nap = str(soma_gbar_nap)+" S_per_m2"
        self.soma_gbar_km = str(soma_gbar_km)+" S_per_m2"
        self.basal_gbar_ih = str(basal_gbar_ih)+" S_per_m2"
        self.tuft_gbar_ih = str(tuft_gbar_ih)+" S_per_m2"
        self.tuft_gbar_nat = str(tuft_gbar_nat)+" S_per_m2"
        self.hillock_gbar_nat = str(hillock_gbar_nat)+" S_per_m2"
        self.iseg_gbar_nat = str(iseg_gbar_nat)+" S_per_m2"

        self.iseg_vshift2_nat = str(10+iseg_vshift2_nat)+" mV"
        """ The original hoc files in ../NEURON/init_models_with_ca/ has vShift2 mentioned for the section iseg. Seeing the mod file for sca channel in
            ../NEURON/channels/sca.mod the v_shift used below is the equal to vShift + vShift2 and calculated as v_shift = 10 mV + (-10.612583 mV)
        """
        self.axosomatic_gbar_pas = str((1/Rm_axosomatic)*1e4)+" S_per_m2"
        self.apicaltree_gbar_pas = str(((1/Rm_axosomatic)*1e4)*spinefactor)+" S_per_m2"

        self.axosomatic_list_cm = str(axosomatic_list_cm)+" uF_per_cm2"
        self.apicaltree_list_cm = str(axosomatic_list_cm*spinefactor)+" uF_per_cm2"

        # Defining variable parameter value for the respective channels
        self.apicaltree_gbar_kfast_val = str(soma_gbar_kfast)+"*exp(-p/"+str(decay_kfast)+")"
        self.apicaltree_gbar_kslow_val = str(soma_gbar_kslow)+"*exp(-p/"+str(decay_kslow)+")"

        self.tuft_mih = tuft_gbar_ih/500
        self.tuft_mnat = (tuft_gbar_nat - soma_gbar_nat)/500
        self.apical_gbar_ih_val = str(self.tuft_mih)+"*p"
        self.apical_gbar_nat_val = str(self.tuft_mnat)+"*p + "+str(soma_gbar_nat)

        # Incorporating calcium dependent mechanisms to the respective segments
        self.Ra_apical = str(Ra_apical/1000)+" kohm_cm"
        self.tuft_gbar_sca = str(tuft_gbar_sca)+" S_per_m2"
        self.tuft_vshift_sca = str(tuft_vshift_sca)+" mV"
        self.tuft_gbar_kca = str(tuft_gbar_kca)+" S_per_m2"

        # Input to cell ( somatic pulse and dendritic EPSP)
        self.amplitude_soma_pulse = amplitude_soma_pulse
        self.duration_soma_pulse = duration_soma_pulse
        self.amplitude_dendritic_pulse = str(amplitude_dendritic_pulse)
        self.modelname = str(modelname)



    def create_pyr_cell(self):
        pyr_cell_doc = NeuroMLDocument(id='cell', notes="Layer 5 Pyramidal cell")
        cell = create_cell("pyr"+"_"+self.modelname)
        nml_cell_file = cell.id + ".cell.nml"

        pyr_cell_doc.includes.append(IncludeType("kca.channel.nml"))
        pyr_cell_doc.includes.append(IncludeType("sca.channel.nml"))
        pyr_cell_doc.includes.append(IncludeType("cad.nml"))
        pyr_cell_doc.includes.append(IncludeType("nat.channel.nml"))

        """ Adding the morphological detailed segments in the cell """
        #   Add soma segments
        diam = 23.1453
        # soma_0 = add_segment(cell,
        #                     prox=[0.0, 0.0, 0.0, diam],
        #                     dist=[diam, 0.0, 0.0, diam],
        #                     name="Seg0_soma",
        #                     group="soma")
        soma_0 = add_segment(cell,
                            prox=[0.0, 0.0, 0.0, diam],
                            dist=[11.5726, 0.0, 0.0, diam],
                            name="Seg0_soma",
                            group="soma_0")

        soma_1 = add_segment(cell,
                            prox=None,
                            dist=[diam, 0.0, 0.0, diam],
                            name="Seg1_soma",
                            parent=soma_0,
                            group="soma_0")

        # Add hillock segments
        hillock_0 = add_segment(cell,
                                parent=soma_0,
                                prox=[0, 0, 0, 3.35],
                                dist=[-2, 1.74846e-07, 0, 3.35],
                                name="Seg0_hillock",
                                group="hillock_0")

        hillock_1 = add_segment(cell,
                                parent=hillock_0,
                                prox=None,
                                dist=[-6, 5.24537e-07, 0, 3.05],
                                name="Seg1_hillock",
                                group="hillock_0")

        hillock_2 = add_segment(cell,
                                parent=hillock_1,
                                prox=None,
                                dist=[-10, 8.74228e-07, 0, 2.75],
                                name="Seg2_hillock",
                                group="hillock_0")

        hillock_3 = add_segment(cell,
                                parent=hillock_2,
                                prox=None,
                                dist=[-14, 1.22392e-06, 0, 2.45],
                                name="Seg3_hillock",
                                group="hillock_0")

        hillock_4 = add_segment(cell,
                                parent=hillock_3,
                                prox=None,
                                dist=[-18, 1.57361e-06, 0, 2.15],
                                name="Seg4_hillock",
                                group="hillock_0"
                                )

        hillock_5 = add_segment(cell,
                                parent=hillock_4,
                                prox=None,
                                dist=[-20, 1.7486e-06, 0, 2.15],
                                name="Seg5_hillock",
                                group="hillock_0"
                                )

        # Add basal segments
        basal_0 = add_segment(cell,
                            parent=soma_0,
                            prox=[11.5726, 0, 0, 8.74536],
                            dist=[11.5726, 128.5, 0, 8.74536],
                            name="Seg0_basal",
                            group="basal_0")

        basal_1 = add_segment(cell,
                            parent=basal_0,
                            prox=None,
                            dist=[11.5726, 257, 0, 8.74536],
                            name="Seg1_basal",
                            group="basal_0") 

        # Add apical segments
        apical_0 = add_segment(cell,
                            parent=soma_1,
                            prox=[23.1453, 0, 0, 5.92845],
                            dist=[73.1453, 0, 0, 5.92845],
                            name="Seg0_apical",
                            group="apical_0")

        apical_1 = add_segment(cell,
                            parent=apical_0,
                            prox=None,
                            dist=[173.145, 0, 0, 5.92845],
                            name="Seg1_apical",
                            group="apical_0")

        apical_2 = add_segment(cell,
                            parent=apical_1,
                            prox=None,
                            dist=[273.145, 0, 0, 5.92845],
                            name="Seg2_apical",
                            group="apical_0")

        apical_3 = add_segment(cell,
                            parent=apical_2,
                            prox=None,
                            dist=[373.145, 0, 0, 5.92845],
                            name="Seg3_apical",
                            group="apical_0")

        apical_4 = add_segment(cell,
                            parent=apical_3,
                            prox=None,
                            dist=[473.145, 0, 0, 5.92845],
                            name="Seg4_apical",
                            group="apical_0")

        apical_5 = add_segment(cell,
                            parent=apical_4,
                            prox=None,
                            dist=[523.145, 0, 0, 5.92845],
                            name="Seg5_apical",
                            group="apical_0")

        # Add iseg segments
        iseg_0 = add_segment(cell,
                            parent=hillock_5,
                            prox=[-20, 1.74846e-06, 0, 1.95],
                            dist=[-22.5, 2.12595e-06, 0, 1.95],
                            name="Seg0_iseg",
                            group="iseg_0")

        iseg_1 = add_segment(cell,
                            parent=iseg_0,
                            prox=None,
                            dist=[-27.5, 2.88092e-06, 0, 1.85],
                            name="Seg1_iseg",
                            group="iseg_0")

        iseg_2 = add_segment(cell,
                            parent=iseg_1,
                            prox=None,
                            dist=[-32.5, 3.6359e-06, 0, 1.75],
                            name="Seg2_iseg",
                            group="iseg_0")

        iseg_3 = add_segment(cell,
                            parent=iseg_2,
                            prox=None,
                            dist=[-37.5, 4.39088e-06, 0, 1.65],
                            name="Seg3_iseg",
                            group="iseg_0")

        iseg_4 = add_segment(cell,
                            parent=iseg_3,
                            prox=None,
                            dist=[-42.5, 5.14586e-06, 0, 1.55],
                            name="Seg4_iseg",
                            group="iseg_0")

        iseg_5 = add_segment(cell,
                            parent=iseg_4,
                            prox=None,
                            dist=[-45, 5.52335e-06, 0, 1.55],
                            name="Seg5_iseg",
                            group="iseg_0")

        # Add tuft segments
        tuft_0 = add_segment(cell,
                            parent=apical_5,
                            prox=[523.145, 0, 0, 6.01807],
                            dist=[647.895, 0, 0, 6.01807],
                            name="Seg0_tuft",
                            group="tuft_0"
                            )

        tuft_1 = add_segment(cell,
                            parent=tuft_0,
                            prox=None,
                            dist=[897.395, 0, 0, 6.01807],
                            name="Seg1_tuft",
                            group="tuft_0"
                            )

        tuft_2 = add_segment(cell,
                            parent=tuft_1,
                            prox=None,
                            dist=[1022.15, 0, 0, 6.01807],
                            name="Seg2_tuft",
                            group="tuft_0"
                            )

        # Add axon segments
        axon_0 = add_segment(cell,
                            parent=iseg_5,
                            prox=[-45, 5.52335e-06, 0, 1.5],
                            dist=[-295, 4.32723e-05, 0, 1.5],
                            name="Seg0_axon",
                            group="axon_0"
                            )

        axon_1 = add_segment(cell,
                            parent=axon_0,
                            prox=None,
                            dist=[-545, 8.10213e-05, 0, 1.5],
                            name="Seg1_axon",
                            group="axon_0")

        # Define the nseg for each of the segments in the cell
        for section_name in ["soma_0", "hillock_0", "basal_0", "apical_0", "iseg_0", "tuft_0", "axon_0"]:
            section_group = get_seg_group_by_id(section_name, cell)
            if section_group is None:
                continue
            else:
                section_group.neuro_lex_id = 'sao864921383'
                if section_name in ["apical_0", "hillock_0", "iseg_0"]:
                    section_group.properties.append(Property(tag="numberInternalDivisions", value="5"))
                elif section_name in ["tuft_0"]:
                    section_group.properties.append(Property(tag="numberInternalDivisions", value="2"))
                else:
                    continue

        # Creating additional segment groups which are necessary to add the density mechanisms
        basal_seg_group = SegmentGroup(neuro_lex_id=None, id="basal_group")
        basal_seg_group.includes.append(Include(segment_groups="basal_0"))

        apical_seg_group = SegmentGroup(neuro_lex_id=None, id="apical_group")
        apical_seg_group.includes.append(Include(segment_groups="apical_0"))    

        tuft_seg_group = SegmentGroup(neuro_lex_id=None, id="tuft_group")
        tuft_seg_group.includes.append(Include(segment_groups="tuft_0"))

        hillock_seg_group = SegmentGroup(neuro_lex_id=None, id="hillock_group")
        hillock_seg_group.includes.append(Include(segment_groups="hillock_0"))

        iseg_seg_group = SegmentGroup(neuro_lex_id=None, id="iseg_group")
        iseg_seg_group.includes.append(Include(segment_groups="iseg_0"))

        cell.morphology.segment_groups.append(basal_seg_group)
        cell.morphology.segment_groups.append(apical_seg_group)
        cell.morphology.segment_groups.append(tuft_seg_group)
        cell.morphology.segment_groups.append(hillock_seg_group)
        cell.morphology.segment_groups.append(iseg_seg_group)

        # Adding the segments to axon_group, dendrite_group, soma_group to help in visualization
        soma_seg_group = get_seg_group_by_id("soma_group", cell)
        soma_seg_group.includes.append(Include(segment_groups="soma_0"))
        soma_seg_group.properties.append(Property(tag="color", value="0 0 0.8"))

        ax_seg_group = get_seg_group_by_id("axon_group", cell)
        ax_seg_group.includes.append(Include(segment_groups="axon_0"))
        ax_seg_group.includes.append(Include(segment_groups="hillock_0"))
        ax_seg_group.includes.append(Include(segment_groups="iseg_0"))
        ax_seg_group.properties.append(Property(tag="color", value="0 0.8 0"))

        den_seg_group = get_seg_group_by_id("dendrite_group", cell)
        den_seg_group.includes.append(Include(segment_groups="basal_0"))
        den_seg_group.includes.append(Include(segment_groups="apical_0"))
        den_seg_group.includes.append(Include(segment_groups="tuft_0"))
        den_seg_group.properties.append(Property(tag="color", value="0.8 0 0"))

        # Adding two additional segments namely axosomatic and apicaltree 
        axosomatic = SegmentGroup(neuro_lex_id=None, id="axosomatic_list")
        apicaltree = SegmentGroup(neuro_lex_id=None, id="apicaltree_list")

        cell.morphology.segment_groups.append(axosomatic)
        cell.morphology.segment_groups.append(apicaltree)

        axosomatic_group = get_seg_group_by_id("axosomatic_list", cell)
        axosomatic_group.includes.append(Include(segment_groups="soma_0"))
        axosomatic_group.includes.append(Include(segment_groups="hillock_0"))
        axosomatic_group.includes.append(Include(segment_groups="basal_0"))
        axosomatic_group.includes.append(Include(segment_groups="iseg_0"))
        axosomatic_group.includes.append(Include(segment_groups="axon_0"))
        # axosomatic_group.properties.append(Property(tag="color", value="0.8 0 0"))

        apicaltree_group = get_seg_group_by_id("apicaltree_list", cell)
        apicaltree_group.includes.append(Include(segment_groups="apical_0"))
        apicaltree_group.includes.append(Include(segment_groups="tuft_0"))

        # Defining the variable parameters for the segment groups apicaltree_list and apical_group
        for g in ['apicaltree_list', 'apical_group']:
            seg_group = get_seg_group_by_id(g, cell)
            seg_group.inhomogeneous_parameters.append(
                InhomogeneousParameter(
                    id="PathLengthOver_" + g,
                    variable="p",
                    metric="Path Length from root",
                    proximal=ProximalDetails(
                        translation_start="0")))

        # Adding biophyshical properties of the cell 
        # Adding density mechanisms to each of the respective segments present in the cell
        # leak_axosomatic_list
        add_channel_density(cell, pyr_cell_doc,
                            cd_id="axosomatic_gpas",
                            cond_density=self.axosomatic_gbar_pas,
                            ion_channel="pas",
                            ion_chan_def_file="pas.channel.nml",
                            erev=self.e_pas,
                            ion="non_specific",
                            group="axosomatic_list")

        # leak_apicaltree_list
        add_channel_density(cell, pyr_cell_doc,
                        cd_id="apicaltree_gpas",
                        cond_density=self.apicaltree_gbar_pas,
                        ion_channel="pas",
                        ion_chan_def_file="pas.channel.nml",
                        erev=self.e_pas,
                        ion="non_specific",
                        group="apicaltree_list")                     

        # add_channel_density(cell, pyr_cell_doc,
        #                     cd_id="soma_gpas",
        #                     cond_density="0.485726 S_per_m2",
        #                     ion_channel="pas",
        #                     ion_chan_def_file="pas.channel.nml",
        #                     erev="-80.3987 mV",
        #                     ion="non_specific",
        #                     group="soma_group")
        
        # nat_soma    
        nat_soma = ChannelDensityVShift(id="nat_soma", cond_density=self.soma_gbar_nat, erev="55 mV", v_shift="10mV", ion="na", ion_channel="nat",
                                            segment_groups="soma_group")
        cell.biophysical_properties.membrane_properties.channel_density_v_shifts.append(nat_soma)


        # nat_hillock
        nat_hillock = ChannelDensityVShift(id="nat_hillock", cond_density=self.hillock_gbar_nat, erev="55 mV", v_shift="10mV", ion="na", ion_channel="nat",
                                            segment_groups="hillock_group")
        cell.biophysical_properties.membrane_properties.channel_density_v_shifts.append(nat_hillock)
        
        # nat_iseg 
        """ The original hoc files in ../NEURON/init_models_with_ca/ has vShift2 mentioned for the section iseg. Seeing the mod file for sca channel in
            ../NEURON/channels/sca.mod the v_shift used below is the equal to vShift + vShift2 and calculated as v_shift = 10 mV + (-10.612583 mV)
        """
        nat_iseg = ChannelDensityVShift(id="nat_iseg", cond_density=self.iseg_gbar_nat, erev="55 mV", v_shift=self.iseg_vshift2_nat, ion="na", ion_channel="nat",
                                            segment_groups="iseg_group")
        cell.biophysical_properties.membrane_properties.channel_density_v_shifts.append(nat_iseg)

        # nat_tuft
        nat_tuft = ChannelDensityVShift(id="nat_tuft", cond_density=self.tuft_gbar_nat, erev="55 mV", v_shift="10 mV", ion="na", ion_channel="nat",
                                            segment_groups="tuft_group")
        cell.biophysical_properties.membrane_properties.channel_density_v_shifts.append(nat_tuft)

        # kfast_soma
        add_channel_density(cell, pyr_cell_doc,
                            cd_id="kfast_soma",
                            cond_density=self.soma_gbar_kfast,
                            ion_channel="kfast",
                            ion_chan_def_file="kfast.channel.nml",
                            erev="-80mV",
                            ion="k",
                            group="soma_group")

        # kslow_soma
        add_channel_density(cell, pyr_cell_doc,
                            cd_id="kslow_soma",
                            cond_density=self.soma_gbar_kslow,
                            ion_channel="kslow",
                            ion_chan_def_file="kslow.channel.nml",
                            erev="-80mV",
                            ion="k",
                            group="soma_group")   

        # nap_soma
        add_channel_density(cell, pyr_cell_doc,
                            cd_id="nap_soma",
                            cond_density=self.soma_gbar_nap,
                            ion_channel="nap",
                            ion_chan_def_file="nap.channel.nml",
                            erev="55mV",
                            ion="na",
                            group="soma_group")  

        # km_soma
        add_channel_density(cell, pyr_cell_doc,
                            cd_id="km_soma",
                            cond_density=self.soma_gbar_km,
                            ion_channel="km",
                            ion_chan_def_file="IKM.channel.nml",
                            erev="-80mV",
                            ion="k",
                            group="soma_group")

        # ih_basal
        add_channel_density(cell, pyr_cell_doc,
                            cd_id="ih_basal",
                            cond_density=self.basal_gbar_ih,
                            ion_channel="ih",
                            ion_chan_def_file="ih.channel.nml",
                            erev="-47mV",
                            ion="hcn",
                            group="basal_group")

        # sca_tuft
        sca_tuft = ChannelDensityVShift(id="tuft_sca", cond_density=self.tuft_gbar_sca, erev="140 mV", v_shift=self.tuft_vshift_sca, ion="ca", ion_channel="sca",
                                        segment_groups="tuft_group")
        cell.biophysical_properties.membrane_properties.channel_density_v_shifts.append(sca_tuft)

        # kca_tuft
        kca_tuft = ChannelDensity(id="tuft_kca", ion_channel="kca", cond_density=self.tuft_gbar_kca, segment_groups="tuft_group", ion="k", erev="-80mV")
        cell.biophysical_properties.membrane_properties.channel_densities.append(kca_tuft)

        # Calculating the kfast conduction density using variable parameter for segment group apicaltree                           
        gbar_kfast_apicaltree = VariableParameter(parameter="condDensity",
                                                segment_groups="apicaltree_list",
                                                inhomogeneous_value=InhomogeneousValue(inhomogeneous_parameters="PathLengthOver_apicaltree_list",
                                                value=self.apicaltree_gbar_kfast_val))
        kfast_apicaltree_list = ChannelDensityNonUniform(id="apicaltree_g_kfast", ion_channel="kfast", erev="-80 mV", ion="k")
        kfast_apicaltree_list.variable_parameters.append(gbar_kfast_apicaltree)

        # Calculating the kfast conduction density using variable parameter for segment group apicaltree
        gbar_kslow_apicaltree = VariableParameter(parameter="condDensity",
                                                segment_groups="apicaltree_list",
                                                inhomogeneous_value=InhomogeneousValue(inhomogeneous_parameters="PathLengthOver_apicaltree_list",
                                                value=self.apicaltree_gbar_kslow_val))
        kslow_apicaltree_list = ChannelDensityNonUniform(id="apicaltree_g_kslow", ion_channel="kslow", erev="-80mV", ion="k")
        kslow_apicaltree_list.variable_parameters.append(gbar_kslow_apicaltree)

        # Calculating the nat conduction density using variable parameter for segment group apical [47.34461*p+236.616175]
        gbar_nat_apical = VariableParameter(parameter="condDensity",
                                            segment_groups="apical_group",
                                            inhomogeneous_value=InhomogeneousValue(inhomogeneous_parameters="PathLengthOver_apical_group",
                                            value=self.apical_gbar_nat_val))
        nat_apical = ChannelDensityNonUniform(id="apical_g_nat", ion_channel="nat", erev="55 mV", ion="na")
        nat_apical.variable_parameters.append(gbar_nat_apical)

        # Calculating the nat conduction density using variable parameter for segment group apical
        gbar_ih_apical = VariableParameter(parameter="condDensity",
                                            segment_groups="apical_group",
                                            inhomogeneous_value=InhomogeneousValue(inhomogeneous_parameters="PathLengthOver_apical_group",
                                            value=self.apical_gbar_ih_val))
        ih_apical = ChannelDensityNonUniform(id="apical_g_ih", ion_channel="ih", erev="-47 mV", ion="hcn")
        ih_apical.variable_parameters.append(gbar_ih_apical)

        cell.biophysical_properties.membrane_properties.channel_density_non_uniforms.append(kfast_apicaltree_list)
        cell.biophysical_properties.membrane_properties.channel_density_non_uniforms.append(kslow_apicaltree_list)
        cell.biophysical_properties.membrane_properties.channel_density_non_uniforms.append(nat_apical)
        cell.biophysical_properties.membrane_properties.channel_density_non_uniforms.append(ih_apical)

        # Other cell properties
        set_specific_capacitance(cell, self.axosomatic_list_cm, group="axosomatic_list")
        set_specific_capacitance(cell, self.apicaltree_list_cm, group="apicaltree_list")
        cell.biophysical_properties.membrane_properties.spike_threshes.append(SpikeThresh(value="-20mV"))
        # set_specific_capacitance(cell, "2.23041 uF_per_cm2", group="soma_group")
        set_init_memb_potential(cell, "-67mV")
        # set_resistivity(cell, "0.082 kohm_cm")
        set_resistivity(cell, "0.082 kohm_cm", "soma_group")
        set_resistivity(cell, "0.082 kohm_cm", "axon_group")
        set_resistivity(cell, "0.734 kohm_cm", "basal_group")
        set_resistivity(cell, "0.527 kohm_cm", "tuft_group")
        set_resistivity(cell, self.Ra_apical, "apical_group")

        cell.biophysical_properties.intracellular_properties.species.append(Species(id="ca", concentration_model="cad", ion="ca", initial_concentration="100e-6 mM",
                                initial_ext_concentration="2 mM", segment_groups="tuft_group"))

        pyr_cell_doc.cells.append(cell)
        pynml.write_neuroml2_file(nml2_doc=pyr_cell_doc, nml2_file_name=nml_cell_file, validate=True)
        return nml_cell_file 

    def set_dendritic_ampltide(self):
        # parsing directly.
        tree = ET.parse('epsp_tuft.xml')
        root = tree.getroot()
        for epsp in root.iter('epsp_input'):
            epsp.set('startAmplitude', self.amplitude_dendritic_pulse)
        tree.write('epsp_tuft.xml')

    def create_pyr_network(self):
        """Create the network

        :returns: name of network nml file
        """
        net_doc = NeuroMLDocument(id="network",
                                notes="Pyramidal cell network")
        net_doc_fn = "pyr_multi_comp.net.nml"
        net_doc.includes.append(IncludeType(href=self.create_pyr_cell()))

        # Create a population: convenient to create many cells of the same type
        pop = Population(id="pop0", notes="A population for pyramidal cell",
                         component="pyr"+"_"+self.modelname, size=1)
        # Input
        pulsegen = PulseGenerator(id="pg", notes="Simple pulse generator",
                                  delay="100ms",
                                  duration=self.duration_soma_pulse,
                                  amplitude=self.amplitude_soma_pulse)
        exp_input = ExplicitInput(target="pop0[0]", input="pg")

        # EPSP shaped current injected to the dendritic tuft
        epsp_current = Input(id="0", target="pop0/0/pyr"+"_"+self.modelname, segment_id="23", destination="synapses", fraction_along=0.5)
        dend_input = InputList(id="i1", component="epsp_tuft", populations="pop0")
        dend_input.input.append(epsp_current)

        net = Network(id="single_pyr_cell_network",
                    type="networkWithTemperature",
                    temperature = "37 degC",
                    note="A network with a single population")
        net_doc.pulse_generators.append(pulsegen)
        net.explicit_inputs.append(exp_input)
        net.input_lists.append(dend_input)
        net.populations.append(pop)
        net_doc.networks.append(net)

        pynml.write_neuroml2_file(nml2_doc=net_doc, nml2_file_name=net_doc_fn, validate=True)
        return net_doc_fn

    def run_simulation(self):
        """Run the simulation using the neuroml file generated for the cell

        Include the NeuroML model into a LEMS simulation file, run it, plot some
        data.
        """
        # Simulation bits

        sim_id = "pyr_multi_comp"
        simulation = LEMSSimulation(sim_id=sim_id, duration=700, dt=0.005, simulation_seed=123)

        self.set_dendritic_ampltide()
        simulation.include_lems_file("epsp_tuft.xml")
        # Include the NeuroML model file
        simulation.include_neuroml2_file(self.create_pyr_network())

        # Assign target for the simulation
        simulation.assign_simulation_target("single_pyr_cell_network")

        # Recording information from the simulation
        simulation.create_output_file(id="output0", file_name=sim_id + ".dat")
        simulation.add_column_to_output_file("output0", column_id="pop0_0_soma_v", quantity="pop0/0/pyr"+"_"+self.modelname+"/0/v")
        # Add other segments to the output file of membrane potential i.e. apical and tuft
        simulation.add_column_to_output_file("output0", column_id="pop0_0_apical_v", quantity="pop0/0/pyr"+"_"+self.modelname+"/13/v")
        simulation.add_column_to_output_file("output0", column_id="pop0_0_tuft_v", quantity="pop0/0/pyr"+"_"+self.modelname+"/23/v")

        # Save LEMS simulation to file
        sim_file = simulation.save_to_file()

        # Run the simulation using the default jNeuroML simulator
        # pynml.run_lems_with_jneuroml(sim_file, max_memory="2G", nogui=True, plot=False)

        # For multicompartmental cell model run the lems using JNML NEURON
        pynml.run_lems_with_jneuroml_neuron(sim_file, max_memory="2G", nogui=True, plot=False)

# def regenerate_and_run_model():
#     sim_id = "pyr_multi_comp"
#     pyr = BahlPyramidal(e_pas, soma_gbar_nat, soma_gbar_kfast, soma_gbar_kslow, soma_gbar_nap, soma_gbar_km,
#                     basal_gbar_ih, tuft_gbar_ih, tuft_gbar_nat, hillock_gbar_nat, iseg_gbar_nat, iseg_vshift2_nat,
#                     Rm_axosomatic, axosomatic_list_cm, spinefactor, decay_kfast, decay_kslow, Ra_apical,
#                     tuft_gbar_sca, tuft_vshift_sca, tuft_gbar_kca)
#     pyr.run_simulation()  