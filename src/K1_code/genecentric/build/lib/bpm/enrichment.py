'''
enrichment.py provides functions for gathering, reading, writing and sorting
GO enrichment information from Funcassociate.
'''
import re

from bpm import conf, faread, parallel

def enrich(modulecnt, (bpmi, modi, genes)):
    '''
    Initiates a request to Funcassociate and returns a dictionary of goterms.

    :param modulecnt: The total number of modules in the BPM file.
    :param bpmi, modi, genes: A tuple representing a module. 'bpmi' is the
                                BPM index number, 'modi' is the module index
                                number, and 'genes' is a list of gene names
                                in the module.
    :return: A four-tuple of the input module and its associated go terms.
    '''
    goterms = faread.functionate(genes, min(10000, max(1000, modulecnt)))

    parallel.inc_counter()
    parallel.print_progress()

    return bpmi, modi, genes, goterms

def sortgo(goterms):
    '''
    Sorts the keys of a goterms dictionary according to the current
    configuration.
    '''
    if conf is None:
        reverse = False
        sort_by = 'p'
    else:
        reverse = conf.order_go == 'desc'
        sort_by = conf.sort_go_by

    if sort_by == 'p':
        return sorted(goterms, key=lambda acc: goterms[acc]['p'],
                      reverse=reverse)
    elif sort_by == 'accession':
        return sorted(goterms, reverse=reverse)
    elif sort_by == 'name':
        return sorted(goterms, key=lambda acc: goterms[acc]['name'].lower(),
                      reverse=reverse)
    elif sort_by == 'num_genes_with':
        return sorted(goterms, key=lambda acc: goterms[acc]['num_with'],
                      reverse=reverse)

    assert False, 'Invalid sort by column.'

def read_bpm(bpmtext):
    '''
    Parses raw BPM text (everything between the '>' and '>') from a gobpm file,
    and turns it into a goterms dictionary keyed by GO accession.

    The fields in each dictionary entry represent the GO information returned
    by Funcassociate. Namely, a p-value, the number of genes in the module
    with the same enrichment, the number of genes in the query, the name of the 
    GO term, and finally, the names of the genes in the query with the
    corresponding GO enrichment.
    '''
    lines = map(str.strip, bpmtext.splitlines())

    bpmids = lines[0]
    m = re.search('BPM(\d+)/Module(\d+)', bpmids)
    bpmi, modi = int(m.group(1)), int(m.group(2))

    genes = set(map(str.strip, lines[1].split('\t')))

    goterms = {}
    gotermlns = lines[2:]
    for gotermln in gotermlns:
        columns = gotermln.split('\t')
        accession = columns[0].strip()
        p = columns[1].strip()
        num_with, num_query = map(int, columns[2].strip().split('/'))
        name = columns[3]

        if len(columns) == 5:
            egenes = set(columns[4].strip().split())
        else:
            egenes = set()

        assert len(egenes) == 0 or len(egenes) == num_with, columns

        goterms[accession] = {
            'p': float(p),
            'num_with': num_with,
            'num_query': num_query,
            'name': name,
            'genes': egenes,
        }

    return bpmi, modi, genes, goterms

def write_bpm(bpmi, modi, genes, goterms):
    '''
    Writes a BPM entry with GO enrichment information in gobpm file format.
    '''
    obpm = ['> BPM%d/Module%d' % (bpmi, modi)]
    obpm.append('\t'.join(genes))

    for accession in sortgo(goterms):
        goterm = goterms[accession]

        if conf is not None and conf.hide_enriched_genes:
            egenes = ''
        else:
            egenes = '\t%s' % ' '.join(goterm['genes'])

        frac = '%d/%d' % (goterm['num_with'], goterm['num_query'])
        obpm.append('%s\t%f\t%s\t%s%s'
                     % (accession, goterm['p'], frac, goterm['name'], egenes))

    return '\n'.join(obpm)

