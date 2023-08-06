import pandas as pd
import numpy as np

import pyranges as pr

import MySQLdb

from itertools import chain


def _exons(df):

    _df = df.drop(["Start", "End"], axis=1)

    cols = _df.columns.difference(['XS', 'XE'])
    exon_starts = _df['XS'].str.replace(",$", "").str.split(',')
    exon_ends = _df['XE'].str.replace(",$", "").str.split(',')

    _x = list(exon_starts)
    exon_numbers = []
    for x in _x:
        exon_numbers.extend(list(range(len(x))))

    n_repeats = exon_starts.apply(len)
    chromosomes = np.repeat(_df.Chromosome.values, n_repeats)
    gene_ids = np.repeat(_df.gene_id.values, n_repeats)
    transcript_ids = np.repeat(_df.transcript_id.values, n_repeats)
    strands = np.repeat(_df.Strand.values, n_repeats)
    transcript_name = np.repeat(_df.transcript_name.values, n_repeats)
    feature = ["exon"] * sum(n_repeats)

    exon_starts = np.array([int(i) for i in chain.from_iterable(exon_starts.tolist())], dtype=np.int32)
    exon_ends = np.array([int(i) for i in chain.from_iterable(exon_ends.tolist())], dtype=np.int32)

    exon_starts = pd.Series(exon_starts, dtype=np.int32)
    exon_ends = pd.Series(exon_ends, exon_ends, dtype=np.int32)

    exons = pd.concat([pd.Series(s).reset_index(drop=True) for s in [chromosomes, exon_starts,
                                                                     exon_ends, feature, gene_ids, strands, transcript_ids, exon_numbers, transcript_name]], axis=1)

    exons.columns = "Chromosome Start End Feature gene_id Strand transcript_id ExonNumber transcript_name".split()

    return exons


def ucsc(genome, query, host="genome-euro-mysql.soe.ucsc.edu"):

    user = "genome"
    db = genome

    conn = MySQLdb.Connection(host=host, user=user, db=db)

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def genes(genome, head=False):

    if not head:
        df = genes_df(genome)
    else:
        df = genes_df(
            genome,
            'select chrom, txStart, txEnd, exonStarts, exonEnds, name, name2, strand from refGene limit 500;'
        )

    return parse_genes(df)


def genes_df(
        genome,
        __query='select chrom, txStart, txEnd, exonStarts, exonEnds, name, name2, strand from refGene'
):

    df = ucsc(genome, __query)
    df.loc[:, "exonStarts"] = df["exonStarts"].str.decode("utf-8")
    df.loc[:, "exonEnds"] = df["exonEnds"].str.decode("utf-8")

    return df


def add_genes(df):

    grpby = df.groupby("gene_id")

    chromosome = grpby.Chromosome.first().astype("category")
    strand = grpby.Strand.first().astype("category")
    start = grpby.Start.min()
    end = grpby.End.max()
    gene_id = grpby.gene_id.first().astype("category")
    feature = pd.Series(["gene"] * len(end), index=gene_id.index, name="Feature")

    df_ = pd.concat([chromosome, start, end, strand, feature, gene_id], axis=1)

    df = pd.concat([df_, df], sort=True)

    return df


def parse_genes(df):

    df.columns = "Chromosome Start End XS XE transcript_name gene_id Strand".split(
    )

    df.insert(df.shape[1], "transcript_id", range(len(df)))

    exons = _exons(df)
    _df = (df.drop("XS XE".split(), axis=1).assign(Feature="transcript", ExonNumber=np.nan))

    col_order = "Chromosome Start End Feature gene_id transcript_id Strand ExonNumber transcript_name".split()
    _df = _df[col_order]
    exons = exons[col_order]

    df = pd.concat([_df, exons], sort=False).sort_values(
        "Chromosome Start End".split()
    )[col_order]

    df = add_genes(df)

    df = df.astype({
        "Chromosome": "category",
        "Feature": "category",
        "gene_id": "category",
        "Strand": "category",
        "transcript_name": "category",
    })

    return pr.PyRanges(df[col_order])


def chromosome_sizes(genome):

    query = 'select chrom,size from chromInfo'

    df = ucsc(genome, query)
    df.columns = ["Chromosome", "End"]
    df.insert(1, "Start", 0)

    return pr.PyRanges(df)


def genomes(host="genome-euro-mysql.soe.ucsc.edu"):

    # host = "genome-mysql.cse.ucsc.edu"
    user = "genome"

    conn = MySQLdb.Connection(host=host, user=user)

    df = pd.read_sql("show databases", conn)
    df.columns = ["Genome"]

    return df
