import numpy
import pandas 
import collections
import json

sample_names = [ 'samp_{0:02d}'.format(x) for x in range(48) ]

coverage = pandas.read_table(
    '../../131004_SN1055_0174_BC2GHAACXX_targetbases_coverage',
    # 'testdata',
    names=['chr', 'start', 'end'] + sample_names + [ 'rgn_chr', 'rgn_start', 'rgn_end', 'rgn_gene', 'rgn_bases' ])

by_gene = []

done = set()

Row = collections.namedtuple('Row', [ 'gene', 'counts', 'length', 'start', 'end', 'chr' ])

for gene in coverage.rgn_gene:
    # only do each gene once, but keep them in the same order as they are in the input.
    if gene in done: continue
    done.add(gene)

    # get coverage rows for this gene
    cov_g = coverage.ix[coverage.rgn_gene == gene]

    # compute a block length for each row
    block_len = (cov_g.end - cov_g.start)

    # total gene length
    length = block_len.sum(axis = 0)

    # multiply each coverage value by block length.
    # v is now the total number of covered bases for the gene.
    # i.e.: a gene of length 10 bases, with a uniform coverage of 100 should
    #       get a value of 1000 here
    v = cov_g.ix[:,3:51].mul(block_len, axis=0).sum(axis = 0)

    by_gene.append(Row(gene, v, length, min(cov_g.start), max(cov_g.end), str(list(cov_g.chr)[0])))

genecounts = numpy.array([ x.counts for x in by_gene ], dtype=float)

# totals is the total number of covered bases per sample

totals = genecounts.sum(axis=0)

# RPKM-like normalization: coverage counts * 1e8 / library_size / gene length

gene_lengths = numpy.array([ x.length for x in by_gene ])

normalized_genecounts = (genecounts * 1e8) / totals / gene_lengths[:,numpy.newaxis]

out = {
  'chr':     [ x.chr          for x in by_gene ],
  'start':   [ int(x.start)   for x in by_gene ],
  'end':     [ int(x.end)     for x in by_gene ],
  'gene':    [ x.gene         for x in by_gene ],
  'samples': { k:list(normalized_genecounts[:,i].T) for i,k in enumerate(sample_names) }
}

print json.dumps(out)
