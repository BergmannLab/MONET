# MONET

This repository holds the source code for **MONET**, a Linux/macOS command-line toolbox to mine molecular and genetic networks, leveraging the top performing methods of the **Disease Module Identification (DMI) DREAM Challenge** (https://www.synapse.org/modulechallenge)

## Methods

Three methods are available as part of MONET. 

* **K1**: Kernel clustering optimisation algorithm, https://www.synapse.org/#!Synapse:syn7349492/wiki/407359

* **M1**: Modularity optimisation algorithm, https://www.synapse.org/#!Synapse:syn7352969/wiki/407384

* **R1**: Random-walk-based algorithm, https://www.synapse.org/#!Synapse:syn7286597/wiki/406659


## SOURCE CODE

The source code is hosted at: https://github.com/BergmannLab/MONET.git

## PREREQUISITES

The tool was tested on *Ubuntu Linux 18.04*, *CentOS Linux 7.5* and *macOS Sierra* Version 10.12.

* Software: either ```docker``` or ```singularity``` must be installed. Please visit https://www.docker.com or http://singularity.lbl.gov
* memory: some of the methods require large amount of resources, depending on your input. To fully reproduce the results of the DREAM challenge, around 40GB of memory are required

## INSTALLATION

To install: 

```$ git clone https://github.com/BergmannLab/MONET.git```

```$ cd MONET && ./install.sh```

A folder MONET will have been created with the source code: you are free to remove it, if you are not interested. The command ```monet --help``` can be invoked from any location on the system (like ```ls``` or ```pwd```).

## RUNNING

From any location on your machine, you can use the following example command: it will run method M1 on a network container in your tmp folder using docker. For details about input format, parameters and output, read the rest of this document.

```$ monet --help```

```$ monet --input=/tmp/input_network.txt —-method=M1 --container=docker```

## INPUT

The format for the input network is the following: a tab-separated file containing one line for each edge. If an edge is connecting two nodes, nodeA and nodeB, with weight weight_AB, the file will contain the entry:

```[nodeA]	[nodeB]	[weight_AB]```

nodeA and nodeB are of type *integer*, weight_AB is of type *float*.

For an example, see the contents of MONET/test/system_test/input/


## PARAMETERS

Please, provide values for the following MANDATORY parameters:

* --input: path to the network file to be analysed

* --method: method to be used to analyse the input: [K1|M1|R1]

* --container: virtualisation technology available on the system: [docker|singularity]


## OPTIONAL

You may provide values for the following parameter:

* --output: directory in which to output results (default is current directory)


OPTIONS for M1; if you select M1 as a method, you may provide the following: 

* --linksdir: directionality of links: [undirected|directed] (default is undirected)

* --avgk: desired average degree for nodes in output (default is 25)

* --smallest: min size of output clusters (default is 3)

* --largest: max size of output clusters (default is 100)


OPTIONS for R1; if you select R1 as a method, you may provide the following: 

* --c: trade-off parameter for computational efficiency: for larger c, the algorithm will run slower, but may provide more accurate results (default is 800)

* --i: inflation parameter for standard Markov Clustering algorithm on which R1 is based (default is 2)

* --b: parameter controlling how balanced the clustering results should be; for b=0, R1 behaves like standard Regularized Markov Cluster (default is 2)

* --threshold: remove edges smaller than threshold from the input (default is 4)

* --smallest: min size of output clusters (default is 3)

* --largest: max size of output clusters (default is 100)

* --post: decide whether to recursively cluster (recluster) or discard too large output clusters: [recluster|discard] (default is discard)

* --c2: (only used if --post=recluster) sets —-c for reclustering round (default is 500)

* --i2: (only used if --post=recluster) sets —-i for reclustering round (default is 2)

* —-b2: (only used if --post=recluster) sets —-b for reclustering round (default is 2)


## OUTPUT

Two output files will be generated in the directory where you run the command, marked with a timestamp and the name of your input network: one file containing the run-time outputs and the other containing the results of your analysis.

## BENCHMARKING

Please refer to MONET/test/benchmarking.

## QUESTIONS / BUG-REPORTS

Please, address your questions and bug reports to Mattia Tomasoni, <mattia.tomasoni AT unil.ch>. An issue will be opened here to address your problem: https://github.com/BergmannLab/MONET/issues

## CONTRIBUTING

If you are interested in contributing to MONET, we encourage you to get in touch! We will be happy to add you to the list of our developers https://github.com/BergmannLab/MONET/graphs/contributors

## PUBLICATIONS

Sarvenaz Choobdar, Mehmet Ahsen, Jake Crawford, Mattia Tomasoni, Tao Fang, David Lamparter, Junyuan Lin, Benjamin Hescott, Xiaozhe Hu, Johnathan Mercer, Ted Natoli, Rajiv Narayan, Aravind Subramanian, Jitao David Zhang, Gustavo Stolovitzky, Zoltán Kutalik, Kasper Lage, Donna Slonim, Julio Saez-Rodriguez, Lenore Cowen, Sven Bergmann. Assessment of network module identification across complex diseases. Nature Methods 16 (2019) 843-852. doi: https://doi.org/10.1038/s41592-019-0509-5

Mattia Tomasoni, Sergio Gómez, Jake Crawford, Weijia Zhang, Sarvenaz Choobdar, Daniel Marbach and Sven Bergmann. MONET: MOdularising NEtwork Toolbox for mining of molecular and genetic networks. Preprints (2019). doi: https://doi.org/10.1101/611418



