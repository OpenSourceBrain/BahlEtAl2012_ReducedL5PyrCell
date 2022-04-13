echo "Simulating using .mod file"
cd NEURON/channels
pynml-modchananalysis kfast -stepV 5 -temperature 37

cd ../../NeuroML2
pynml-channelanalysis kfast.channel.nml
echo "Simulating using .nml file"
