# MONET

This repository holds the source code for **MONET**, a Linux/macOS command-line toolbox to mine molecular and genetic networks, leveraging the top performing methods of the **Disease Module Identification (DMI) DREAM Challenge** (https://www.synapse.org/modulechallenge)

## SOURCE CODE

The source code is hosted at: https://github.com/BergmannLab/MONET.git

## PREREQUISITES

The tool was tested on *Ubuntu Linux 18.04*, *CentOS Linux 7.5* and *macOS Sierra* Version 10.12.

Either ```docker``` or ```singularity``` must be installed. Please visit https://www.docker.com or http://singularity.lbl.gov

## INSTALLATION

To install: 

```$ git clone https://github.com/BergmannLab/MONET.git```

```$ cd MONET && ./install.sh```

A folder MONET will have been created with the source code: you are free to remove it, if you are not interested. This will not affect MONET, which has now being installed in your system: the command ```monet``` can be invoked from any location on the system (like any other command, like ```ls``` or ```pwd```).

## MONET HELP COMMAND

After installing MONET, the help command ```monet --help``` will be available from any location on your system.

## RUNNING

Once installed, from any location on your system, you can run the following example command: it will run a method called M1 (see section METHODS for details), on a network contained in your tmp folder (see section INPUT for details), using docker virtualization (see section PREREQUISITES for details). In the remainder of this document, you will find details about what parameters you can use, what to expect as an output and resource usage (in the PARAMETRS,  OUTPUT and COMPUTATIONAL RESOURCES sections respectively).

```$ monet --help```

```$ monet --input=/tmp/input_network.txt —-method=M1 --container=docker```

## INPUT

The format for the input network is the following: a **tab-separated** file containing one line for each edge. 

If an edge is connecting two nodes, gene_a and gene_b, with weight 1, the file will contain the line:

```gene_a /t gene_b /t 1 /n```

Data type:
* gene_a and gene_b can be either *sting* or *integer*
* weigth can be of type type *integer* or *float*
* "/t" indicates the tab character and "/n" a newline

For an example, see MONET/test/system_test/input/zachary_karate_club.txt. The same folder containing the actual inputs to the Disease Module Identification (DMI) DREAM Challenge. Beware that some of the inputs will require high amounts of computational resources and are not suited to be run on a simple laptop or desktop computer; please refer to section COMPUTATIONAL RESOURCES for details.

## OUTPUT

Two output files will be generated in the directory where you run the command, marked with a timestamp and the name of your input network: one file containing the run-time outputs and the other containing the results of your analysis.

## METHODS

Three methods are available as part of MONET, which emerged as the top-performing methods of the DREAM Challenge.

In order to run one of the three methods, adapt the example command provided in section RUNNING providing the --method option with the name of the chosen method (--method=[K1|M1|R1], for details, see section PARAMETERS).

* **K1**: KERNEL CLUSTERING OPTIMISATION algorithm. K1 is based on the “Diffusion State Distance” (DSD), a novel graph metric which is built on the premise that paths through low-degree nodes are stronger indications of functional similarity than paths that traverse highdegree nodes by Cao et al. (2014). The DSD metric is used to define a pairwise distance matrix between all nodes, on which a spectral clustering algorithm is applied. In parallel, dense bipartite sub-graphs are identified using standard graph techniques. Finally, results are merged into a single set of non-overlapping clusters. For further details, please see: https://www.synapse.org/#!Synapse:syn7349492/wiki/407359

* **M1**: MODULARITY OPTIMIZATION algorithm. M1 employs an original technique named Multiresolution introduced by (Arenas et al., 2008) to explore all topological scales at which modules may be found. The novelty of this approach relies on the introduction of a parameter, called resistance, which controls the aversion of nodes to form modules. Modularity (Newman and Girvan, 2004; Arenas et al., 2007) is optimized using an ensemble of algorithms: Extremal optimization (Duch
and Arenas, 2005), Spectral optimization (Newman, 2006), Fast algorithm (Newman, 2004), Tabu search (Arenas et al., 2008), and fine-tuning by iterative repositioning of individual nodes in adjacent modules. For further details, please see: https://www.synapse.org/#!Synapse:syn7352969/wiki/407384

* **R1**: RANDOM-WALK-BASED algorithm. R1 is based on a variant ofMarkov Cluster Algorithmknown as balancedMulti-layer Regularized Markov Cluster Algorithm(bMLRMCL)(Satuluriet al., 2010) which scales well to large graphs and minimizes the number ofoversized clusters. First, a pre-processing step is applied so that edges withlow weights are discarded and all remaining edges are scaled to integervalues. Then,bMLRMCLis applied iteratively on modules of size graterthan a user-defined threshold. For further details, please see: https://www.synapse.org/#!Synapse:syn7286597/wiki/406659

## PARAMETERS

Please, provide values for the following MANDATORY parameters:

* **--input**: path to the network file to be analysed

* **--method**: method to be used to analyse the input: [K1|M1|R1]

* **--container**: virtualisation technology available on the system: [docker|singularity]


## OPTIONAL PARAMETERS

You may provide values for the following parameter:

* **--output**: directory in which to output results (default is current directory)


OPTIONS for M1; **if you select M1** as a method, you may additionally provide the following: 

* --linksdir: directionality of links: [undirected|directed] (default is undirected)

* --avgk: desired average degree for nodes in output (default is 25)

* --smallest: min size of output clusters (default is 3)

* --largest: max size of output clusters (default is 100)


OPTIONS for R1; **if you select R1** as a method, you may additionally provide the following: 

* --c: trade-off parameter for computational efficiency: for larger c, the algorithm will run slower, but may provide more accurate results (default is 800)

* --i: inflation parameter for standard Markov Clustering algorithm on which R1 is based (default is 2)

* --b: parameter controlling how balanced the clustering results should be; for b=0, R1 behaves like standard Regularized Markov Cluster (default is 2)

* --threshold: remove edges smaller than threshold from the input (default is 4)

* --smallest: min size of output clusters (default is 3)

* --largest: max size of output clusters (default is 100)

* --post: decide whether to recursively cluster (recluster) or discard too large output clusters: [recluster|discard] (default is discard)

* --c2: (only used if --post=recluster) sets --c for reclustering round (default is 500)

* --i2: (only used if --post=recluster) sets --i for reclustering round (default is 2)

* --b2: (only used if --post=recluster) sets --b for reclustering round (default is 2)

## COMPUTATIONAL RESOURCES

Some of the methods require large amount of resources, depending on your input (please, refer to the MONET paper in the PUBLICATIONS section for details about how resource needs will scale with the size of the input, for the different methods). 

To reproduce the results of the DREAM Challenge, you can run MONET/test/system_test/reproduce_challenge.sh. This cannot be accomplished on commodity hardware (i.e., a regular laptop or desktop) unless a very large SWAP partition is created: in the same folder you can find a file with the exact ram usage and the challenge outputs (reproduced using MONET).

To monitor resource usage (and thus determine the amount or RAM / swap needed by your particular input network for a particular method), two simple scripts have been added to MONET/test/helper_scripts (for for Unix and one for MacOS systems): launch them before execution of MONET and redirect their output to file for simple inspection (no other task should be running).

## BENCHMARKING

For details about the modularization performance of the MONET methods on a set of artificial benchmarks (Louvain algorithm is shown as a baseline), please refer to the MONET paper in the PUBLICATIONS section; in particular, Fig. 1. MONET/test/benchmarking for a detailed output of the experiments that have been carried out.

## QUESTIONS / BUG-REPORTS

Please, address your questions and bug reports to Mattia Tomasoni, <mattia.tomasoni AT unil.ch>. An issue will be opened here to address your problem: https://github.com/BergmannLab/MONET/issues

## CONTRIBUTING

If you are interested in contributing to MONET, we encourage you to get in touch! We will be happy to add you to the list of our developers https://github.com/BergmannLab/MONET/graphs/contributors

## PUBLICATIONS

* **MONET paper**: Mattia Tomasoni, Sergio Gómez, Jake Crawford, Weijia Zhang, Sarvenaz Choobdar, Daniel Marbach and Sven Bergmann. MONET: a toolbox integrating top-performing methods for network modularisation. Preprints (2019). doi: https://doi.org/10.1101/611418

* **DREAM Challenge paper**: Sarvenaz Choobdar, Mehmet Ahsen, Jake Crawford, Mattia Tomasoni, Tao Fang, David Lamparter, Junyuan Lin, Benjamin Hescott, Xiaozhe Hu, Johnathan Mercer, Ted Natoli, Rajiv Narayan, Aravind Subramanian, Jitao David Zhang, Gustavo Stolovitzky, Zoltán Kutalik, Kasper Lage, Donna Slonim, Julio Saez-Rodriguez, Lenore Cowen, Sven Bergmann. Assessment of network module identification across complex diseases. Nature Methods 16 (2019) 843-852. doi: https://doi.org/10.1038/s41592-019-0509-5



