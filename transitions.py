
from os import path
import pandas as pd
import numpy as np
from graph_tool.all import *
from mpl_chord_diagram import chord_diagram
import matplotlib.pyplot as plt
import setup as stp

TOP = 100
###############################################################################
# Read Data
###############################################################################
fNames = ('chipmaligno_cln.csv', 'chipmaligno_mbz.csv')
(DTA_CLN, DTA_MBZ) = [pd.read_csv(path.join(stp.DATA_PATH, i)) for i in fNames]
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
tMat = np.zeros((TOP, TOP), dtype=np.int_)
for ix in range(playNum-1):
    # pl0 is newer than pl1 ---------------------------------------------------
    (pl0, pl1) = [DTA_CLN.iloc[i] for i in (ix, ix+1)]
    (pa0, pa1) = [play['Artist'] for play in (pl0, pl1)]
    if (pa0 in artsTop) and (pa1 in artsTop):
        (px0, px1) = [artsTop.index(artName) for artName in (pa0, pa1)]
        tMat[px0, px1] = (tMat[px0, px1] + 1)
    print(f'Processing: {ix}/{playNum}', end='\r')
np.fill_diagonal(tMat, 0)
# np.sum(tMat, axis=1)
###############################################################################
# Plot
###############################################################################
plt.imshow(tMat, vmin=0, vmax=10)
plt.show()
# Chord -----------------------------------------------------------------------
sub = len(arts)
chord_diagram(
    tMat[:sub,:sub], names=artsTop, 
    alpha=.65, pad=.5, gap=0.05, 
    use_gradient=True,
    sorts='size', #'distance',
    chordwidth=.7,
    width=0.1, 
    rotate_names=[True]*TOP,
    fontsize=5
    # directed=False
)
plt.savefig(
    path.join(stp.IMG_PATH, 'artChord.png'),
    dpi=500, facecolor='w'
)
plt.close('all')
###############################################################################
# Graph Tools
###############################################################################
g = Graph(directed=True)
g.add_edge_list(np.transpose(tMat.nonzero()))
v_prop = g.new_vertex_property("string")
for (i, v) in enumerate(g.vertices()):
    v_prop[v] = arts[i]
# state = minimize_blockmodel_dl(g)
state = minimize_nested_blockmodel_dl(g)
state.draw(
    vertex_text=v_prop, 
    output=path.join(stp.IMG_PATH, 'NSBM.png'), 
    output_size=(2000, 2000)
)
# text
# Simple layout ---------------------------------------------------------------
pos = sfdp_layout(g)
graph_draw(g, pos, output_size=(1000, 1000))
# MCMC ------------------------------------------------------------------------
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
state.draw(vertex_shape="pie", vertex_pie_fractions=pv)