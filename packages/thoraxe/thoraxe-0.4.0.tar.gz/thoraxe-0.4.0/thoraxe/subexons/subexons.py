"""Functions to create the subexon table."""

import collections

import pandas as pd

from thoraxe import transcript_info
from thoraxe.transcript_info import phases

# A basic interval type, containing start and end coordinates and the set of
# components that are included on it.
Interval = collections.namedtuple('Interval', ['start', 'end', 'components'])


def _check_disjoint_intervals_inputs(starts, ends, ids):
    """Check the inputs of disjoint_intervals."""
    assert len(starts) == len(ends) == len(ids), 'starts, ends and ids '\
        'should have the same length.'
    assert all(starts[i] <= starts[i + 1] for i in range(len(starts) - 1)),\
        'starts should be sorted.'


def disjoint_intervals(starts, ends, ids):
    """
    Return list of disjoint intervals.

    Produce the set of disjoint intervals from a list of start and end
    positions (same chr) and optionally ids.
    Empty intervals are reported as well.
    !!! The intervals need to be sorted by start and end position before
    calling the function and the coordinates should be inclusive.

    >>> disjoint_intervals([1,10,20,40], [9,30,30,50], [0,1,2,3])
    [Interval(start=1, end=9, components={0}), \
Interval(start=10, end=19, components={1}), \
Interval(start=20, end=30, components={1, 2}), \
Interval(start=31, end=39, components=set()), \
Interval(start=40, end=50, components={3})]
    >>> disjoint_intervals([1,1], [9,7], [0,1])
    [Interval(start=1, end=7, components={0, 1}), \
Interval(start=8, end=9, components={0})]
    >>> disjoint_intervals([1,3], [7,9], [0,1])
    [Interval(start=1, end=2, components={0}), \
Interval(start=3, end=7, components={0, 1}), \
Interval(start=8, end=9, components={1})]
    >>> disjoint_intervals([3,1], [9,7], [0,1])
    Traceback (most recent call last):
        ...
    AssertionError: starts should be sorted.
    >>> disjoint_intervals([3,1], [9,7,10], [0,1])
    Traceback (most recent call last):
        ...
    AssertionError: starts, ends and ids should have the same length.
    """
    _check_disjoint_intervals_inputs(starts, ends, ids)
    d_j = {}
    for i, start in enumerate(starts):
        d_j.setdefault(start, []).append((1, ids[i]))
    for i, end in enumerate(ends):
        # The end occurs after the end position,
        # explains also the BED style coding
        d_j.setdefault(end + 1, []).append((-1, ids[i]))
    j_pos = sorted(d_j.keys())
    interval_reduce = []
    # The list of open intervals from the last turn
    last = set([])
    for left, right in zip(j_pos[:-1], j_pos[1:]):
        cint = Interval(left, right - 1, set(last))
        cint.components.update([x[1] for x in d_j[left] if x[0] == 1])
        cint.components.symmetric_difference_update(
            [x[1] for x in d_j[left] if x[0] == -1])
        interval_reduce.append(cint)
        last = cint.components
    # Need to decide of the format.
    return interval_reduce


def _get_subexon_seq(exon_row, interval):
    """Return the interval sequence of the subexon."""
    seq = exon_row['ExonSequence']
    if exon_row['Strand'] == 1:
        exon_start = exon_row['ExonRegionStart']
        interval_start = interval.start - exon_start
        # Because interval.end includes the last base (close interval)
        # and Python indexing doesn't include the last value, +1 is needed:
        interval_end = interval.end - exon_start + 1
    else:
        exon_start = exon_row['ExonRegionEnd']
        interval_start = exon_start - interval.end
        interval_end = exon_start - interval.start + 1

    assert interval_start < interval_end, 'Interval end should not be '\
        'lower than its start'

    return seq[interval_start:interval_end]


def _subexon_ranks(strand, transcript_len):
    """
    Return a list of the subexon ranks.

    NOTE: Rank starts in 0 to make this compatible with
    end_phase_previous_exon that expect exon_pos(ition) to start in 0.

    >>> _subexon_ranks(-1, 10)
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    >>> _subexon_ranks(1, 10)
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    """
    if strand == -1:
        return list(range(transcript_len - 1, -1, -1))

    return list(range(0, transcript_len))


def _sort_subexons_coordinates(subexon_df):
    """Sort subexons and return the DataFrame."""
    transcript_data_frames = []

    id_columns = ['GeneID', 'TranscriptID']
    for _, transcript_df in subexon_df.groupby(id_columns):
        transcript_data_frames.append(
            transcript_df.sort_values(by='GenomicCodingStart', ascending=True))

    return pd.concat(transcript_data_frames)


