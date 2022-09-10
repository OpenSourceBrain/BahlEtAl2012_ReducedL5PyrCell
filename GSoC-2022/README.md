# Google Summer of Code 2022
## General Information:
- Mentor information:
    - Padraig Gleeson (p.gleeson@ucl.ac.uk) (he/him/his)
    - Ankur Sinha (ankur.sinha@ucl.ac.uk) (he/him/his)
- Public chat channels (use either Gitter or Matrix—they’re bridged to each other):
    - OSB: https://docs.opensourcebrain.org/General/Contacts.html#chat  
    - NeuroML: https://docs.neuroml.org/NeuroMLOrg/CommunicationChannels.html#chat-channels 
- GSoC timeline: https://developers.google.com/open-source/gsoc/timeline
- General links:
    - NeuroML documentation: https://docs.neuroml.org
    - Open Source Brain documentation: https://docs.opensourcebrain.org
    - OSBv1: https://opensourcebrain.org
    - OSBv2: https://v2.opensourcebrain.org

## Project Information:
- [Project Proposal](https://docs.google.com/document/d/1GBoi9apEY3H_MndKfPCxUw29VjSLbJN6fgwAEDZXoGw/edit)
- [Project Description](https://summerofcode.withgoogle.com/programs/2022/projects/gXt6Wgk5)

## Community bonding period
The community bonding period was mainly for getting to know more about the other cortical pyramidal cell models on OSB which have been converted to NeuroML. They had same or similar mod files which eased the conversion of those used in this model. Moving forward I started with writing a python script for the single compartmental cell i.e. soma with all the density mechanisms and was able to successfully run a simulation on it. Other than that, in this period I was involved with running simulations on NEURON. Since I was not much accustomed to the NEURON GUI tools I went through some of the NEURON tutorial videos and also got myself added to their discussion group.

## Week 1 - 4
- Created the [Test_soma.hoc](https://github.com/OpenSourceBrain/BahlEtAl2012_ReducedL5PyrCell/blob/master/NEURON/channels/Test_soma.hoc) file to test the neuroml single compartmental (soma) cell 
    - Added [plots](https://github.com/OpenSourceBrain/BahlEtAl2012_ReducedL5PyrCell/blob/70ab1e87dda5fd983c6c47a2af87027f647952b4/NEURON/channels/Test_soma.hoc#L101) of the activation / inactivation variables for all the channels 
- Added the summary plots of the channels converted to neuroml to a directory
    - Density mechanisms in neuroml are first validated using ```pyneuroml -validate```
    - Summary plots include time course and steady state of the different gates. Link to the [directory](https://github.com/OpenSourceBrain/BahlEtAl2012_ReducedL5PyrCell/tree/nrn_tests/NeuroML2/channel_summary)
    - Faced issue to plot for kslow channel (fractional gate) using pynml-channelanalysis. Hence, created a [LEMS file for kslow channel](https://github.com/OpenSourceBrain/BahlEtAl2012_ReducedL5PyrCell/blob/nrn_tests/NeuroML2/LEMS_Test_kslow.xml) to get the simulation saved in dat files
    - Upgraded the [channel info template](https://github.com/NeuroML/pyNeuroML/blob/development/pyneuroml/analysis/ChannelInfo_TEMPLATE.md) to a different style with no text flowing inside. Link to the [merged PR](https://github.com/NeuroML/pyNeuroML/pull/174) 
- Comparison of LEMS and mod files for all the channels
    - [compare_nml2_mods.py](compare_nml2_mods.py) - Updates the readme, comparing steady state and time course plots of each channel gates for LEMS and mod files inside the [directory](https://github.com/OpenSourceBrain/BahlEtAl2012_ReducedL5PyrCell/tree/nrn_tests/NeuroML2/compare_nml2_mods) 
- NeuroML implementation of the single compartmental cell (soma) adding each channel one by one
    - Understand the change on activation / inactivation variables (gates) with variable pulse inputs
    - Inferential study of the characteristics of the channels involved 
    - Created [mep file](https://github.com/OpenSourceBrain/BahlEtAl2012_ReducedL5PyrCell/blob/master/NEURON/test/.test.mep) and added OMV tests for the LEMS and NEURON files in their respective directories.

## Week 5 - 8
- Converted the ca dependent mechanisms namely (cad, sca, kca) to NeuroML
    - Understood the dynamics from their mod files and referenced some of the previous works that involved conversion of such mechanisms
    - Compared the LEMS and mod file for sca channel and added the plots to the compare_nml2_mods directory
- Validated the ca dependent channels on single compartmental cell
    - Created a NEURON hoc file including the three mechanisms and a leak channel. Recorded the cai,(internal ca conc.), cao (outer ca conc.) and ica (ca current)
    - Similarly, created a neuroml cell with soma including leak, sca and kca as channel densities and adding the cad as intracellular properties. The notebook included plots as above.
    - To debug the discrepancies in the plots, set the conductance for sca, kca to 0 then increased conductance of the mechanisms involved one by one and saw how eca and ica changed for both NEURON as well as NeuroML code.
    - ECA (ca reversal potential) used was not being calculated using the nernst / ghk equation instead was fixed at 140.
    - OMV tests were added for LEMS and hoc files which ran on three simulation engines : jNeuroML, jNeuroML_NEURON, jNeuroML_NetPyNE
- Created a test file for example 1 which was able to record from 3 different locations of the cell namely Soma, Apical, Tuft. 
- Morphology of the multi compartmental cell 
    - Exported from the test file created above to NeuroML using export_nml2.py
    - Used cellBuilder.py to add the different components to the neuroml cell effeciently
    
- parse_mod_file.py : 
    - Added the necessary information (parameters and procedures) as comments to the converted neuroml file which can be deleted afterwards.
    - Improved and moved the script along with the mod files to test to the repository NEURONShowcase 
    - Added the tutorial notebook showing how to use the utility method to parse mod files to NeuroML

## Week 9-13

- Incorporate vShift in the channels to NeuroML:
    - Incorporated the vShift in channels like nat, sca using the channeldensityVShift to their respective segments
    - For the vShift2 defined for nat in the iseg, there was no other easy way than to add it to vShift. Lets say, we have vShift = 10 mV and vShift2 = -10.612 mV then the updated vShift = 10mV + -10.612mV to be used as above.
- Biophysical properties of the cell added to the NeuroML code and validated:
    - Homogeneous channels were activated one by one in both NEURON and NeuroML codes.
        - jNeuroML does not support multicompartmental cell models instead used pyneuroml to run the simulation on NEURON. 
        - Using the membrane potential plots for the segments soma, apical and tuft we were able to replicate the results of the NEURON code.
    - For the nonhomogeneous channels gmax was variable along the segments and were calculated on the basis of distance from the soma. Utilised the following strategy to check on the gmax values being set:
        - For the hoc code: Utilised the neuron gui model view option to view the gmax
        - For the neuroml code: Added print statements inside biophys_inhomogeneous() of neuroml generated neuron file
        - Worked with Ankur and improved the pyneuroml.neuron utils module to give information for the mechanisms on segment level
    - Added axonal, dendritic segments to the segment groups axon_group and dendrite_group respectively for better visualisation on OpenSourceBrain.
    - Added OMV tests on the multicompartmental cell for both NEURON and the LEMS file.
- Created an python script with BahlPyramidal cell class and methods to plot the simulated data
    - The class __init__ module:
        - added units to the parameters being passed to it
        - initialised variable parameters value as a string element 
    - Other methods include set_dendritic_amplitude(), create_pyr_cell(), create_pyr_network(), run_simulation() with their name revealing their functionalities.
- Epsp shaped dendritic input current
    - Defined a new component type inside epsp_input.xml. As the amplitude for the dendritic current is reset the epsp_tuft.xml is redefined with the new value.
- An interactive notebook to work with variations in input current to the multicompartmental cell as in the paper / issue:
    - Utility methods helped parse the hoc files parameter and to be further passed as argument to BahlPyramidal cell class.
    - Four variations combining the somatic pulse amplitude and dendritic amplitude were replicated
        - Readme is updated with the plots for that with parameters from the model2 for each of the cases.

