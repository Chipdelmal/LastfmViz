
from sys import argv
from os import path
import numpy as np
import pandas as pd
from math import floor, ceil, log10
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from mpl_chord_diagram import chord_diagram
import matplotlib.pyplot as plt
from matplotlib import colors
import matplotlib
import aux as aux
import setup as stp
import warnings
warnings.filterwarnings("ignore")

if aux.isnotebook():
    (TOP, WRAN, ID) = (50, 5, 'C') 
else:
    (TOP, WRAN, ID) = (int(argv[1]), int(argv[2]), argv[3])
T_THRESHOLD = timedelta(minutes=60)
(CVAR, CSCALE) = ('PSelf', 'Linear')
(dteLo, dteHi) = (date(2012, 1, 1), date(2023, 1, 1))
cList = (
    ['#04067B', '#bdedf6'], 
    ['#ff006e', '#fdfffc', '#3a0ca3'], 
    ['#3a0ca3', '#fdfffc']
)
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
# Iterate through months
###############################################################################
dteMax = max(DTA_CLN['Date'])
months = ceil((date(dteMax.year, dteMax.month, 1) - dteLo).days/30)
m=10
for m in range(10, months):
    print('Iter: {:04d}/{:04d}'.format(m+1, months))
    msk = [((i.date() >= dteLo) and (i.date() <= dteLo+relativedelta(months=m))) 
        if (type(i) is not float) else (False) for i in DTA_CLN['Date']
    ]
    data = DTA_CLN.loc[msk]
    ###############################################################################
    # Iterate Through Plays (Generate Transitions Matrix)
    ###############################################################################
    tMat = aux.calcWeightedTransitionsMatrix(
        data, artsTop, windowRange=(1, WRAN), 
        timeThreshold=T_THRESHOLD, verbose=True
    )
    # Get diagonals for colors ----------------------------------------------------
    artDegree = np.sum(tMat, axis=1)+np.sum(tMat, axis=0)
    artSelfP = np.nan_to_num(np.diag(aux.normalizeMatrix(tMat), k=0))
    artDiag = np.diag(tMat.copy(), k=0)
    # Delete self-loops and normalize ---------------------------------------------
    np.fill_diagonal(tMat, 0)
    pMat = aux.normalizeMatrix(tMat)
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
        norm = colors.Normalize(vmin=0, vmax=.75)
    # Colors list -----------------------------------------------------------------
    rvb = aux.colorPaletteFromHexList(cList[0])
    # Full Plot -------------------------------------------------------------------
    pColors = [rvb(norm(i)) for i in cVar]
    sub = len(arts)
    fName = 'Chord{}_{:03d}-{:02d}_{:05d}.png'
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
        path.join(stp.VID_PATH, fName.format(ids, TOP, WRAN, m)),
        dpi=350, transparent=True, facecolor='w', 
        bbox_inches='tight'
    )
    plt.close('all')