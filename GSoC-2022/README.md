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
