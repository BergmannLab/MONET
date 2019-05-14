'''
'faread.py' is a wrapper around 'faclient.py' that handles the nastiness of
the data we get back.
'''
import sys

from bpm import conf, geneinter, faclient

def functionate(genes, modulecnt):
    '''
    Sends a geneset to Funcassociate and returns its Go enrichment results.

    Handles a lot of the nastiness of parsing the return results. Namely,
    using the entity attribute table to actually get the names of genes that
    correspond to each GO enrichment.

    :param genes: A set of gene identifiers.
    :param modulecnt: The total number of modules in the BPM file. This
                      corresponds to the 'reps' (reptitions) Funcassociate
                      parameter.
    '''
    if conf.fa_species_genespace:
        genespace = None
    else:
        genespace = list(geneinter.genespace)

    c = faclient.FuncassociateClient()
    response = c.functionate(query=genes, 
                             species=conf.fa_species, 
                             namespace=conf.fa_namespace,
                             genespace=genespace,
                             reps=modulecnt,
                             cutoff=conf.fa_cutoff)

    # Lets label the info for each GO term, shall we?
    # Names ending in 'with' should be read as, for example:
    #   'Number of genes in genespace *with* this GO term annotation'
    names = ['num_with', 'num_query', 'num_genespace_with',
             'log_odds', 'unadj_p', 'adj_p', 'accession', 'goname']
    overrep = [dict(zip(names, row)) for row in response['over']]

    # Let's make a dict keyed by GO term
    goterms = {}
    for row in overrep:
        assert row['accession'] not in goterms
        goterms[row['accession']] = {
            'name': row['goname'],
            'p': float(row['adj_p']),
            'num_genespace_with': int(row['num_genespace_with']),
            'num_with': int(row['num_with']),
            'num_query': int(row['num_query']),
            'genes': set(), # see below
        }

    # Now go back and annotate the GO terms with the genes that were
    # enriched for that GO term.
    #
    # 'column_headers' are the GO terms
    # 'row_headers' are the genes
    # 'table' is a list of lists of indexes into 'column_headers' where
    #         the index of each list corresponds to an index in 'row_headers'.
    #         Thus, we have a mapping from GO term to gene :-)
    enttable = response['entity_attribute_table']
    for geneind, goinds in enumerate(enttable['table']):
        for accession in [enttable['column_headers'][i] for i in goinds]:
            try:
                gene = enttable['row_headers'][geneind]
            except IndexError:
                print >> sys.stderr, 'A gene in the Funcassociate response' \
                                     ' could not be found.'
                sys.exit(1)

            try:
                goterms[accession]['genes'].add(gene)
            except IndexError:
                print >> sys.stderr, 'A GO term in the Funcassociate response' \
                                     ' could not be found.'
                sys.exit(1)

    # This is commented out because there is a bug in Funcassociate
    # where the enrichment counts don't match the entity-attribute
    # correspondence.
    # N.B. This was actually a performance limitation that has since
    # been lifted at my request. If it comes back, this assertion
    # will have to be removed.
    for accession, goterm in goterms.iteritems():
        assert len(goterm['genes']) == goterm['num_with'], \
                '%s: %s' % (accession, str(goterm))
    
    return goterms

