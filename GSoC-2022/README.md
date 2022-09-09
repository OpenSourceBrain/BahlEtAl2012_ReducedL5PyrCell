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

## Week 9-13

