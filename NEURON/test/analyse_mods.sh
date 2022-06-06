pynml-modchananalysis nat -stepV 5 -temperature [37] -modFile '../channels/nat.mod'
#pynml-modchananalysis nap -stepV 5 -temperature [37] -modFile '../channels/nap.mod'
pynml-modchananalysis kfast -stepV 5 -temperature 37
#pynml-modchananalysis km -stepV 5 -temperature [37] -modFile '../channels/IKM.mod'
#pynml-modchananalysis sca -stepV 5 -temperature [37] -modFile '../channels/SlowCa.mod'
#pynml-modchananalysis ih -stepV 5 -temperature [37] -modFile '../channels



#pynml-modchananalysis kca -stepV 5 -temperature [37] -modFile '../channels/kca.mod'/h.mod'
#pynml-modchananalysis kslow -stepV 10 -temperature [37] -duration 100000 -modFile '../channels/kslow.mod'  # Takes ~1hour...