def _add_subexon_rank(subexon_df):
    """
    Sort subexon_df and add a column with the subexon rank in the transcript.

    It returns the modified pandas' DataFrame.
    """
    subexon_df = _sort_subexons_coordinates(subexon_df)

    ranks = []
    id_columns = ['GeneID', 'TranscriptID']
    for _, transcript_df in subexon_df.groupby(id_columns):
        strand = transcript_df.loc[transcript_df.index[0], 'Strand']
        transcript_len = len(transcript_df)
        ranks.extend(_subexon_ranks(strand, transcript_len))

    subexon_df['SubexonRank'] = ranks

    return subexon_df


def _get_info_from_row(row, columns):
    """Return a dict with from column to value."""
    return {col: getattr(row, col) for col in columns}


def _subexon_info(  # pylint: disable=too-many-locals
        gene_df, exon_df, intervals):
    """Return a pandas' DataFrame for subexons."""
    # We are going to use transcript_info functions to transcribe and
    # merge subexons. Therefore, we are going to use the exon table column
    # names at the beginning, and then we are going to change these column
    # names by the columns_to_rename values before returning subexon_df:
    columns_to_rename = {
        'SubexonID': 'SubexonID',
        'ExonSequence': 'SubexonSequence',
        'GenomicCodingStart': 'SubexonCodingStart',
        'GenomicCodingEnd': 'SubexonCodingEnd',
        'IntervalNumber': 'IntervalNumber'
    }

    columns_to_keep = [
        # Transcript information
        'GeneID',
        'TranscriptID',
        'ProteinID',
        'Strand',
        'ExonRank',
        'TranscriptIDCluster',
        # 'ExonID' is kept to merge the exon and subexon tables later
        'ExonID',
        'ExonIDCluster',
        'Cluster',
        'QueryExon',
        'TargetCoverage',
        'PercentIdentity',
        'AlignedQuery',
        'AlignedTarget'
    ]

    # cDNA_CodingStart and end are only needed for _get_exon_cds
    column_to_delete = ['cDNA_CodingStart', 'cDNA_CodingEnd']

    subexon_dict = {
        key: []
        for key in list(columns_to_rename.keys()) + columns_to_keep +
        column_to_delete
    }

    for interval_number, interval in enumerate(intervals):
        for exon_id in interval.components:
            exon_row = exon_df.loc[exon_id]
            seq = _get_subexon_seq(exon_row, interval)
            subexon_info = {
                'SubexonID': exon_id + '_SE_' + str(interval_number),
                'IntervalNumber': interval_number,
                'ExonID': exon_id,
                'Cluster': exon_row['Cluster'],

                # CDS sequence of the subexon:
                'ExonSequence': seq,

                # cDNA_CodingStart and end have dummy values to make
                # _get_exon_cds to return the input sequence without
                # modifications:
                'cDNA_CodingStart': 0,
                'cDNA_CodingEnd': len(seq) - 1
            }
            if exon_row['Strand'] == 1:
                subexon_info.update({
                    'GenomicCodingStart': interval.start,
                    'GenomicCodingEnd': interval.end
                })
            else:
                subexon_info.update({
                    'GenomicCodingStart': interval.end,
                    'GenomicCodingEnd': interval.start
                })
            for row in gene_df[gene_df['ExonID'] == exon_id].itertuples():
                transcript_row_info = _get_info_from_row(row, columns_to_keep)
                transcript_row_info.update(subexon_info)
                for key, value in transcript_row_info.items():
                    subexon_dict[key].append(value)

    subexon_df = pd.DataFrame.from_dict(subexon_dict)
    subexon_df = _add_subexon_rank(subexon_df)
    subexon_df = subexon_df.sort_values(
        by=['GeneID', 'TranscriptID', 'SubexonRank'])

    _add_phases(subexon_df,
                rank_column='SubexonRank',
                seq_column='ExonSequence')

    transcript_info.add_protein_seq(subexon_df,
                                    seq_column="SubexonProteinSequence")

    transcript_info.merge_identical_exons(subexon_df,
                                          exon_id_column='SubexonID',
                                          seq_column="SubexonProteinSequence")

    subexon_df.drop(columns=column_to_delete, inplace=True)
    subexon_df.rename(columns=columns_to_rename, inplace=True)

    return subexon_df


def _add_phases(subexon_df,
                rank_column='SubexonRank',
                seq_column='SubexonSequence'):
    """
    Add columns with start and end phases.

    This function need to be run after _add_subexon_rank is used to
    assign rank to the subexons in the transcript.

    subexon_df needs to be sorted by subexon rank.
    """
    subexon_df['StartPhase'] = -99
    subexon_df['EndPhase'] = -99

    n_rows = len(subexon_df)
    row_number = 0
    while row_number < n_rows:
        row_index = subexon_df.index[row_number]
        row = subexon_df.loc[row_index, :]
        cdna_len = len(row[seq_column])

        if row_number == 0:
            previous_end_phase = 0
        else:
            subexon_rank = row[rank_column]
            previous_end_phase = phases.end_phase_previous_exon(
                subexon_df, subexon_rank, subexon_df.index[row_number - 1])

        start_phase, end_phase = phases.calculate_phase(
            cdna_len, previous_end_phase)

        subexon_df.at[row_index, 'StartPhase'] = start_phase
        subexon_df.at[row_index, 'EndPhase'] = end_phase

        row_number += 1


