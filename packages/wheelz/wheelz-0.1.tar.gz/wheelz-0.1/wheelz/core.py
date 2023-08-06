# -*- coding: utf-8 -*-
"""
Core logic for complexity calculation
"""
#
# standard library imports
#
import os
from collections import Counter, OrderedDict
from datetime import datetime
from itertools import chain, combinations
#
# third-party imports
#
import click
import dask.bag as db
from dask.diagnostics import ProgressBar
import numpy as np
import pandas as pd
from Bio import SeqIO
from Bio.Data import IUPACData
#
# package imports
#
from . import cli, logger
#
# global constants
#
UNITS = {'Mb':{'factor': 1,
               'outunits': 'MB'},
         'Gb':{'factor': 1024,
               'outunits': 'MB'},
         's':{'factor': 1,
              'outunits': 's'},
         'm':{'factor': 60,
              'outunits': 's'},
         'h':{'factor': 3600,
              'outunits': 's'}}
ID_SEPARATOR = '.'
FILETYPE = 'pdf'
ALPHABET = IUPACData.protein_letters 
#
# Classes
#
class ElapsedTimeReport:
    def __init__(self, name):
        self.start_time = datetime.now()
        self.name = name

    def elapsed(self, next_name):
        now = datetime.now()
        seconds = (now - self.start_time).total_seconds()
        report = '%s phase took %d seconds' %(self.name, seconds)
        self.start_time = now
        self.name = next_name
        return report


class Sanitizer(object):
    """clean up and count potential problems with sequence

       potential problems are:
          dashes:    (optional, removed if remove_dashes=True)
          alphabet:  if not in IUPAC set, changed to 'X'
    """

    def __init__(self, remove_dashes=False):
        self.remove_dashes = remove_dashes
        self.seqs_sanitized = 0
        self.chars_in = 0
        self.chars_removed = 0
        self.chars_fixed = 0
        self.endchars_removed = 0

    def char_remover(self, s, character):
        """remove positions with a given character

        :param s: mutable sequence
        :return: sequence with characters removed
        """
        removals = [i for i, j in enumerate(s) if j == character]
        self.chars_removed += len(removals)
        [s.pop(pos - k) for k, pos in enumerate(removals)]
        return s

    def fix_alphabet(self, s):
        """replace everything out of alphabet with 'X'

        :param s: mutable sequence, upper-cased
        :return: fixed sequence
        """
        fix_positions = [pos for pos, char in enumerate(s)
                         if char not in ALPHABET]
        self.chars_fixed = len(fix_positions)
        [s.__setitem__(pos, 'X') for pos in fix_positions]
        return s

    def remove_char_on_ends(self, s, character):
        """remove leading/trailing ambiguous residues

        :param s: mutable sequence
        :return: sequence with characterss removed from ends
        """
        in_len = len(s)
        while s[-1] == character:
            s.pop()
        while s[0] == character:
            s.pop(0)
        self.endchars_removed += in_len - len(s)
        return s

    def sanitize(self, s):
        """sanitize alphabet use while checking lengths

        :param s: mutable sequence
        :return: sanitized sequence
        """
        self.seqs_sanitized += 1
        self.chars_in += len(s)
        if len(s) and self.remove_dashes:
            s = self.char_remover(s, '-')
        if len(s):
            s = self.fix_alphabet(s)
        if len(s):
            s = self.remove_char_on_ends(s, 'X')
        return s


@cli.command()
@click.argument('infile')
def clusters_to_histograms(infile):
    """Compute histograms from a tab-delimited cluster file"""
    try:
        inpath, dirpath = get_paths_from_file(infile)
    except FileNotFoundError:
        logger.error('Input file "%s" does not exist!', infile)
        sys.exit(1)
    histfilepath = dirpath/(inpath.stem + '-sizedist.tsv')
    clusters = pd.read_csv(dirpath/infile, sep='\t', index_col=0)
    cluster_counter = Counter()
    for cluster_id, group in clusters.groupby(['cluster']):
        cluster_counter.update({len(group): 1})
    logger.info('writing to %s', histfilepath)
    cluster_hist = pd.DataFrame(list(cluster_counter.items()),
                                columns=['siz', 'clusts'])
    total_clusters = cluster_hist['clusts'].sum()
    cluster_hist['%clusts'] = cluster_hist['clusts'] * 100. / total_clusters
    cluster_hist['%genes'] = cluster_hist['clusts']*cluster_hist['siz'] * 100. / len(clusters)
    cluster_hist.sort_values(['siz'], inplace=True)
    cluster_hist.set_index('siz', inplace=True)
    cluster_hist.to_csv(histfilepath, sep='\t', float_format='%06.3f')


@cli.command()
@click.argument('file1')
@click.argument('file2')
def compare_clusters(file1, file2):
    """ compare one cluster file with another
    """
    path1 = Path(file1)
    path2 = Path(file2)
    commondir = Path(os.path.commonpath([path1, path2]))
    missing1 = commondir/'notin1.tsv'
    missing2 = commondir/'notin2.tsv'
    clusters1 = pd.read_csv(path1, sep='\t', index_col=0)
    print('%d members in %s'%(len(clusters1), file1))
    clusters2 = pd.read_csv(path2, sep='\t', index_col=0)
    print('%d members in %s'%(len(clusters2), file2))
    ids1 = set(clusters1['id'])
    ids2 = set(clusters2['id'])
    notin1 = pd.DataFrame(ids2.difference(ids1), columns=['id'])
    notin1.sort_values('id', inplace=True)
    notin1.to_csv(missing1, sep='\t')
    notin2 = pd.DataFrame(ids1.difference(ids2), columns=['id'])
    notin2.sort_values('id', inplace=True)
    notin2.to_csv(missing2, sep='\t')

    print('%d ids not in ids1' %len(notin1))
    print('%d ids not in ids2' %len(notin2))
    print('%d in %s after dropping'%(len(clusters1), file1))
    #print(notin2)

