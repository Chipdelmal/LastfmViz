
from os import path
import pandas as pd
import numpy as np
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
plt.imshow(tMat)
plt.show()