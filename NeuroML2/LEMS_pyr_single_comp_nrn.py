'''
Neuron simulator export for:

Components:
    null (Type: notes)
    null (Type: notes)
    null (Type: notes)
    pas (Type: ionChannelPassive:  conductance=1.0E-11 (SI conductance))
    null (Type: notes)
    km (Type: ionChannelHH:  conductance=1.0E-11 (SI conductance))
    pyr_cell (Type: cell)
    pg (Type: pulseGenerator:  delay=0.1 (SI time) duration=0.5 (SI time) amplitude=4.0000000000000007E-10 (SI current))
    single_pyr_cell_network (Type: networkWithTemperature:  temperature=310.15 (SI temperature))
    pyr_single_comp (Type: Simulation:  length=0.7000000000000001 (SI time) step=1.0E-5 (SI time))


    This NEURON file has been generated by org.neuroml.export (see https://github.com/NeuroML/org.neuroml.export)
         org.neuroml.export  v1.9.0
         org.neuroml.model   v1.9.0
         jLEMS               v0.10.7

'''

import neuron

import time
import datetime
import sys

import hashlib
h = neuron.h
h.load_file("nrngui.hoc")

h("objref p")
h("p = new PythonObject()")

class NeuronSimulation():

    def __init__(self, tstop, dt, seed=123):

        print("\n    Starting simulation in NEURON of %sms generated from NeuroML2 model...\n"%tstop)

        self.setup_start = time.time()
        self.seed = seed
        self.randoms = []
        self.next_global_id = 0  # Used in Random123 classes for elements using random(), etc. 

        self.next_spiking_input_id = 0  # Used in Random123 classes for elements using random(), etc. 

        '''
        Adding simulation Component(id=pyr_single_comp type=Simulation) of network/component: single_pyr_cell_network (Type: networkWithTemperature:  temperature=310.15 (SI temperature))
        
        '''

        # Temperature used for network: 310.15 K
        h.celsius = 310.15 - 273.15

        # ######################   Population: pop0
        print("Population pop0 contains 1 instance(s) of component: pyr_cell of type: cell")

        h.load_file("pyr_cell.hoc")
        a_pop0 = []
        h("{ n_pop0 = 1 }")
        h("objectvar a_pop0[n_pop0]")
        for i in range(int(h.n_pop0)):
            h("a_pop0[%i] = new pyr_cell()"%i)
            h("access a_pop0[%i].soma"%i)

            self.next_global_id+=1


        h("proc initialiseV_pop0() { for i = 0, n_pop0-1 { a_pop0[i].set_initial_v() } }")
        h("objref fih_pop0")
        h('{fih_pop0 = new FInitializeHandler(0, "initialiseV_pop0()")}')

        h("proc initialiseIons_pop0() { for i = 0, n_pop0-1 { a_pop0[i].set_initial_ion_properties() } }")
        h("objref fih_ion_pop0")
        h('{fih_ion_pop0 = new FInitializeHandler(1, "initialiseIons_pop0()")}')

        # Adding single input: Component(id=null type=explicitInput)
        h("objref explicitInput_pga_pop0_0__soma")
        h("a_pop0[0].soma { explicitInput_pga_pop0_0__soma = new pg(0.5) } ")

        trec = h.Vector()
        trec.record(h._ref_t)

        h.tstop = tstop

        h.dt = dt

        h.steps_per_ms = 1/h.dt



        # ######################   File to save: pyr_single_comp.ikm_m.dat (ikm_m)
        # Column: pop0[0]/pyr_b_prop/membraneProperties/km_channels/km/m/q
        h(' objectvar v_pop0_0__ikm_m_ikm_m ')
        h(' { v_pop0_0__ikm_m_ikm_m = new Vector() } ')
        h(' { v_pop0_0__ikm_m_ikm_m.record(&a_pop0[0].soma.m_q_km(0.5)) } ')
        h.v_pop0_0__ikm_m_ikm_m.resize((h.tstop * h.steps_per_ms) + 1)

        # ######################   File to save: time.dat (time)
        # Column: time
        h(' objectvar v_time ')
        h(' { v_time = new Vector() } ')
        h(' { v_time.record(&t) } ')
        h.v_time.resize((h.tstop * h.steps_per_ms) + 1)

        # ######################   File to save: pyr_single_comp.dat (output0)
        # Column: pop0[0]/v
        h(' objectvar v_pop0_0__v_output0 ')
        h(' { v_pop0_0__v_output0 = new Vector() } ')
        h(' { v_pop0_0__v_output0.record(&a_pop0[0].soma.v(0.5)) } ')
        h.v_pop0_0__v_output0.resize((h.tstop * h.steps_per_ms) + 1)

        self.initialized = False

        self.sim_end = -1 # will be overwritten

        setup_end = time.time()
        self.setup_time = setup_end - self.setup_start
        print("Setting up the network to simulate took %f seconds"%(self.setup_time))

        h.nrncontrolmenu()


    def run(self):

        self.initialized = True
        sim_start = time.time()
        print("Running a simulation of %sms (dt = %sms; seed=%s)" % (h.tstop, h.dt, self.seed))

        try:
            h.run()
        except Exception as e:
            print("Exception running NEURON: %s" % (e))
            return


        self.sim_end = time.time()
        self.sim_time = self.sim_end - sim_start
        print("Finished NEURON simulation in %f seconds (%f mins)..."%(self.sim_time, self.sim_time/60.0))

        try:
            self.save_results()
        except Exception as e:
            print("Exception saving results of NEURON simulation: %s" % (e))
            return


    def advance(self):

        if not self.initialized:
            h.finitialize()
            self.initialized = True

        h.fadvance()


    ###############################################################################
    # Hash function to use in generation of random value
    # This is copied from NetPyNE: https://github.com/Neurosim-lab/netpyne/blob/master/netpyne/simFuncs.py
    ###############################################################################
    def _id32 (self,obj): 
        return int(hashlib.md5(obj.encode('utf-8')).hexdigest()[0:8],16)  # convert 8 first chars of md5 hash in base 16 to int


    ###############################################################################
    # Initialize the stim randomizer
    # This is copied from NetPyNE: https://github.com/Neurosim-lab/netpyne/blob/master/netpyne/simFuncs.py
    ###############################################################################
    def _init_stim_randomizer(self,rand, stimType, gid, seed): 
        #print("INIT STIM  %s; %s; %s; %s"%(rand, stimType, gid, seed))
        rand.Random123(self._id32(stimType), gid, seed)


    def save_results(self):

        print("Saving results at t=%s..."%h.t)

        if self.sim_end < 0: self.sim_end = time.time()


        # ######################   File to save: time.dat (time)
        py_v_time = [ t/1000 for t in h.v_time.to_python() ]  # Convert to Python list for speed...

        f_time_f2 = open('time.dat', 'w')
        num_points = len(py_v_time)  # Simulation may have been stopped before tstop...

        for i in range(num_points):
            f_time_f2.write('%f'% py_v_time[i])  # Save in SI units...
        f_time_f2.close()
        print("Saved data to: time.dat")

        # ######################   File to save: pyr_single_comp.ikm_m.dat (ikm_m)
        py_v_pop0_0__ikm_m_ikm_m = [ float(x ) for x in h.v_pop0_0__ikm_m_ikm_m.to_python() ]  # Convert to Python list for speed, variable has dim: none

        f_ikm_m_f2 = open('pyr_single_comp.ikm_m.dat', 'w')
        num_points = len(py_v_time)  # Simulation may have been stopped before tstop...

        for i in range(num_points):
            f_ikm_m_f2.write('%e\t%e\t\n' % (py_v_time[i], py_v_pop0_0__ikm_m_ikm_m[i], ))
        f_ikm_m_f2.close()
        print("Saved data to: pyr_single_comp.ikm_m.dat")

        # ######################   File to save: pyr_single_comp.dat (output0)
        py_v_pop0_0__v_output0 = [ float(x  / 1000.0) for x in h.v_pop0_0__v_output0.to_python() ]  # Convert to Python list for speed, variable has dim: voltage

        f_output0_f2 = open('pyr_single_comp.dat', 'w')
        num_points = len(py_v_time)  # Simulation may have been stopped before tstop...

        for i in range(num_points):
            f_output0_f2.write('%e\t%e\t\n' % (py_v_time[i], py_v_pop0_0__v_output0[i], ))
        f_output0_f2.close()
        print("Saved data to: pyr_single_comp.dat")

        save_end = time.time()
        save_time = save_end - self.sim_end
        print("Finished saving results in %f seconds"%(save_time))

        print("Done")

if __name__ == '__main__':

    ns = NeuronSimulation(tstop=700, dt=0.01, seed=123)

    ns.run()

