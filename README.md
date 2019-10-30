# MONET
This repository holds the source code for **MONET**, a Linux/macOS command-line toolbox to mine molecular and genetic networks, leveraging the top performing methods of the **Disease Module Identification (DMI) DREAM Challenge** (https://www.synapse.org/modulechallenge)

## Methods
* **K1**: Kernel clustering optimisation algorithm, https://www.synapse.org/#!Synapse:syn7349492/wiki/407359
* **M1**: Modularity optimization algorithm, https://www.synapse.org/#!Synapse:syn7352969/wiki/407384
* **R1**: Random-walk-based algorithm, https://www.synapse.org/#!Synapse:syn7286597/wiki/406659


## SOURCE CODE
The source code is hosted at: https://github.com/BergmannLab/MONET.git

## PREREQUISITES
Either ```docker``` or ```singularity``` must be installed. Please visit https://www.docker.com or http://singularity.lbl.gov

Some of the Methods may require large amount of resources, depending on your input.

The tool was tested on *Ubuntu Linux 18.04*, *CentOS Linux 7.5* and *macOS Sierra* Version 10.12.


## INSTALLATION
To install: ```./install.sh```

To uninstall: ```./uninstall.sh```

## RUNNING
To run, invoke, from any location: ```monet --help```

## INPUT
The format for the input network is the following: a tab-separated file containing one line for each edge. If an edge is connecting two nodes, nodeA and nodeB, with weight weight_AB, the file will contain the entry:

```[nodeA]	[nodeB]	[weight_AB]```

nodeA and nodeB are of type *integer*, weight_AB is of type *float*.


For an example, see the contents of test/system_test/input/.

## BENCHMARKING
see test/benchmarking

## PUBLICATIONS

Sarvenaz Choobdar, Mehmet Ahsen, Jake Crawford, Mattia Tomasoni, Tao Fang, David Lamparter, Junyuan Lin, Benjamin Hescott, Xiaozhe Hu, Johnathan Mercer, Ted Natoli, Rajiv Narayan, Aravind Subramanian, Jitao David Zhang, Gustavo Stolovitzky, Zoltán Kutalik, Kasper Lage, Donna Slonim, Julio Saez-Rodriguez, Lenore Cowen, Sven Bergmann. Community challenge assesses network module identification methods across complex diseases. Nature Methods (2019). doi: https://doi.org/10.1101/265553

Mattia Tomasoni, Sergio Gómez, Jake Crawford, Weijia Zhang, Sarvenaz Choobdar, Daniel Marbach and Sven Bergmann. MONET: MOdularising NEtwork Toolbox for mining of molecular and genetic networks. Preprints (2019). doi: https://doi.org/10.1101/611418



