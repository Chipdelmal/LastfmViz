
from sys import argv
from os import path
import numpy as np
import pandas as pd
import pickle as pkl
from datetime import date, timedelta
from graph_tool.all import *
from mpl_chord_diagram import chord_diagram
import matplotlib.pyplot as plt
from discreteMarkovChain import markovChain
from quantecon import MarkovChain
import aux as aux
import setup as stp

if aux.isnotebook():
    (TOP, WRAN, ID) = (350, 5, 'C') 
else:
    (TOP, WRAN, ID) = (int(argv[1]), int(argv[2]), argv[3])
T_THRESHOLD = timedelta(minutes=60)
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
markovMat = aux.normalizeMatrix(tMat)
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
    beta_range=(1, 30), niter=200, 
    mcmc_equilibrate_args=dict(force_niter=10),
    verbose=True
)
# pos = sfdp_layout(g)
fName = 'NSBM{}_{:03d}-{:02d}.png'
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
# fName = 'NSBM{}_{:03d}-{:02d}.pkl'
# with open(path.join(stp.IMG_PATH, fName.format(ID, TOP, WRAN)), 'wb') as handle:
#     pkl.dump(state, handle)
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

blocks = list(state.get_bs()[0])
mylist = list(zip(artsTop, blocks))
values = set(map(lambda x:x[1], mylist))
clusters = [[y[0] for y in mylist if y[1]==x] for x in values]
clusters


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
