# ReducedL5PyrCell_BahlEtAl2012

[![Continuous build using OMV](https://github.com/OpenSourceBrain/BahlEtAl2012_ReducedL5PyrCell/actions/workflows/omv-ci.yml/badge.svg)](https://github.com/OpenSourceBrain/BahlEtAl2012_ReducedL5PyrCell/actions/workflows/omv-ci.yml)

A set of reduced models of layer 5 pyramidal neurons from: **Automated optimization of a reduced layer 5 pyramidal cell model based on experimental data** [Bahl et al. 2012](https://www.sciencedirect.com/science/article/pii/S016502701200129X) 

## Conversion to NeuroML

See https://github.com/OpenSourceBrain/Contribute/issues/15 for issue related to this.

### Channels

At the moment only the transient sodium channel is converted. To compare the activation curves run

```
./compare_na_channels.sh
```
