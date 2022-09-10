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
- To test the neuroml single compartmental cell file NEURON (hoc) test files just including the soma is created
    - Added plots of the activation / inactivation variables for all the channels to help debug in case of inconsistency in results
- Added the summary plots of the channels converted to neuroml to a directory
    - Density mechanisms are first validated using pyneuroml -validate 
    - Summary plots include time course and steady state of the the different gates involved in the channel
    - Faced issue to plot for kslow channel (fractional gate) using pynml-channelanalysis. Hence, created a LEMS file kslow channel to get the simulation saved as dat files
    - Upgraded the channel info template to a different style with no text flowing inside the pyNeuroML library that helps render the plots and notes for the channels in the channel summary directory
- Comparison of LEMS and mod files for all the channels
    - Created a script inside the directory that updates a readme, comparing steady state and time course of each channel gates (activation / inactivation) variables using LEMS and mod files
- NeuroML implementation of the single compartmental cell (soma) adding each channel one by one
    - Understand the change on activation / inactivation variables (gates) with variable pulse inputs
    - Inferential study of the characteristics of the channels involved 
    - Added OMV test for the LEMS file in ./NeuroML2 across two simulation engines i.e. jNeuroML_NEURON and jNeuroML where spikes are assumed and checked above a threshold and a set tolerance level

## Week 5 - 8
- Converted the ca dependent mechanisms namely (cad, sca, kca) to NeuroML
    - Understood the dynamics of them from their mod files and followed some of the previous works that involved conversion of such ca dependent mechanisms
    - Compared the LEMS and mod file for sca channel and added to the compare_nml2_mods directory
- Validated the ca dependent channels on single compartmental cell
    - Created a NEURON hoc file including the three mechanisms, and recorded the cai (internal ca concentration), cao (outer ca concentration) and ica (ca current produced)
    - Created a neuroml cell with just the soma including leak, sca and kca as channel densities, while adding the cad as intracellular properties. The notebook included plots as above.
    - To debug the discrepancies in the plots, I followed a strategy of setting the conductance for sca, kca to 0 and see how eca and ica changes for both NEURON as well as NeuroML code and increasing the conductance one by one
    - ECA used was not being calculated using the nernst / ghk equation instead was fixed. Other than that, there was a correction to the units of caConc in the neuroml file for kca.
    - OMV tests were added for LEMS and hoc code which ran on three simulation engines namely : jNeuroML, jNeuroML_NEURON, jNeuroML_NetPyNE
- Created a test file for example 1 which was able to record from 3 different locations of the cell namely Soma, Apical, Tuft. 
- Morphology of the multi compartmental cell is exported from the hoc format to neuroml using export_nml2.py on the test file created above.
- parse_mod_file.py : Adding the necessary information related to the conversion of the channel ( parameters and procedures) as comments to the converted neuroml file. This extra information can be deleted afterwards. 
    - Moved the script along with the mod files to improve and test to the repository NEURONShowcase 
    - Added the tutorial notebook showing how to use the utility method to parse mod files to nml

## Week 9-13

- vShift in the channels:
    - Incorporated the vShift in channels like nat, sca using the channeldensityVShift to their respective segments as in the original NEURON code
    - For the vShift2 defined for nat in the iseg, there was no other easy way than to add it to vShift. Lets say, we have vShift = 10 mV and vShift2 = -10.612 mV then the updated vShift = 10mV + -10.612mV to be used as above.
- Biophysical properties of the cell added to the NeuroML code and validated:
    - Homogeneous channels were activated one by one in both NEURON and NeuroML codes.
        - jNeuroML does not support multicompartmental cell models instead used pyneuroml to run the simulation on NEURON. 
        - Using the membrane potential plots for the segments soma, apical and tuft we were able to replicate the results of the NEURON code.
    - For the Nonhomogeneous channels gmax was variable along the segments and were calculated on the basis of distance from the soma. Utilised the following strategy to check on the gmax values being set:
        - For the hoc code: Utilised the neuron gui model view option to view the gmax along the segments
        - For the neuroml code: Added print statements inside biophys_inhomogeneous() inside the neuroml generated neuron file
        - Worked with Ankur and improved the pyneuroml.neuron utils module to give information for the mechanisms on segment level
    - Added axonal, dendritic segments to the segment groups axon_group and dendrite_group respectively. This helps us to better visualise the neuroml cell on OpenSourceBrain
    - Added OMV tests on the multicompartmental cell for both NEURON as well as for the LEMS file generated from the NeuroML code. Currently the tests are failing for NEURON 8 and above and being looked into in a separate branch.
- Created an python script with BahlPyramidal cell class and methods to plot the simulated results 
    - Class constitutes the __init__ module majorly to:
        - add units to the parameters being passed as arguments.
        - variable parameters value are initialised as a string element 
    - Other methods include create_pyr_cell(), create_pyr_network(), run_simulation() with their name revealing their functionalities.
- Epsp shaped dendritic input current
    - Defined a new component type in epsp_input.xml. As the amplitude for epsp current is reset the epsp_tuft.xml is redefined with the new value.
    - The *.xml file is included in the LEMSSimulation using include_lems_file module.
- An interactive notebook to work with variations in input current to the multicompartmental cell as in the paper / issue:
    - Notebook has utility methods that helped parse the hoc files parameter and initialise them as variables to be further passed as argument to BahlPyramidal cell class.
    - Four variations were tried combining the somatic pulse amplitude and dendritic amplitude referenced from the paper.
        - Readme is updated with the plots with parameters from the model2 for each of the cases.

