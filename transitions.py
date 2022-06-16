
from os import path
import numpy as np
import pandas as pd
from datetime import date, timedelta
from graph_tool.all import *
from mpl_chord_diagram import chord_diagram
import matplotlib.pyplot as plt
import aux as aux
import setup as stp


(TOP, T_THRESHOLD, P_THRESHOLD) = (100, timedelta(minutes=30), 200)
(yLo, yHi) = ((1950, 1), (2023, 1))
yLo = [int(i) for i in yLo]
yHi = [int(i) for i in yHi]
###############################################################################
# Read Data
###############################################################################
DTA_CLN = pd.read_csv(path.join(stp.DATA_PATH, stp.USR+'_fxd.csv'), parse_dates=[3])
DTA_MBZ = pd.read_csv(path.join(stp.DATA_PATH, stp.USR+'_mbz.csv'))
DTA_CLN = DTA_CLN.drop_duplicates()                 
msk = [
    (
        (i.date() >= date(yLo[0], yLo[1], 1)) and 
        (i.date() < date(yHi[0], yHi[1], 1))
    ) 
    if (type(i) is not float) else (False) for i in DTA_CLN['Date']
]
DTA_CLN = DTA_CLN.loc[msk]
###############################################################################
# Setup Structures
###############################################################################
arts = sorted(list(DTA_CLN['Artist'].unique()))
(artsNum, playNum) = (len(arts), DTA_CLN.shape[0])
artsCount = DTA_CLN.groupby('Artist').size().sort_values(ascending=False)
###############################################################################
# Filter Top
###############################################################################
artsTop = list(artsCount.index)[:TOP]
artsTopSet = set(artsTop)
###############################################################################
# Iterate Through Plays (Generate Transitions Matrix)
###############################################################################
ix = 0
# tMat = aux.calcWeightedTransitionsMatrix(
#     DTA_CLN, artsTop,
#     windowRange=(1, 3), timeThreshold=T_THRESHOLD, verbose=True
# )
tMat = np.zeros((TOP, TOP), dtype=np.int_)
aux.calcTransitionsMatrix(
    tMat, DTA_CLN, artsTop, 
    window=2, timeThreshold=T_THRESHOLD, verbose=True
)
# Delete self-loops and normalize ---------------------------------------------
np.fill_diagonal(tMat, 0)
pMat = tMat.copy()
row_sums = pMat.sum(axis=1)
pMat = pMat/row_sums[:, np.newaxis]
###############################################################################
# Plot
###############################################################################
plt.imshow(tMat, vmin=0, vmax=10)
plt.show()
# Chord -----------------------------------------------------------------------
sub = len(arts)
its = [
    ('p', pMat*1000, 180, range(len(artsTop)), 'turbo_r'), 
    ('t', tMat, 0, list(reversed(range(len(artsTop)))), 'turbo_r')
]
(nme, mat, start, order, cmap) = its[0]
for (nme, mat, start, order, cmap) in its:
    chord_diagram(
        mat[:sub,:sub], 
        names=artsTop, order=order,
        alpha=.65, pad=.5, gap=0.05, 
        use_gradient=True,
        sorts='size', # 'distance', 
        fontcolor='w', chordwidth=.7, width=0.1, 
        rotate_names=[True]*TOP,
        extent=180, fontsize=2.6,
        cmap=cmap, start_at=start
    )
    plt.savefig(
        path.join(stp.IMG_PATH, nme+'_artChord.png'),
        dpi=1000, transparent=True #facecolor='w'
    )
    plt.close('all')
# Chord -----------------------------------------------------------------------
sub = len(arts)
its = [
    ('t', tMat, 0, range(len(artsTop)), 'turbo_r'),
    ('p', pMat, 0, range(len(artsTop)), 'turbo_r')
]    
for (nme, mat, start, order, cmap) in its:
    chord_diagram(
        mat[:sub,:sub], 
        names=artsTop,
        order=order,
        alpha=.65, 
        pad=.5, gap=0.05, 
        use_gradient=True,
        sorts='size', # 'distance', 
        fontcolor='w',
        chordwidth=.7,
        width=0.1, 
        rotate_names=[True]*TOP,
        fontsize=2.25,
        extent=360,
        cmap=cmap,
        start_at=start
        # directed=True
    )
    plt.savefig(
        path.join(stp.IMG_PATH, nme+'_artChord_r.png'),
        dpi=1000, transparent=True #facecolor='w'
    )
    plt.close('all')
