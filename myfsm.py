# -*- coding: utf8
from collections import defaultdict
from graphviz import Graph

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def mplot(df, labels=None):
    M = df.values.copy()
    if labels is not None:
        M = M[np.argsort(labels)]
        M = M[:, np.argsort(labels)]

    plt.matshow(M)
    plt.colorbar()
    plt.show()
    plt.close()


def compute_ptt(df, z):
    vals = df['Z_{}'.format(z)]
    names = df.index
    X = np.outer(vals.values, vals.values)
    return pd.DataFrame(X, index=names, columns=names)


def get_diff(node1, node2):
    spl1 = node1.split('/')
    spl2 = node2.split('/')
    changes = []
    for i in range(len(spl1)):
        changes.append((spl1[i], spl2[i]))
    return changes


def draw_fsm(df, z):
    df_fsm = compute_ptt(df, z)
    cols = df_fsm.columns
    rows = df_fsm.index.get_values()
    uni_prob = 1.0 / df_fsm.shape[1]
    rows_nz, cols_nz = np.nonzero(df_fsm.values)
    edges = defaultdict(float)
    for row, col in zip(rows_nz, cols_nz):
        if df_fsm.values[row, col] > uni_prob:
            diff = get_diff(rows[row], cols[col])
            for nodes in diff:
                edges[nodes[0], nodes[1]] += 1 #df_fsm.values[row, col]

    node_size = defaultdict(float)
    for c in cols:
        for name in c.split('/'):
            node_size[name] += df['Z_{}'.format(z)].loc[c]

    dg = Graph(format='pdf')
    dg.attr('node', shape='circle')
    dg.attr('node', fixedsize='true')
    dg.attr('node', width='.8')
    dg.attr('edge', style='bold', weight='3', dir='both')

    seen = set()
    nodes = set()
    for from_, to in edges:
        if (from_, to) in seen:
            continue
        seen.add((from_, to))
        seen.add((to, from_))

        if from_ not in nodes:
            if 'neither' in from_:
                dg.node(from_, label='neither')
            elif 'not_' in from_:
                dg.node(from_, label=('!' + from_[4:][:8]))
            else:
                dg.node(from_, label=from_[:8])
            nodes.add(from_)

        if to not in nodes:
            if 'neither' in to:
                dg.node(to, label='neither')
            elif 'not_' in to:
                dg.node(to, label=('!' + to[4:])[:8])
            else:
                dg.node(to, label=to[:8])
            nodes.add(to)

        dg.edge(from_, to, label=' %d' % edges[from_, to],
                penwidth=str(0.03*edges[from_, to]))
    dg.render(filename='graph_%d' % z)


if __name__ == '__main__':
    df_summary = pd.read_csv('./model/model-150-new/summarymachine.tsv.gz',
                             sep='\t')
    df_prob_tag_z = pd.read_csv('./model/model-150-new/o_by_z.tsv.gz',
                                sep='\t', index_col=0)
    labels = df_prob_tag_z.values.argmax(axis=1)
    df_tag_tag = pd.read_csv('./model/model-150-new/o_by_o.tsv.gz',
                             index_col=0, sep='\t')
    for z in range(150):
        draw_fsm(df_prob_tag_z, z)

    #df_prob_z_user = pd.read_csv('./model/model-150-new/z_by_u.tsv.gz',
    #                             index_col=0, sep='\t')
    #print(df_prob_z_user.argmax())
