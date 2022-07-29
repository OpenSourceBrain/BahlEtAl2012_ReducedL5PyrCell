Channel information
===================
    
<p style="font-family:arial">Channel information at: T = 37.0 degC, E_rev = 0 mV, [Ca2+] = 5e-05 mM</p>

<div style="border:solid 2px white; padding-left:10px">
<div>
<b>nap</b><br/>
<a href="../nap.channel.nml">nap.channel.nml</a>
     <br/>
        <b>Ion: na</b><br/>
        <b>
        <i><code>g = gmax * m </code></i><br/>
        </b>
        </div>

        NeuroML2 file automatically generated from NMODL file: ./NEURON/channels/nap.mod
<div><a href="nap.inf.png"><img alt="nap steady state" src="nap.inf.png" height="250" width="300" style="padding:10px 35px 10px 0px"/></a>
<a href="nap.tau.png"><img alt="nap time course" src="nap.tau.png" height="250" width="300" style="padding:10px 10px 10px 0px"/></a>
</div>
</div>
<div style="border:solid 2px white; padding-left:10px">
<div>
<b>nat</b><br/>
<a href="../nat.channel.nml">nat.channel.nml</a>
     <br/>
        <b>Ion: na</b><br/>
        <b>
        <i><code>g = gmax * m<sup>3</sup> * h </code></i><br/>
        </b>
        </div>

        Sodium channel, Hodgkin-Huxley style kinetics.
            Comments from original mod file:
            26 Ago 2002 Modification of original channel to allow variable time step and to correct an initialization
            error.
            Done by Michael Hines(michael.hines@yale.e) and Ruggero Scorcioni(rscorcio@gmu.edu) at EU Advance Course in
            Computational Neuroscience. Obidos, Portugal
            Sodium channel, Hodgkin-Huxley style kinetics.
            Kinetics were fit to data from Huguenard et al. (1988) and Hamill et
            al. (1991)
            qi is not well constrained by the data, since there are no points
            between -80 and -55. So this was fixed at 5 while the thi1,thi2,Rg,Rd
            were optimized using a simplex least square proc.
            Voltage dependencies are shifted approximately from the best
            fit to give higher threshold
            Author: Zach Mainen, Salk Institute, 1994, zach@salk.edu
            May 2006: set the tha -28 mV, vshift 0 and thinf -55 mV to comply with measured
            Somatic Na+ kinetics in neocortex. Kole, ANU, 2006
        
<div><a href="nat.inf.png"><img alt="nat steady state" src="nat.inf.png" height="250" width="300" style="padding:10px 35px 10px 0px"/></a>
<a href="nat.tau.png"><img alt="nat time course" src="nat.tau.png" height="250" width="300" style="padding:10px 10px 10px 0px"/></a>
</div>
</div>
<div style="border:solid 2px white; padding-left:10px">
<div>
<b>kfast</b><br/>
<a href="../kfast.channel.nml">kfast.channel.nml</a>
     <br/>
        <b>Ion: k</b><br/>
        <b>
        <i><code>g = gmax * n </code></i><br/>
        </b>
        </div>

        Potassium channel, Hodgkin-Huxley style kinetics
            Comments from original mod file:
            26 Ago 2002 Modification of original channel to allow variable time step and to correct an initialization error.
            Done by Michael Hines(michael.hines@yale.e) and Ruggero Scorcioni(rscorcio@gmu.edu) at EU Advance Course in Computational Neuroscience. Obidos, Portugal
            Potassium channel, Hodgkin-Huxley style kinetics
            Kinetic rates based roughly on Sah et al. and Hamill et al. (1991)
            Author: Zach Mainen, Salk Institute, 1995, zach@salk.edu
        
<div><a href="kfast.inf.png"><img alt="kfast steady state" src="kfast.inf.png" height="250" width="300" style="padding:10px 35px 10px 0px"/></a>
<a href="kfast.tau.png"><img alt="kfast time course" src="kfast.tau.png" height="250" width="300" style="padding:10px 10px 10px 0px"/></a>
</div>
</div>
<div style="border:solid 2px white; padding-left:10px">
<div>
<b>km</b><br/>
<a href="../IKM.channel.nml">IKM.channel.nml</a>
     <br/>
        <b>Ion: k</b><br/>
        <b>
        <i><code>g = gmax * m </code></i><br/>
        </b>
        </div>

        NeuroML2 file automatically generated from NMODL file: ./NEURON/channels/IKM.mod
<div><a href="km.inf.png"><img alt="km steady state" src="km.inf.png" height="250" width="300" style="padding:10px 35px 10px 0px"/></a>
<a href="km.tau.png"><img alt="km time course" src="km.tau.png" height="250" width="300" style="padding:10px 10px 10px 0px"/></a>
</div>
</div>

<div style="border:solid 2px white; padding-left:10px">
<div>
<b>km</b><br/>
<a href="../kslow.channel.nml">kslow.channel.nml</a>
     <br/>
        <b>Ion: k</b><br/>
        <b>
        <i><code>g = gmax * a<sup>2</sup> * (0.5*b+0.5*b1)</code></i><br/>
        </b>
        </div>

        NeuroML2 file automatically generated from NMODL file: ./NEURON/channels/kslow.mod. 
        Example of a fractional gate. Steady state plots for bb and bb1 fractional gates overlap.
<div><a href="kslow.inf.png"><img alt="kslow steady state" src="kslow.inf.png" height="250" width="300" style="padding:10px 35px 10px 0px"/></a>
<a href="kslow.tau.png"><img alt="kslow time course" src="kslow.tau.png" height="250" width="300" style="padding:10px 10px 10px 0px"/></a>
</div>
</div>
<div style="border:solid 2px white; padding-left:10px">
<div>
<b>ih</b><br/>
<a href="../ih.channel.nml">ih.channel.nml</a>
     <br/>
        <b>Ion: hcn</b><br/>
        <b>
        <i><code>g = gmax * qq </code></i><br/>
        </b>
        </div>

        Deterministic model of kinetics and voltage-dependence of Ih-currents
                in layer 5 pyramidal neuron, see Kole et al., 2006. Implemented by
                Stefan Hallermann.

                Added possibility to shift voltage activiation (vshift) and allowed access to gating variables, Armin Bahl 2009

                Predominantly HCN1 / HCN2
        
<div><a href="ih.inf.png"><img alt="ih steady state" src="ih.inf.png" height="250" width="300" style="padding:10px 35px 10px 0px"/></a>
<a href="ih.tau.png"><img alt="ih time course" src="ih.tau.png" height="250" width="300" style="padding:10px 10px 10px 0px"/></a>
</div>
</div>

