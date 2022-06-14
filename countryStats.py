import math
from sys import argv
import datetime
import squarify
import aux as aux
import setup as stp
import numpy as np
import pandas as pd
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.transforms import Affine2D
import matplotlib as mpl
import matplotlib.cm
import random
from pywaffle import Waffle
from matplotlib.pyplot import figure, show, rc
mpl.rcParams['axes.linewidth'] = 1

(yLo, yHi) = ((2012, 1), (2022, 1))
yLo = [int(i) for i in yLo]
yHi = [int(i) for i in yHi]
##############################################################################
# Aesthetics parameters
##############################################################################
(WIDTH, HEIGHT, RESOLUTION) = (3840, 2160, 500)
##############################################################################
# Read artists file
##############################################################################
dataF = pd.read_csv(stp.DATA_PATH+stp.USR+'_cln.csv', parse_dates=[3])
data = dataF.drop_duplicates()
msk = [
    (
        (i.date() >= datetime.date(yLo[0], yLo[1], 1)) and 
        (i.date() < datetime.date(yHi[0], yHi[1], 1))
    ) 
    if (type(i) is not float) else (False) for i in data['Date']
]
# Read Geo File --------------------------------------------------------------
dataG = pd.read_csv(stp.DATA_PATH + stp.USR + '_mbz.csv')
##############################################################################
# Counts
##############################################################################
artistsDB = dataG[['Artist', 'MB_Geo1']]
cntryRaw = list(artistsDB['MB_Geo1'].unique())
cntry = sorted([x for x in cntryRaw if isinstance(x, str)])
# Artists frequencies --------------------------------------------------------
artistsPlayed = dataF['Artist'].unique()
artistCounts = dataF.groupby('Artist').size().reset_index(name='Frequency')
##############################################################################
# Compile data
##############################################################################
cix = cntry[1]
df = pd.DataFrame(columns=['Country', 'Frequency', 'Artists', 'Ratio'])
for cix in cntry:
    artsInCountry = artistsDB[artistsDB['MB_Geo1'] == cix]
    arts = set(artsInCountry['Artist'])
    artsWithFreq = artistCounts[artistCounts['Artist'].isin(arts)]
    freqByCountry = sum(artsWithFreq['Frequency'])
    df = df.append({
        'Country': cix, 
        'Frequency': freqByCountry,
        'Artists': len(arts),
        'Ratio': freqByCountry/len(arts)
    }, ignore_index=True)
##############################################################################
# Waffle Plots
##############################################################################
fig = plt.figure(
    FigureClass = Waffle,
    rows = 50, columns = 200,
    values = df.Ratio,
    labels = list(df.Country),
    interval_ratio_x=.5, interval_ratio_y=.5,
    legend={
        # 'labels': [f"{k} ({v}%)" for k, v in data.items()],  # lebels could also be under legend instead
        'loc': 'lower left',
        'bbox_to_anchor': (0, -0.25),
        'ncol': 10,
        'framealpha': 0,
        'fontsize': 12
    }
)
fig.set_size_inches(20, 20)
##############################################################################
# Tree Map
##############################################################################
# https://matplotlib.org/3.5.1/api/_as_gen/matplotlib.axes.Axes.text.html
# https://matplotlib.org/3.5.0/api/_as_gen/matplotlib.axes.Axes.bar.html
font = {'color': (1, 1, 1), 'weight': 'bold', 'rotation': 90, 'fontsize': 17.5}
bar = {'edgecolor': (0, 0, 0), 'linewidth': 2}
# Frequency ------------------------------------------------------------------
(cat, ths) = ('Frequency', 1000)
(fig, ax) = plt.subplots(1, 1, figsize=(15, 15))
dfSub = df[df[cat] > ths]
# cmap = matplotlib.cm.get_cmap("plasma")
# color = [cmap(random.random()) for i in range(dfSub.shape[0])]
squarify.plot(
    dfSub[cat], 
    label=dfSub['Country'], pad=True, 
    text_kwargs=font, bar_kwargs=bar
)
ax.set_aspect(1)
plt.axis('off')
# plt.show()
fig.savefig(
    stp.IMG_PATH + 'countryFrequency.png',
    dpi=RESOLUTION, orientation='portrait', papertype=None, format=None,
    facecolor='w', edgecolor='w',
    transparent=False,
    bbox_inches='tight', pad_inches=0, metadata=None
)
# Ratio ----------------------------------------------------------------------
(cat, ths) = ('Ratio', 25)
(fig, ax) = plt.subplots(1, 1, figsize=(15, 15))
dfSub = df[df[cat] > ths]
squarify.plot(
    dfSub[cat], 
    label=dfSub['Country'], pad=True, 
    text_kwargs=font, bar_kwargs=bar
)
ax.set_aspect(1)
plt.axis('off')
# plt.show()
fig.savefig(
    stp.IMG_PATH + 'countryRatio.png',
    dpi=RESOLUTION, orientation='portrait', papertype=None, format=None,
    facecolor='w', edgecolor='w',
    transparent=False,
    bbox_inches='tight', pad_inches=0, metadata=None
)