def _add_transcript_fraction(subexon_df):
    """
    Add the fraction of the transcripts in which the subexon is present.

    1.0 for constitutive exons, < 1.0 for alternative exons
    """
    subexon_counts = subexon_df.groupby(
        ['GeneID',
         'SubexonID']).size().to_frame('TranscriptsWithSubexon').reset_index()

    transcript_counts = subexon_df.loc[:, [
        'GeneID', 'TranscriptID'
    ]].drop_duplicates().groupby(
        ['GeneID']).size().to_frame('TranscriptsInGene').reset_index()

    counts = pd.merge(subexon_counts,
                      transcript_counts,
                      how='inner',
                      on='GeneID')

    counts['TranscriptFraction'] = (
        counts['TranscriptsWithSubexon'] /
        counts['TranscriptsInGene'].astype('float64'))

    return pd.merge(subexon_df,
                    counts,
                    how='inner',
                    on=['GeneID', 'SubexonID'])


def _find_exon(subexon_table, subexon_id_cluster):
    """Return a list with the 'ExonID's of a particular subexon."""
    return subexon_table.loc[subexon_table['SubexonIDCluster'] ==
                             subexon_id_cluster, 'ExonID'].unique().tolist()


def _update_to_merge_list(to_merge, subexon_1, subexon_2):
    """
    Add subexon_1 and subexon_2 to the to_merge list.

    >>> _update_to_merge_list([], 1, 2)
    [{1, 2}]
    >>> _update_to_merge_list([{1, 2}], 2, 3)
    [{1, 2, 3}]
    >>> _update_to_merge_list([{1, 2}], 8, 9)
    [{1, 2}, {8, 9}]
    """
    group = {subexon_1, subexon_2}

    for existing_group in to_merge:
        if existing_group.intersection(group):
            existing_group.update(group)
            return to_merge

    to_merge.append(group)
    return to_merge


def _fill_subexons_to_merge(subexons_to_merge, subexons, exon_table):
    """
    Take the exon information to find subexons to merge.

    The subexons to merge are appended to subexons_to_merge and deleted from
    the subexons list. This function returns 0 if there are exons to merge,
    otherwise it returns 1.
    """
    exon_table.sort_values(by='SubexonRank', inplace=True, ascending=True)
    row_list = exon_table.to_dict('records')
    nrows = len(row_list)
    to_merge = []
    for row_index in range(1, nrows):
        previous_row = row_list[row_index - 1]
        actual_row = row_list[row_index]
        if (previous_row['SubexonIDCluster'] in subexons) and (
                actual_row['SubexonIDCluster'] in subexons) and (
                    previous_row['TranscriptFraction'] ==
                    actual_row['TranscriptFraction']):
            to_merge = _update_to_merge_list(to_merge,
                                             previous_row['SubexonIDCluster'],
                                             actual_row['SubexonIDCluster'])
    if to_merge:
        for group in to_merge:
            for subexon in group:
                subexons.remove(subexon)
        subexons_to_merge.append(to_merge)
        return 0

    return 1


def _find_subexons_to_merge(subexon_table, delim='/'):
    """Find non redundant and contiguous subexons."""
    subexons_to_merge = []
    subexons = [
        subexon for subexon in subexon_table['SubexonIDCluster'].unique()
        if delim not in subexon  # non-redundant subexons
    ]
    subexon_index = 0
    while subexon_index < len(subexons):
        subexon = subexons[subexon_index]
        exons = _find_exon(subexon_table, subexon)
        if len(exons) == 1:
            exon = exons[0]
            exon_table = subexon_table[subexon_table['ExonID'] == exon]
            exon_table = exon_table.drop_duplicates(
                'SubexonIDCluster')  # keep the first transcript
            if exon_table.shape[0] > 1:
                subexon_index += _fill_subexons_to_merge(
                    subexons_to_merge, subexons, exon_table)
                continue
        else:
            raise Exception(
                'Non-redundant subexon is present in more than one exon.')
        subexon_index += 1
    return subexons_to_merge


