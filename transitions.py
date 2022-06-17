
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
    (TOP, WRAN) = (100, 1) 
else:
    (TOP, WRAN) = argv[1:]
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
# Plot
###############################################################################
fName = 'Matrix{}_{:03d}-{}.png'
plt.imshow(tMat, vmin=0, vmax=150)
plt.savefig(path.join(stp.IMG_PATH, fName.format('C', TOP, WRAN)), dpi=1000)
plt.close('all')
plt.imshow(pMat, vmin=0, vmax=.2)
plt.savefig(path.join(stp.IMG_PATH, fName.format('P', TOP, WRAN)), dpi=1000)
plt.close('all')
# Chord -----------------------------------------------------------------------
rvb = aux.colorPaletteFromHexList(
    ['#ff006e', '#e0aaff', '#ffffff', '#caffbf', '#4361ee']
)
sub = len(arts)
its = [
    ('t', tMat, 0, range(len(artsTop)), 'turbo_r', 'C'),
    ('p', pMat, 0, range(len(artsTop)), 'turbo_r', 'T')
]
fName = 'Chord{}_{:03d}-{}.png'
for (nme, mat, start, order, cmap, ids) in its:
    chord_diagram(
        mat[:sub,:sub], 
        names=artsTop, order=order,
        alpha=.65, pad=.5, gap=0.05,
        fontcolor='w', chordwidth=.7, width=0.1, 
        rotate_names=[True]*TOP,
        extent=360, fontsize=2.25,
        cmap=cmap, 
        start_at=start,
        sorts='size', # 'distance', 
        use_gradient=True
        # directed=True
    )
    plt.savefig(
        path.join(stp.IMG_PATH, fName.format(ids, TOP, WRAN)),
        dpi=1000, transparent=False, facecolor='k'
    )
    plt.close('all')