###############################################################################
# Nested Block Model
###############################################################################
mat = tMat
# Generate graph --------------------------------------------------------------
g = Graph(directed=True)
g.add_edge_list(np.transpose(mat.nonzero()))
weight = g.new_edge_property("double")
edges = list(g.edges())
for e in edges:
    weight[e] = mat[int(e.source()), int(e.target())]
# Vertices names --------------------------------------------------------------
v_prop = g.new_vertex_property("string")
for (i, v) in enumerate(g.vertices()):
    v_prop[v] = artsTop[i]
# e_prop = g.new_edge_property("string")
# e_size = g.new_edge_property("float")
# for (i, v) in enumerate(g.edges()):
#     e_prop[v] = 'none'
#     e_size = 0.1
# state = minimize_blockmodel_dl(g)
# state.draw()
state = minimize_nested_blockmodel_dl(
    g, state_args=dict(recs=[weight], rec_types=["real-exponential"])
)
mcmc_anneal(
    state, 
    beta_range=(1, 2), niter=1000, 
    mcmc_equilibrate_args=dict(force_niter=10),
    verbose=True
)
# pos = sfdp_layout(g)
state.draw(
    # pos=pos,
    vertex_text=v_prop, 
    vertex_font_size=3,
    ink_scale=1,
    edge_marker_size=0.1,
    edge_pen_width=prop_to_size(weight, 0.075, 1.5, power=1),
    # edge_marker_size=e_size,
    output=path.join(stp.IMG_PATH, 'NSBM.png'), 
    output_size=(2000, 2000)
)
levels = state.get_levels()
blocks = list(state.get_bs()[0])
# blocks = list(levels[1].get_blocks())
mylist = list(zip(artsTop, blocks))

values = set(map(lambda x:x[1], mylist))
newlist = [[y[0] for y in mylist if y[1]==x] for x in values]
newlist


state.print_summary()

# levels[3].draw(
#     # vertex_text=v_prop, 
#     # vertex_font_size=3,
#     ink_scale=1,
#     edge_marker_size=0.1,
#     # edge_pen_width=prop_to_size(weight, 0.1, 2, power=1),
#     # edge_marker_size=e_size,
#     output=path.join(stp.IMG_PATH, 'NSBM.png'), 
#     output_size=(1000, 1000)
# )
###############################################################################
# MCMC Posterior Distribution
###############################################################################
state = NestedBlockState(g)
dS, nmoves = 0, 0
for i in range(100):
    ret = state.multiflip_mcmc_sweep(niter=10)
    dS += ret[0]
    nmoves += ret[1]
    
# We will first equilibrate the Markov chain
mcmc_equilibrate(state, wait=1000, mcmc_args=dict(niter=10))

# collect nested partitions
bs = []
def collect_partitions(s):
   global bs
   bs.append(s.get_bs())
# Now we collect the marginals for exactly 100,000 sweeps
mcmc_equilibrate(state, force_niter=10000, mcmc_args=dict(niter=10),
                    callback=collect_partitions)
# Disambiguate partitions and obtain marginals
pmode = PartitionModeState(bs, nested=True, converge=True)
pv = pmode.get_marginal(g)
# Get consensus estimate
bs = pmode.get_max_nested()
state = state.copy(bs=bs)
# We can visualize the marginals as pie charts on the nodes:
state.draw(
    vertex_shape="pie",
    layout="radial",
    ink_scale=1,
    edge_pen_width=.2,
    edge_marker_size=0.1,
    vertex_pie_fractions=pv,
    output=path.join(stp.IMG_PATH, 'PRTC.png'), 
    output_size=(2000, 2000)
)
###############################################################################
# Layout Tests
###############################################################################
pos = sfdp_layout(g)
# pos = radial_tree_layout(g, g.vertex(0))
graph_draw(
    g, pos, 
    #vertex_text=v_prop, font_size=2,
    output_size=(1000, 1000)
)