def _fill_with_new_subexon_data(old2new, rowi, rowj):
    """Fill a dict from old subexon ID to a dict with the new values."""
    if rowi['Strand'] == 1:
        doit = (rowj['SubexonCodingStart'] - rowi['SubexonCodingEnd'] == 1)
    else:
        doit = (rowi['SubexonCodingEnd'] - rowj['SubexonCodingStart'] == 1)

    if doit:
        keys = [
            'SubexonID', 'SubexonIDCluster', 'SubexonCodingStart',
            'SubexonCodingEnd', 'StartPhase', 'EndPhase', 'SubexonSequence',
            'SubexonProteinSequence', 'IntervalNumber', 'SubexonRank'
        ]
        rowi_subexon = rowi['SubexonIDCluster']
        rowj_subexon = rowj['SubexonIDCluster']
        previous = old2new.setdefault(rowi_subexon, rowi[keys].to_dict())
        actual = old2new.setdefault(rowj_subexon, rowj[keys].to_dict())
        if rowi['Strand'] == 1:
            previous['SubexonCodingEnd'] = actual['SubexonCodingEnd']
            actual['SubexonCodingStart'] = previous['SubexonCodingStart']
        else:
            actual['SubexonCodingStart'] = previous['SubexonCodingStart']
            previous['SubexonCodingEnd'] = actual['SubexonCodingEnd']
        previous['EndPhase'] = actual['EndPhase']
        actual['StartPhase'] = previous['StartPhase']
        merged_protein = previous['SubexonProteinSequence'] + actual[
            'SubexonProteinSequence']
        previous['SubexonProteinSequence'] = merged_protein
        actual['SubexonProteinSequence'] = merged_protein
        merged_dna_seq = previous['SubexonSequence'] + actual['SubexonSequence']
        previous['SubexonSequence'] = merged_dna_seq
        actual['SubexonSequence'] = merged_dna_seq
        subexon_id = rowi_subexon + '_' + rowj_subexon.split('_')[-1]
        actual['SubexonID'] = subexon_id
        previous['SubexonID'] = subexon_id
        actual['SubexonIDCluster'] = subexon_id
        previous['SubexonIDCluster'] = subexon_id
        previous['IntervalNumber'] = actual['IntervalNumber']
        previous['SubexonRank'] = actual['SubexonRank']


def _merge_subexons(subexon_table, subexons_to_merge):
    """Merge subexons in the subexon_table."""
    for groups in subexons_to_merge:
        for subexon_group in groups:
            n_subexons = len(subexon_group)
            group_index = subexon_table.index[
                subexon_table['SubexonIDCluster'].isin(subexon_group)]
            group_mask = subexon_table.index.isin(group_index)
            transcript = subexon_table[group_mask].drop_duplicates(
                'SubexonIDCluster')  # keep the first transcript
            transcript.sort_values(by='SubexonRank',
                                   inplace=True,
                                   ascending=True)
            assert len(transcript) == n_subexons

            old2new = {}
            for index in range(1, n_subexons):
                previous_row = transcript.iloc[index - 1, :]
                actual_row = transcript.iloc[index, :]
                _fill_with_new_subexon_data(old2new, previous_row, actual_row)

            for index in group_index:
                subexon_id = subexon_table.loc[index, 'SubexonIDCluster']
                for key, value in old2new[subexon_id].items():
                    subexon_table.loc[index, key] = value

            subexon_table.drop_duplicates(subset=[
                'GeneID', 'TranscriptID', 'TranscriptIDCluster', 'ExonID',
                'ExonIDCluster', 'SubexonID', 'SubexonIDCluster'
            ],
                                          inplace=True)


def create_subexon_table(transcript_data, merge_non_redundant=True):
    """
    Return a subexon table.

    If merge_non_redundant is True (default), contiguous subexons that
    appear together in only one exon are merged/joint. This happens
    because subexons are defined using coordinates at the genomic level
    to reduce redundancy.
    However, some subexons does not have the same protein sequence because
    of different reading frames/phases, giving non-redundant subexons at
    the protein level.
    """
    subexon_data_frames = []
    for _, gene_df in transcript_data.groupby('GeneID'):

        # We need the genomic coding coordinates and the sequence of each exon
        exon_df = gene_df.drop_duplicates(subset='ExonID')
        exon_df.set_index('ExonID', inplace=True)
        exon_df = exon_df.sort_values(
            by=['GenomicCodingStart', 'GenomicCodingEnd'])

        intervals = disjoint_intervals(list(exon_df['GenomicCodingStart']),
                                       list(exon_df['GenomicCodingEnd']),
                                       list(exon_df.index))

        intervals = [
            interval for interval in intervals if len(interval.components) > 0
        ]

        intervals = sorted(intervals, key=lambda interval: interval.start)

        subexon_df = _subexon_info(gene_df, exon_df, intervals)
        subexon_data_frames.append(subexon_df)

    subexon_table = pd.concat(subexon_data_frames)
    subexon_table = _add_transcript_fraction(subexon_table)

    if merge_non_redundant:
        subexons_to_merge = _find_subexons_to_merge(subexon_table)
        _merge_subexons(subexon_table, subexons_to_merge)

    return subexon_table
