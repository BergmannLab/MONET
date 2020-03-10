# MONET

This repository holds the source code for **MONET**, a Linux/MacOS command-line toolbox to mine molecular and genetic networks, leveraging the top performing methods of the **Disease Module Identification (DMI) DREAM Challenge** (see DREAM Challenge paper under section PUBLICATIONS and https://www.synapse.org/modulechallenge)

## PREREQUISITES

**Operating System**: MONET can be run on **either**
* Linux (it was tested on *Ubuntu Linux* 18.04, *CentOS Linux* 7.5)
* MacOS (it was tested on *macOS Sierra* 10.12)

**Software**: MONET requires **either**:
* ```Docker``` (see https://www.docker.com)
* ```Singularity``` (see http://singularity.lbl.gov)

**Hardware**: MONET was tested both on server and on commodity hardware (i.e., regular desktop). For details, please refer to section COMPUTATIONAL RESOURCES below.

## INSTALLATION

**Just like you can ```ls``` a folder, after installation will be able to ```monet``` a network** from any location on your system.

Simply run:

```$ git clone https://github.com/BergmannLab/MONET.git && cd MONET && ./install.sh```

A folder MONET will have been created with the source code: you are free to remove it, if you are not interested. This will not affect MONET, which has now been installed in your system: the command ```monet``` can be invoked from any location on the system.

#### IF YOU NEED SOME MORE GUIDANCE

You can follow this [survey-tutorial](https://form.jotform.com/tomasonimattia/monet-installation):
* it will guide you step by step (assumes no prior knowledge)
* (optionally) guides you through running some examples (feel free to skip those)
* it will help us collect information about possible errors on different platforms

#### IF YOU ARE ON WINDOWS

Users using Windows are encouraged to install a hypervisor (i.e., a software that allows to creates and run virtual machines): for example, install VirtualBox https://www.virtualbox.org/wiki/Downloads and configure it up to run a virtual Ubuntu Linux inside which to install MONET (using the instructions above).

#### IF YOU ARE A SINGULARITY USER WITHOUT SUDO RIGHTS

Sudo rights will be required at installation time for Singularity users: Singularity users will not need sudo rights while running MONET (i.e., Singularity does not require sudo right to run containers), but they will need it at installation time (i.e., at the time the Singularity images are first created). 

Users that don't have sudo rights should follow the regular installation procedure explained above, then refer to MONET/docs/installation_no_sudo.txt where they will find a workaround to complete the installation manually without needing sudo.

## TESTING THE INSTALLATION

At the end of the install process, you will be asked whether you want to test MONET. This test is completely automatic.

## MONET HELP COMMAND

After installing MONET, the help command ```monet --help``` will be available from any location on your system.

## RUNNING

Once installed, from any location on your system, you can run the following example command: it will run a method called M1 (see section METHODS for details), on a network contained in your /tmp folder (see section INPUT for details), using docker virtualization (see section PREREQUISITES for details). In the remainder of this document, you will find details about what parameters you can use, what to expect as an output and resource usage (in the PARAMETERS, OUTPUT and COMPUTATIONAL RESOURCES sections respectively).

```$ monet --help```

```$ monet --input=/tmp/input_network.txt —-method=M1 --container=docker```

## INPUT

The input file is provided to MONET using the ```--input``` parameter (see section RUNNING and section PARAMETERS).

The format for the input network is the following: a **tab-separated** file containing one line for each edge. 

If an edge is connecting two nodes, gene_a and gene_b, with a certain weight, the file will contain the line:

```gene_a \t gene_b \t weight \n```

Details:
* gene_a and gene_b, the gene ids, can be either *string* or *integer*
* weight can be of type *integer* or *float*
* "\t" indicates the tab character and "\n" the newline character
* no blank spaces should appear, neither as separators nor as part of the gene ids

For an example, see MONET/test/system_test/input/zachary_karate_club.txt. The same folder containing the actual inputs to the Disease Module Identification (DMI) DREAM Challenge. Beware that some of the inputs will require high amounts of computational resources and are not suited to be run on a simple laptop or desktop computer; please refer to section COMPUTATIONAL RESOURCES for details.

## OUTPUT

The output location is provided to MONET using the ```--output``` parameter (see section OPTIONAL PARAMETERS).

Two output files will be generated in the directory where you run the command. They are marked with a timestamp, the name of the selected method and the name of your input network. For example, let's assume if you run M1 on 1st January 2020 at midday on a file called input_network.txt:
* a **console-output** file, which will contain the run-time outputs generated by the method you have selected, providing details about the steps that the M1 algorithm took to generate your output. Any errors would also be redirected here. The file would be called: ```2020-01-01-120000__M1__console-output__input_network.txt```
* a **result-modules** file, containing the results of your analysis and it will not be generated in case of errors. The file would be called: ```2020-01-01-120000__M1__result-modules__input_network.txt```. It will be in tab-separated format, containing one module per line:
  * the first value of each line will be a module identifier (in the form of an integer number starting from 1)
  * the second is a fixed numerical value and can be ignored (originally used in the DREAM Challenge to provide module-level confidence scores)
  * the rest of the values on the line will be the gene ids container in the input (like gene_a and gene_b, see section INPUT)

## METHODS

Three methods are available as part of MONET, which emerged as the top-performing methods of the DREAM Challenge.

In order to run one of the three methods, adapt the example command provided in section RUNNING providing the --method option with the name of the chosen method (--method=[K1|M1|R1], for details, see section PARAMETERS).

* **K1**: KERNEL CLUSTERING OPTIMISATION algorithm. K1 is based on the “Diffusion State Distance” (DSD), a novel graph metric which is built on the premise that paths through low-degree nodes are stronger indications of functional similarity than paths that traverse high degree nodes by Cao et al. (2014). The DSD metric is used to define a pairwise distance matrix between all nodes, on which a spectral clustering algorithm is applied. In parallel, dense bipartite sub-graphs are identified using standard graph techniques. Finally, results are merged into a single set of non-overlapping clusters. For further details, please see: https://www.synapse.org/#!Synapse:syn7349492/wiki/407359
* **M1**: MODULARITY OPTIMIZATION algorithm. M1 employs an original technique named Multiresolution introduced by (Arenas et al., 2008) to explore all topological scales at which modules may be found. The novelty of this approach relies on the introduction of a parameter, called resistance, which controls the aversion of nodes to form modules. Modularity (Newman and Girvan, 2004; Arenas et al., 2007) is optimized using an ensemble of algorithms: Extremal optimization (Duch and Arenas, 2005), Spectral optimization (Newman, 2006), Fast algorithm (Newman, 2004), Tabu search (Arenas et al., 2008), and fine-tuning by iterative repositioning of individual nodes in adjacent modules. For further details, please see: https://www.synapse.org/#!Synapse:syn7352969/wiki/407384
* **R1**: RANDOM-WALK-BASED algorithm. R1 is based on a variant of Markov Cluster Algorithm known as balanced Multi-layer Regularized Markov Cluster Algorithm(bMLRMCL) (Satuluriet al., 2010) which scales well to large graphs and minimizes the number of oversized clusters. First, a pre-processing step is applied so that edges with low weights are discarded and all remaining edges are scaled to integer values. Then, bMLRMCL is applied iteratively on modules of size grater than a user-defined threshold. For further details, please see: https://www.synapse.org/#!Synapse:syn7286597/wiki/406659

## PARAMETERS

Please, provide values for the following MANDATORY parameters:
* **--input**: path to the network file to be analysed
* **--method**: method to be used to analyse the input: [K1|M1|R1]
* **--container**: virtualisation technology available on the system: [docker|singularity]

## OPTIONAL PARAMETERS

* **--output**: directory in which to output results (default is current directory)

**if you select K1** as a method, you may additionally provide the following: 

* **--nclusters**: initial number of output clusters for spectral clustering step; final number may differ (default is 100)

**if you select M1** as a method, you may additionally provide the following: 

* **--smallest**: min size of output clusters (default is 3)
* **--largest**: max size of output clusters (default is 100)
* **--linksdir**: directionality of links: [undirected|directed] (default is undirected)
* **--avgk**: desired average degree for nodes in output (default is 25)

**if you select R1** as a method, you may additionally provide the following: 

* **--smallest**: min size of output clusters (default is 3)
* **--largest**: max size of output clusters (default is 100)
* **--c**: trade-off parameter for computational efficiency; for larger c, the algorithm will run slower, but may provide more accurate results (default is 800)
* **--i**: inflation parameter for standard Markov Clustering algorithm on which R1 is based (default is 2)
* **--b**: parameter controlling how balanced the clustering results should be; for b=0, R1 behaves like standard Regularized Markov Cluster (default is 2)
* **--threshold**: remove edges smaller than threshold from the input (default is 4)
* **--post**: decide whether to recursively cluster (recluster) or discard too large output clusters: [recluster|discard] (default is discard)
* **--c2**: (only used if --post=recluster) sets --c for reclustering round (default is 500)
* **--i2**: (only used if --post=recluster) sets --i for reclustering round (default is 2)
* **--b2**: (only used if --post=recluster) sets --b for reclustering round (default is 2)

## COMPUTATIONAL RESOURCES

Some of the methods require large amount of resources, depending on your input (please, refer to the MONET paper in the PUBLICATIONS section for details about how resource needs will scale with the size of the input, for the different methods). 

To reproduce the results of the DREAM Challenge, you can run MONET/test/system_test/reproduce_challenge/reproduce_challenge.sh. This might fail on commodity hardware (i.e., a regular laptop or desktop) as about 8GB or RAM need to be available. In that case, you can allocate a larger SWAP partition (on Linux) or run the experiment on more powerful hardware, such as a server. Please browser the rest of the contents of MONET/test/system_test/reproduce_challenge to view the exact RAM usage (ram_usage.txt) and the challenge outputs produced by MONET (disease_modules_output directory).

To monitor resource usage when running on your own input (and thus determine the amount or RAM / swap needed by your particular input network for a particular method), two simple scripts have been added to MONET/test/helper_scripts (for Unix and one for MacOS systems): launch them before execution of MONET and redirect their output to file for simple inspection (no other task should be running).

## BENCHMARKING

For details about the modularization performance of the MONET methods on a set of artificial benchmarks (Louvain algorithm is shown as a baseline), please refer to the MONET paper in the PUBLICATIONS section; in particular, Fig. 1. MONET/test/benchmarking for a detailed output of the experiments that have been carried out.

## SOURCE CODE

The source code is hosted at: https://github.com/BergmannLab/MONET.git

## CONTRIBUTING

If you are interested in contributing to MONET, we encourage you to get in touch! We will be happy to add you to the list of our developers https://github.com/BergmannLab/MONET/graphs/contributors. **THANK YOU!**

**CONTRIBUTING - CREATING A BRANCH**

First, we will create an issue for the specific feature you are willing to contribute; let's say yours will happen to be issue 999. You will be then asked to create a new git branch where to implement your changes; run the following from the cloned MONET directory: 

```$ git checkout -b issues_999```

```$ git push origin issues_999```

At this point, you are free to make changes to your local code in your laptop. Don't worry if you mess things up, it's no problem to add mistakes to a branch.

**CONTRIBUTING - TESTING YOUR CHANGES**

Once you are done with your changes, you can test them locally by **reinstalling** from the modified MONET directory.

**CONTRIBUTING - PUBLISHING YOUR CHANGES**

Once you have tested your changes, run the following from the cloned MONET directory:

```$ git add .```

```$ git commit -m "adding code for feature # issues_999"```

```$ git push --set-upstream origin issues_999```

```$ git checkout master```

One of the MONET developers will test the changes in your branch then merge to Master. 

## IMPLEMENTING LOCAL CHANGES TO MONET

If you wish to implement local changes to MONET, independently from our github repository, you can simply modify the code in your local cloned repository and **reinstall** after having made those changes (i.e. run or re-run the ```install.sh``` script and confirm if you are asked to reinstall). This procedure can be repeated as many times as you like.

## TROUBLESHOOTING COMMON PROBLEMS

If a MONET run is suddenly interrupted or if the expected outputs has not been generated, here are few common problems that can occur:
* lack of RAM: if the console-output file (see section OUTPUT) contains the word "Killed", the MONET processed were stopped by the Operating System, likely due to a lack of RAM. To confirm this, please read section COMPUTATIONAL RESOURCES to learn how to monitor your resource usage while running MONET.
* outdated kernel: Singularity users that work on Linux distributions with old kernels (e.g. CentOS 6.1, kernel 2.6) will encounter trouble during the install process; they need to contact their system administrator to inquire whether a kernel upgrade is possible.
* can't implement local changes: please, refer to section IMPLEMENTING LOCAL CHANGES TO MONET.

## BUG-REPORTS

Please, address your questions and bug reports to Mattia Tomasoni, <mattia.tomasoni AT unil.ch>. An issue will be opened here to address your problem: https://github.com/BergmannLab/MONET/issues

## PUBLICATIONS

* **MONET paper**: Mattia Tomasoni, Sergio Gómez, Jake Crawford, Weijia Zhang, Sarvenaz Choobdar, Daniel Marbach and Sven Bergmann. MONET: a toolbox integrating top-performing methods for network modularisation. Preprints (2019). doi: https://doi.org/10.1101/611418

* **DREAM Challenge paper**: Sarvenaz Choobdar, Mehmet Ahsen, Jake Crawford, Mattia Tomasoni, Tao Fang, David Lamparter, Junyuan Lin, Benjamin Hescott, Xiaozhe Hu, Johnathan Mercer, Ted Natoli, Rajiv Narayan, The DREAM Module Identification Challenge Consortium, Aravind Subramanian, Jitao David Zhang, Gustavo Stolovitzky, Zoltán Kutalik, Kasper Lage, Donna Slonim, Julio Saez-Rodriguez, Lenore Cowen, Sven Bergmann, Daniel Marbach. Assessment of network module identification across complex diseases. Nature Methods 16 (2019) 843-852. doi: https://doi.org/10.1038/s41592-019-0509-5



