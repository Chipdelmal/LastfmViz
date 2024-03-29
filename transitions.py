
from sys import argv
from os import path
import numpy as np
import pandas as pd
from math import floor, ceil, log10
from datetime import date, timedelta
from graph_tool.all import *
from mpl_chord_diagram import chord_diagram
from discreteMarkovChain import markovChain
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
import aux as aux
import setup as stp

if aux.isnotebook():
    (TOP, WRAN, ID) = (100, 5, 'T') 
else:
    (TOP, WRAN, ID) = (int(argv[1]), int(argv[2]), argv[3])
T_THRESHOLD = timedelta(minutes=60)
(CVAR, CSCALE) = ('PSelf', 'Linear')
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
artsCount = DTA_CLN.groupby('Artist').size().sort_values(ascending=False).to_frame('Count').reset_index()
###############################################################################
# Filter Top
###############################################################################
artsTop = list(artsCount['Artist'])[:TOP]
artsTopSet = set(artsTop)
###############################################################################
# Plot Frequencies
###############################################################################
pIts = (
    ('log', 'FrequencyLog_{:03d}-{:02d}.png'),
    ('linear', 'FrequencyLin_{:03d}-{:02d}.png')
)
for (yScale, fName) in pIts:
    g = sns.catplot(
        data=artsCount[:TOP], kind="bar",
        x="Artist", y="Count", color='#6C6EE5', dodge=False,
        height=5, aspect=4, alpha=.35
    )
    g.set(yscale=yScale) 
    g.set_xticklabels(rotation=90, size=3)
    plt.savefig(
        path.join(stp.IMG_PATH, fName.format(TOP, WRAN)), 
        dpi=500, transparent=False, bbox_inches='tight'
    )
    plt.close()
###############################################################################
# Iterate Through Plays (Generate Transitions Matrix)
###############################################################################
tMat = aux.calcWeightedTransitionsMatrix(
    DTA_CLN, artsTop, windowRange=(1, WRAN), 
    timeThreshold=T_THRESHOLD, verbose=True
)
# Get diagonals for colors ----------------------------------------------------
artDegree = np.sum(tMat, axis=1)+np.sum(tMat, axis=0)
artSelfP = np.diag(aux.normalizeMatrix(tMat), k=0)
artDiag = np.diag(tMat.copy(), k=0)
# Delete self-loops and normalize ---------------------------------------------
np.fill_diagonal(tMat, 0)
pMat = aux.normalizeMatrix(tMat)
# plt.hist(artDegree)
# plt.yscale('linear')
###############################################################################
# Plot Matrices
###############################################################################
fName = 'Matrix{}_{:03d}-{:02d}.png'
plt.imshow(tMat, vmin=0, vmax=150)
plt.savefig(path.join(stp.IMG_PATH, fName.format('C', TOP, WRAN)), dpi=1000)
plt.close('all')
plt.imshow(pMat, vmin=0, vmax=.2)
plt.savefig(path.join(stp.IMG_PATH, fName.format('P', TOP, WRAN)), dpi=1000)
plt.close('all')
###############################################################################
# Chord Diagram
###############################################################################
if CVAR == 'Self':
    cVar = artDiag
elif CVAR == 'PSelf':
    cVar = artSelfP
else:
    cVar = artDegree
# Color scale -----------------------------------------------------------------
if CSCALE == 'Log':
    norm = colors.LogNorm(
        vmin=np.min(cVar), vmax=np.max(cVar)
    )
else:
    norm = colors.Normalize(
        vmin=np.min(cVar), vmax=np.max(cVar)
    )
# Colors list -----------------------------------------------------------------
cList = (
    ['#04067B', '#bdedf6'], 
    ['#ff006e', '#fdfffc', '#3a0ca3'], 
    ['#3a0ca3', '#fdfffc']
)
rvb = aux.colorPaletteFromHexList(cList[0])
# Full Plot -------------------------------------------------------------------
pColors = [rvb(norm(i)) for i in cVar]
sub = len(arts)
fName = 'Chord{}_{:03d}-{:02d}.png'
if ID == 'C':
    its = ('t', tMat, 0, range(len(artsTop)), 'turbo_r', 'C')
else:
    its = ('p', pMat, 0, range(len(artsTop)), 'turbo_r', 'T')
(nme, mat, start, order, cmap, ids) = its
chord_diagram(
    mat[:sub,:sub], 
    names=artsTop, order=order,
    alpha=.65, pad=.5, gap=0.05,
    fontcolor='k', chordwidth=.7, width=0.1, 
    rotate_names=[True]*TOP,
    extent=360, fontsize=2.25,
    colors=pColors,
    start_at=start,
    use_gradient=True
)
plt.savefig(
    path.join(stp.IMG_PATH, fName.format(ids, TOP, WRAN)),
    dpi=750, transparent=True, facecolor='w', 
    bbox_inches='tight'
)
plt.close('all')