@cli.command()
@click.argument('setname')
@click.argument('filelist', nargs=-1)
def complexity(setname, filelist):
    """scan a set of files, producing summary statistics"""
    setpath = Path(setname)
    if len(filelist)<1:
        logger.error('Empty FILELIST, aborting')
        sys.exit(1)
    if setpath.exists() and setpath.is_file():
        setpath.unlink()
    elif setpath.exists() and setpath.is_dir():
        logger.debug('set path %s exists', setname)
    else:
        logger.info('creating output directory "%s/"', setname)
        setpath.mkdir()
    outfile = setpath/'all.faa'
    statfile = setpath/'records.tsv'
    out_sequences = []
    lengths = []
    ids = []
    files = []
    positions = []
    for file in filelist:
        position = 0
        logger.info('scanning %s', file)
        sanitizer = Sanitizer(remove_dashes=True)
        with open(file, 'rU') as handle:
            for record in SeqIO.parse(handle, SEQ_FILE_TYPE):
                seq = record.seq.upper().tomutable()
                seq = sanitizer.sanitize(seq)
                if not len(seq):
                    # zero-length string after sanitizing
                    continue
                record.seq = seq.toseq()
                ids.append(record.id)
                lengths.append(len(record))
                out_sequences.append(record)
                files.append(file)
                positions.append(position)
                position += 1
    logger.debug('writing output files')
    with outfile.open('w') as output_handle:
        SeqIO.write(out_sequences, output_handle, SEQ_FILE_TYPE)
    df = pd.DataFrame(list(zip(files, ids, positions, lengths)),
                      columns=['file', 'id', 'pos', 'len'])
    df.to_csv(statfile, sep='\t')


@cli.command()
@click.option('--first_n', default=0, show_default=True,
              help='Only process this many clusters.')
@click.option('--clust_size', default=0, show_default=True,
              help='Process only clusters of this size.')
@click.option('--parallel/--no-parallel', is_flag=True, default=True, show_default=True,
              help='Process in parallel.')
@click.option('-q', '--quiet', is_flag=True, show_default=True,
              default=False, help='Suppress logging to stderr.')
@click.argument('synfile')
@click.argument('homofile')
def combine_clusters(first_n, clust_size, synfile, homofile, quiet, parallel):
    """combine synteny and homology clusters"""
    timer = ElapsedTimeReport('reading/preparing')
    syn = pd.read_csv(synfile, sep='\t', index_col=0)
    homo = pd.read_csv(homofile, sep='\t', index_col=0)
    homo_id_dict = dict(zip(homo.id, homo.cluster))
    cluster_size_dict = dict(zip(homo.cluster, homo.siz))
    cluster_count = 0
    arg_list = []
    if first_n:
        logger.debug('processing only first %d clusters' %first_n)
    if not quiet and clust_size:
        logger.info('only clusters of size %d will be used', clust_size)
    syn['link'] = [homo_id_dict[id] for id in syn['id']]
    for cluster_id, gr in syn.groupby(['cluster']):
        cl = gr.copy() # copy, so mutable
        clsize = cl['siz'].iloc[0]
        if clust_size and (clsize != clust_size):
            continue
        if first_n and cluster_count == first_n:
           break
        arg_list.append(cl)
        cluster_count +=1
    del syn
    if parallel:
        bag = db.from_sequence(arg_list)
    else:
        cluster_list = []
    if not quiet:
        logger.info('Combining %d synteny/homology clusters:', cluster_count)
        ProgressBar().register()
    if parallel:
        cluster_list = bag.map(compute_subclusters,
                               cluster_size_dict=cluster_size_dict)
    else:
        for clust in arg_list:
            cluster_list.append(compute_subclusters(clust, cluster_size_dict))
    logger.debug(timer.elapsed('concatenating/writing clusters'))
    out_frame = pd.concat(cluster_list)
    out_frame.sort_values(['cluster', 'sub'], inplace=True)
    out_frame.index = list(range(len(out_frame)))
    for column in ['sub', 'sub_siz']:
        out_frame[column] = out_frame[column].astype(int)
    out_frame['link'] = out_frame['link'].map(lambda x: '' if pd.isnull(x) else '{:.0f}'.format(x))
    out_frame.to_csv('combined.tsv', sep='\t',
                     columns=['cluster', 'siz', 'sub', 'sub_siz',
                              'cont', 'norm', 'std', 'len', 'link', 'id'],
                     float_format='%.3f')
    logger.debug(timer.elapsed('computing stats'))
    n_fully_contained = len(set(out_frame[out_frame['cont'] == 1]['cluster']))
    logger.info('%d of %d clusters are fully contained (%.1f%%)',
                n_fully_contained, cluster_count,
                n_fully_contained * 100 / cluster_count)

