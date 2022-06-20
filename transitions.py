
from sys import argv
from os import path
import numpy as np
import pandas as pd
from math import floor, ceil, log10
from datetime import date, timedelta
from graph_tool.all import *
from mpl_chord_diagram import chord_diagram
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns
import aux as aux
import setup as stp

if aux.isnotebook():
    (TOP, WRAN, ID) = (400, 5, 'C') 
else:
    (TOP, WRAN, ID) = (int(argv[1]), int(argv[2]), argv[3])
T_THRESHOLD = timedelta(minutes=60)
CSCALE = 'Log'
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
# Plot Frequency --------------------------------------------------------------
fName = 'FrequencyLin_{:03d}-{:02d}.png'
g = sns.catplot(
    data=artsCount[:TOP], kind="bar",
    x="Artist", y="Count", color='#3a0ca355', dodge=False,
    height=5, aspect=4, alpha=.65, # palette="tab20"
)
g.set_xticklabels(rotation=90, size=3)
plt.savefig(
    path.join(stp.IMG_PATH, fName.format(TOP, WRAN)), 
    dpi=500, transparent=False, bbox_inches='tight'
)
plt.close()
# Plot Log-Frequency ----------------------------------------------------------
fName = 'FrequencyLog_{:03d}-{:02d}.png'
g = sns.catplot(
    data=artsCount[:TOP], kind="bar",
    x="Artist", y="Count", color='#3a0ca355', dodge=False,
    height=5, aspect=4, alpha=.65,# palette="tab20"
)
# g.set_xlabel("", fontsize=0)
# g.set_ylabel("Play Count", fontsize=20)
g.set(yscale="log") 
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
# Delete self-loops and normalize ---------------------------------------------
artDegree = np.sum(tMat, axis=1)+np.sum(tMat, axis=0)
np.fill_diagonal(tMat, 0)
pMat = aux.normalizeMatrix(tMat)
###############################################################################
# Plot Matrix
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
if CSCALE == 'Log':
    norm = colors.LogNorm(
        vmin=floor(np.min(artDegree)), vmax=ceil(np.max(artDegree)/1.25)
    )
else:
    norm = colors.Normalize(
        vmin=floor(np.min(artDegree)), vmax=ceil(np.max(artDegree)/1.5)
    )
cList = (
    ['#04067B', '#cddafd'], 
    ['#ff006e', '#fdfffc', '#3a0ca3'], 
    ['#3a0ca3', '#fdfffc']
)
rvb = aux.colorPaletteFromHexList(cList[0])
# Full Plot -------------------------------------------------------------------
cList = [rvb(norm(i)) for i in artDegree]
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
    fontcolor='w', chordwidth=.7, width=0.1, 
    rotate_names=[True]*TOP,
    extent=360, fontsize=2.25,
    colors=cList,
    # cmap="tab20b", #cmap, 
    start_at=start,
    sorts='size', # 'distance', 
    use_gradient=True
    # directed=True
)
plt.savefig(
    path.join(stp.IMG_PATH, fName.format(ids, TOP, WRAN)),
    dpi=500, transparent=True, # facecolor='k', 
    bbox_inches='tight'
)
plt.close('all')