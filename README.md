# DreamDMI
This repository holds the source code for **DreamDMI**, a Linux/macOS command-line tool for Disease Module Identification in molecular networks, leveraging the top performing methods of the **Disease Module Identification (DMI) DREAM Challenge** (https://www.synapse.org/modulechallenge)

## Methods
* **K1**: Kernel clustering optimisation algorithm, https://www.synapse.org/#!Synapse:syn7349492/wiki/407359
* **M1**: Modularity optimization algorithm, https://www.synapse.org/#!Synapse:syn7352969/wiki/407384
* **R1**: Random-walk-based algorithm, https://www.synapse.org/#!Synapse:syn7286597/wiki/406659


## SOURCE CODE
The source code is hosted at: https://github.com/mattiat/DREAM_DMI_Tool

## PREREQUISITES
Either ```docker``` or ```singularity``` must be installed. Please visit https://www.docker.com or http://singularity.lbl.gov

Some of the Methods may require large amount of resources, depending on your input.

The tool was tested on *Ubuntu Linux 18.04*, *CentOS Linux 7.5* and *macOS Sierra* Version 10.12.


## INSTALLATION
To install: ```./install```

To uninstall: ```./uninstall```

## RUNNING
To run, invoke, from any location: ```dream_dmi --help```

## INPUT
The format for the input network is the following: a tab-separated file containing one line for each edge. If an edge is connecting two nodes, nodeA and nodeB, with weight weight_AB, the file will contain the entry:

```[nodeA]	[nodeB]	[weight_AB]```

nodeA and nodeB are of type *integer*, weight_AB is of type *float*.


For an example, see the contents of test/system_test/input/.

## BENCHMARKING
see test/benchmarking

## PUBLICATION
Open Community Challenge Reveals Molecular Network Modules with Key Roles in Diseases

Sarvenaz Choobdar, Mehmet E. Ahsen, Jake Crawford, Mattia Tomasoni, David Lamparter, Junyuan Lin, Benjamin Hescott, Xiaozhe Hu, Johnathan Mercer, Ted Natoli, Rajiv Narayan, The DREAM Module Identification Challenge Consortium, Aravind Subramanian, Gustavo Stolovitzky, Zoltán Kutalik, Kasper Lage, Donna K. Slonim, Julio Saez-Rodriguez, Lenore J. Cowen, Sven Bergmann, Daniel Marbach.
bioRxiv 265553 (2018). doi: https://doi.org/10.1101/265553
