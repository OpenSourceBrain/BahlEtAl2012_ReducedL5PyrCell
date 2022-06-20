echo "Simulating using .mod file"
cd NEURON/channels
pynml-modchananalysis kfast -stepV 5 -temperature 37
# pynml-modchananalysis -temperature 37 -modFile IKM.mod km 

cd ../../NeuroML2
pynml-channelanalysis kfast.channel.nml
echo "Simulating using .nml file"
