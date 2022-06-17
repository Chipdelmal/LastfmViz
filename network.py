
from sys import argv
from os import path
import numpy as np
import pandas as pd
from datetime import date, timedelta
from graph_tool.all import *
from mpl_chord_diagram import chord_diagram
import matplotlib.pyplot as plt
import aux as aux
import setup as stp

if aux.isnotebook():
    (TOP, WRAN, ID) = (100, 1, 'C') 
else:
    (TOP, WRAN, ID) = argv[1:]
T_THRESHOLD = timedelta(minutes=30)
###############################################################################
# Read Data
###############################################################################
DTA_CLN = pd.read_csv(path.join(stp.DATA_PATH, stp.USR+'_fxd.csv'), parse_dates=[3])
DTA_MBZ = pd.read_csv(path.join(stp.DATA_PATH, stp.USR+'_mbz.csv'))          
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
tMat = aux.calcWeightedTransitionsMatrix(
    DTA_CLN, artsTop, windowRange=(1, WRAN), 
    timeThreshold=T_THRESHOLD, verbose=True
)
# Delete self-loops and normalize ---------------------------------------------
np.fill_diagonal(tMat, 0)
pMat = aux.normalizeMatrix(tMat)
###############################################################################
# Nested Block Model
###############################################################################
if ID == 'C':
    mat = tMat
else:
    mat = pMat
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
# Nested SBM ------------------------------------------------------------------
state = minimize_nested_blockmodel_dl(
    g, state_args=dict(recs=[weight], rec_types=["real-exponential"])
)
mcmc_anneal(
    state, 
    beta_range=(1, 5), niter=750, 
    mcmc_equilibrate_args=dict(force_niter=10),
    verbose=True
)
# pos = sfdp_layout(g)
fName = 'NSBM{}_{:03d}-{}.png'
state.draw(
    # pos=pos,
    # vertex_text=v_prop, 
    vertex_font_size=3,
    ink_scale=1,
    edge_marker_size=0.1,
    edge_pen_width=prop_to_size(weight, 0.075, 1.5, power=1),
    # edge_marker_size=e_size,
    output=path.join(stp.IMG_PATH, fName.format(ID, TOP, WRAN)),
    output_size=(2000, 2000),
    bg_color='#000000'
)
###############################################################################
# MCMC Posterior Distribution
###############################################################################
state = NestedBlockState(
    g, state_args=dict(recs=[weight], rec_types=["real-exponential"])
)
dS, nmoves = 0, 0
for i in range(100):
    ret = state.multiflip_mcmc_sweep(niter=10)
    dS += ret[0]
    nmoves += ret[1]
mcmc_equilibrate(state, wait=1000, mcmc_args=dict(niter=10))
bs = []
def collect_partitions(s):
   global bs
   bs.append(s.get_bs())
mcmc_equilibrate(
    state, force_niter=10000, mcmc_args=dict(niter=10),
    callback=collect_partitions
)
pmode = PartitionModeState(bs, nested=True, converge=True)
pv = pmode.get_marginal(g)
# Get consensus estimate
bs = pmode.get_max_nested()
state = state.copy(bs=bs)
# We can visualize the marginals as pie charts on the nodes:
fName = 'PRTC{}_{:03d}-{}.png'
state.draw(
    vertex_shape="pie",
    layout="radial",
    ink_scale=1,
    edge_color=weight,
    edge_pen_width=prop_to_size(weight, .05, 2, power=1, log=False),
    edge_marker_size=0.1,
    vertex_pie_fractions=pv,
    output=path.join(stp.IMG_PATH, fName.format(ID, TOP, WRAN)), 
    output_size=(2000, 2000),
    bg_color='#000000'
)
###############################################################################
# Layout Tests and Scrap
###############################################################################
# pos = sfdp_layout(g)
# pos = radial_tree_layout(g, g.vertex(0))
# graph_draw(
#     g, pos, 
#     #vertex_text=v_prop, font_size=2,
#     output_size=(1000, 1000)
# )
#
# levels = state.get_levels()
# blocks = list(state.get_bs()[0])
# # blocks = list(levels[1].get_blocks())
# mylist = list(zip(artsTop, blocks))
# values = set(map(lambda x:x[1], mylist))
# newlist = [[y[0] for y in mylist if y[1]==x] for x in values]
# newlist
# state.print_summary()
# # levels[3].draw(
# #     # vertex_text=v_prop, 
# #     # vertex_font_size=3,
# #     ink_scale=1,
# #     edge_marker_size=0.1,
# #     # edge_pen_width=prop_to_size(weight, 0.1, 2, power=1),
# #     # edge_marker_size=e_size,
# #     output=path.join(stp.IMG_PATH, 'NSBM.png'), 
# #     output_size=(1000, 1000)
# # )