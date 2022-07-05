echo "Simulating using .mod file"
cd NEURON/channels
#pynml-modchananalysis km -stepV 5 -temperature 37
pynml-modchananalysis -temperature 37 -modFile IKM.mod km

cd ../../NeuroML2
pynml-channelanalysis IKM.channel.nml -step 5 -temperature 37
echo "Simulating using .nml file"
