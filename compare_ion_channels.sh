echo "Simulating using .mod file"
cd NEURON/channels
#pynml-modchananalysis km -stepV 5 -temperature 37
#pynml-mochananalysis nat -stepV 5 -temperature 37 -dt 0.0025
#pynml-modchananalysis kslow -stepV 10 -temperature 37 -duration 100000 -modFile './NEURON/channels/kslow.mod'  # Takes ~45mins
pynml-modchananalysis -temperature 37 -modFile IKM.mod km

echo "Simulating using .nml file"
cd ../../NeuroML2
pynml-channelanalysis IKM.channel.nml -step 5 -temperature 37
#  pynml-channelanalysis sca.channel.nml -temperature 37 -scaleDt 0.25 -caConc 5e-05
