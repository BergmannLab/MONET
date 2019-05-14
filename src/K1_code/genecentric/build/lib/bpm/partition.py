'''
'partition.py' is a module that parallelizes the process of partitioning random
sets of genes. This is where most of the complexity of Genecentric is,
particularly in the 'localmaxcut' function.
'''
import random

from bpm import conf, geneinter, parallel

# See notes in 'bpms' for why this is global.
happyparts = None

def bpms():
    '''
    Generates a list of happy bipartitions in parallel and then
    generates a list of BPMs in parallel.
    '''

    # This global variable is bad in principle but seems to be required
    # for parallelism to be effective with 'group_genes'. I was currying
    # 'happyparts' with group_genes, but for whatever reason, this stopped
    # multiprocessing from keeping all of the cores hot.
    global happyparts

    happyparts = parallel.pmap(localmaxcut, xrange(0, conf.M))
    return parallel.pmap(group_genes, enumerate(geneinter.genes))

def group_genes((i, g1)):
    '''
    group_genes is applied to every gene, and a BPM is generated from *every*
    gene. In particular, given M happy bipartitions, generate a BPM where
    the first module contains all genes that appeared in the same set in the M
    bipartitions C% of the time and the second module contains all genes
    that appeared in the opposite set in the M bipartitions C% of the time.
    '''
    mod1, mod2 = [], []

    for g2 in geneinter.genes:
        # Count the number of times g2 is in the same set as g2
        freqsame = sum([1 for A, B in happyparts
                          if (g1 in A and g2 in A) or (g1 in B and g2 in B)])

        ratio = float(freqsame) / conf.M
        if ratio >= conf.C:
            mod1.append(g2)
        elif (1 - ratio) >= conf.C:
            mod2.append(g2)

    parallel.inc_counter()
    parallel.print_progress()

    return set(mod1), set(mod2)

def localmaxcut(m):
    '''
    Generates a random bipartition and makes the bipartition 'happy' by
    applying 'Weighted-Flip' (from Leiserson et al., 2011) until there are no
    unhappy genes left.
    '''
    A, B = random_bipartition()

    same_set = lambda g1, g2: (g1 in A and g2 in A) or (g1 in B and g2 in B)
    def weights(g1):
        '''
        Calculates the total neighboring weight of 'g1'. The total
        neighboring weight is a tuple of the sum of interactions in the same
        set as g1 and the sum of interactions in the opposite set as g1.

        The tuple in this case is represented by a dictionary with keys
        'same' and 'other'. I'm using a dictionary because the values need
        to be mutable; they change as we move vertices between the partitions.
        '''
        ws = { 'same': 0, 'other': 0 }
        for g2 in geneinter.genes:
            w = geneinter.gi(g1, g2)
            if same_set(g1, g2):
                ws['same'] += w
            else:
                ws['other'] += w
        return ws

    nweights = { g: weights(g) for g in geneinter.genes }
    unhappy = get_unhappy(nweights)

    while unhappy:
        v = random.choice(unhappy)

        if v in A:
            A.remove(v)
            B.add(v)
        else:
            A.add(v)
            B.remove(v)

        # This loop eliminates the need to recalculate 'weights' for every
        # gene again, which is O(n^2) in the number of genes. This loop is
        # O(n) but comes at the cost of clarity.
        #
        # The idea is to modify the weights of every other interacting gene and
        # to switch the 'same' and 'other' scores of the gene that was made
        # happy.
        for g, nw in nweights.iteritems():
            if g == v:
                nw['same'], nw['other'] = nw['other'], nw['same']
                continue

            # The interaction score between this gene and the gene that
            # was made happy.
            w = geneinter.gi(v, g) 

            # If the two genes are now in the same set, then 'g' gets a boost
            # to its happiness. Otherwise, 'g' becomes more unhappy.
            if same_set(v, g):
                nw['same'] += w
                nw['other'] -= w
            else:
                nw['same'] -= w
                nw['other'] += w

        # Refresh the unhappy list
        unhappy = get_unhappy(nweights)

    parallel.inc_counter()
    parallel.print_progress()

    return A, B

def get_unhappy(nweights):
    '''
    Returns all of the genes that are unhappy given a dictionary of
    gene ids mapped to its total neighboring weights.
    '''
    return [ g for (g, _) in filter(lambda (g, w): w['same'] < w['other'], 
                                    nweights.items()) ]

def random_bipartition():
    '''
    Creates two random sets of genes from the genetic interaction data.
    '''
    A, B = set(), set()
    for g in geneinter.genes:
        if random.random() < 0.5:
            A.add(g)
        else:
            B.add(g)

    return A, B

