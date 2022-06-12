
from os import path
import pandas as pd
import numpy as np
from graph_tool.all import *
from mpl_chord_diagram import chord_diagram
import matplotlib.pyplot as plt
import setup as stp

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
tMat = np.zeros((artsNum, artsNum), dtype=np.int_)
###############################################################################
# Iterate Through Plays
###############################################################################
ix = 0
for ix in range(playNum-1):
    # pl0 is newer than pl1 ---------------------------------------------------
    (pl0, pl1) = [DTA_CLN.iloc[i] for i in (ix, ix+1)]
    (pa0, pa1) = [play['Artist'] for play in (pl0, pl1)]
    (px0, px1) = [arts.index(artName) for artName in (pa0, pa1)]
    tMat[px0, px1] = (tMat[px0, px1] + 1)
    print(f'Processing: {ix}/{playNum}', end='\r')
# np.sum(tMat, axis=1)
###############################################################################
# Plot
###############################################################################
# plt.imshow(tMat, vmin=0, vmax=10)
# plt.show()
sub = len(arts)
chord_diagram(
    tMat[:sub,:sub], # names=arts[:sub], 
    alpha=.65, pad=.5, gap=0.05, 
    # use_gradient=True,
    sorts='size', #'distance',
    chordwidth=.7,
    width=0.1, 
    # directed=False
    # order=[NAMES.index(i) for i in NAMES]
)
plt.savefig(
    path.join(stp.IMG_PATH, 'artChord.png'),
    dpi=500, bbox_inches='tight', facecolor='w'
)
plt.close('all')
###############################################################################
# Graph Tools
###############################################################################
g = Graph(directed=True)
g.add_edge_list(np.transpose(tMat.nonzero()))
# state = minimize_blockmodel_dl(g)
state = minimize_nested_blockmodel_dl(g)
state.draw()

pos = sfdp_layout(g)
graph_draw(g, pos, output_size=(1000, 1000))