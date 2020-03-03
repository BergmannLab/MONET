'''
'prune.py' provides all the functions required to prune a set of BPMs after
they have been generated.
'''
from functools import partial
from itertools import combinations, product

from bpm import conf, geneinter, parallel

def prune(bpms):
    '''
    After all BPMs are generated, two different pruning mechanisms are applied.
    
    The first is pruning all BPMs that have a module less than the minimum size
    or greater than the maximum size. If either is 0, then the pruning for that
    constraint is skipped.

    The second pruning mechanism is more complex. Essentially, the interaction
    weight of each BPM is calculated (see 'interweight') and the list of BPMs
    are then sorted by that interaction weight in descending order. Starting
    from the beginning, BPMs are then added to final set of BPMs if and only if
    its Jaccard index with every BPM already in the final set is less than
    the threshold.
    '''
    if conf.min_size > 0 or conf.max_size > 0:
        bpms = filter(lambda (A, B): satisfy_min_max(A, B), bpms)

    # If pruning is disabled, exit now.
    if not conf.pruning:
        return bpms

    withI = parallel.pmap(interweight, bpms)
    withI = sorted(withI, key=lambda (iw, (A, B)): iw, reverse=True)

    pruned = []
    for iw, (A, B) in withI:
        jind = partial(jaccard_index, A.union(B))
        if all(map(lambda ji: ji < conf.jaccard,
                   [jind(S1.union(S2)) for S1, S2 in pruned])):
            pruned.append((A, B))
    
    return pruned

def interweight((A, B)):
    '''
    Calculates the interaction weight of a BPM. It is defined as the difference
    of sums of interaction scores within each module and the sum of interaction
    scores between each module divided by the number of genes in the entire BPM.

    The value returned is a BPM "decorated" with the interaction weight for
    sorting purposes. This roundabout means of decoration is used so that
    parallelism can be used for calculating the interaction weights. (As
    opposed to using a higher order function with 'sorted'.)
    '''
    # For converting a tuple to two arguments
    gitup = lambda (g1, g2): geneinter.gi(g1, g2)

    def sum_within(S):
        return sum(map(gitup, combinations(S, 2)))

    within = sum_within(A) + sum_within(B)
    between = sum(map(gitup, product(A, B)))

    iweight = (within - between) / float(len(A) + len(B))

    return (iweight, (A, B))

def jaccard_index(bpm1, bpm2):
    '''
    The Jaccard index of a BPM: the number of genes in the intersection of bpm1
    and bpm2 divided by the number of genes in the union of bpm1 and bpm2.
    
    A BPM is simply the union of its corresponding modules.
    '''
    return len(bpm1.intersection(bpm2)) / float(len(bpm1.union(bpm2)))

def constraint_min(A, B):
    '''
    Whether a BPM's modules BOTH satisfy the minimum size constraint.
    '''
    return len(A) >= conf.min_size and len(B) >= conf.min_size

def constraint_max(A, B):
    '''
    Whether a BPM's modules BOTH satisfy the maximum size constraint.
    '''
    return len(A) <= conf.max_size and len(B) <= conf.max_size

def satisfy_min_max(A, B):
    '''
    Whether a BPM's modules satisfy both the min and max size constraints.
    (Including if the constraints are disabled.)
    '''
    return ((conf.min_size == 0 or constraint_min(A, B))
            and
            (conf.max_size == 0 or constraint_max(A, B)))

