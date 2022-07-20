
import matplotlib.pyplot as pylab
import os.path
import sys
import airspeed


chans = ['nat', 'nap', 'kfast', 'kslow', 'km', 'ih', 'sca']

problematic = []

gates = ['m', 'h', 'n', 'a', 'b', 'b1', 'qq']

temperatures = [37]

MD_TEMPLATE_FILE = "./template.md"

OUTPUT_DIR = os.getcwd()

def merge_with_template(model, templfile):
    if not os.path.isfile(templfile):
        templfile = os.path.join(os.path.dirname(sys.argv[0]), templfile)
    with open(templfile) as f:
        templ = airspeed.Template(f.read())
    return templ.merge(model)

def make_md_file():
    for temperature in temperatures:
        info = {
        "info": (
            "Channel information at: "
            "T = %s degC "
        )
        % (temperature),
        "channels": chans,
        }
    merged = merge_with_template(info, MD_TEMPLATE_FILE)
    new_md_file = os.path.join(OUTPUT_DIR, "README.md")
    lf = open(new_md_file, "w")
    lf.write(merged)
    lf.close()

def main():  
    for temperature in temperatures:

        for channel_id in chans:

            vramp_lems_file  = '../%s.rampV.lems.dat'%(channel_id)

            ts = []
            volts = []
            for line in open(vramp_lems_file):
                ts.append(float(line.split()[0])*1000)
                volts.append(float(line.split()[1])*1000)

            fig = pylab.figure("Time Course(s) of activation variables of %s at %sdegC"%(channel_id, temperature))

            pylab.xlabel('Membrane potential (mV)')
            pylab.ylabel('Time Course - tau (ms)')
            pylab.grid('on')

            for gate in gates:

                tau_lems_file  = '../%s.%s.tau.lems.dat'%(channel_id, gate)

                if os.path.isfile(tau_lems_file):
                    taus = []
                    for line in open(tau_lems_file):
                        ts.append(float(line.split()[0])*1000)
                        taus.append(float(line.split()[1])*1000)

                    pylab.plot(volts, taus, linestyle='-', linewidth=2, label="LEMS %s %s tau"%(channel_id, gate))

                    tau_mod_file  = '../../NEURON/channels/%s.%s.tau.dat'%(channel_id, gate)
                    vs = []
                    taus = []
                    for line in open(tau_mod_file):
                        vs.append(float(line.split()[0]))
                        taus.append(float(line.split()[1]))

                    pylab.plot(vs, taus, '--x', label="Mod %s %s tau"%(channel_id, gate))

            pylab.legend()
            tau_png_file = './%s.tau.png'%(channel_id)
            pylab.savefig(tau_png_file)


            fig = pylab.figure("Steady state(s) of activation variables of %s at %sdegC"%(channel_id, temperature))

            pylab.xlabel('Membrane potential (mV)')
            pylab.ylabel('Steady state (inf)')
            pylab.grid('on')

            for gate in gates:

                inf_lems_file  = '../%s.%s.inf.lems.dat'%(channel_id, gate)

                if os.path.isfile(inf_lems_file):
                    infs = []
                    for line in open(inf_lems_file):
                        infs.append(float(line.split()[1]))

                    pylab.plot(volts, infs, linestyle='-', linewidth=2, label="LEMS %s %s inf"%(channel_id, gate))

                    inf_mod_file  = '../../NEURON/channels/%s.%s.inf.dat'%(channel_id, gate)
                    vs = []
                    infs = []
                    for line in open(inf_mod_file):
                        vs.append(float(line.split()[0]))
                        infs.append(float(line.split()[1]))

                    pylab.plot(vs, infs, '--x', label="Mod %s %s inf"%(channel_id, gate))

            pylab.legend()
            inf_png_file = './%s.inf.png'%(channel_id)
            pylab.savefig(inf_png_file)
    make_md_file()

    # pylab.show()

if __name__ == "__main__":
    main()