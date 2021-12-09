
# import math
import aux as aux
import datetime
import setup as stp
import pandas as pd
import numpy as np
import matplotlib.pylab as ply
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline


RANKS = 15
(WIDTH, HEIGHT, RESOLUTION) = (1920, 1920, 500)
(yLo, yHi) = ((2012, 1), (2022, 1))
# (yLo, yHi) = (
#     (argv[1], argv[2]), 
#     (argv[3], argv[4])
# )
DATE = True
yLo = [int(i) for i in yLo]
yHi = [int(i) for i in yHi]
##############################################################################
# Read artists file
##############################################################################
data = pd.read_csv(stp.DATA_PATH + stp.USR + '_cln.csv', parse_dates=[3])
data = data.drop_duplicates()
if DATE:
    msk = [
        (
            (i.date() >= datetime.date(yLo[0], yLo[1], 1)) and 
            (i.date() < datetime.date(yHi[0], yHi[1], 1))
        ) 
        if (type(i) is not float) else (False) for i in data['Date']
    ]
    data = data.loc[msk]
##############################################################################
# Count frequencies
##############################################################################
artists = sorted(data.get('Artist').unique())
artistCount = data.groupby('Artist').size().sort_values(ascending=False)
topArtists = list(artistCount.index)[:RANKS]
dfFltrd = data[data['Artist'].isin(set(topArtists))]
##############################################################################
# Count and Reshape
##############################################################################
dateSlice = dfFltrd['Date'].apply(lambda x: "{}/{:02d}".format(x.year, x.month)).copy()
dfFltrd.insert(3, 'DateGroup', dateSlice)
grpd = dfFltrd.groupby(['Artist', 'DateGroup']).size()
dfTable = grpd.unstack().reset_index().set_index("Artist")
dfCounts = dfTable.replace(np.nan,0)
##############################################################################
# Rolling
##############################################################################
(WIN_W, WIN_M) = (12, 12)
dfCountsR = dfCounts.rolling(window=WIN_W, axis=1, min_periods=WIN_M).mean()
##############################################################################
# Rank
##############################################################################
dfRanks = dfCounts.rank(ascending=False, method='first', axis=0)
dfRanksR = dfCountsR.rank(ascending=False, method='first', axis=0)
##############################################################################
# Plots
##############################################################################
dates = sorted(list(dfCounts.columns))
artists = sorted(list(dfCounts.index))
cmap = aux.colorPaletteFromHexList([
    '#461177', '#bde0fe', '#f0a6ca', '#ff0054', '#5465ff', '#ff499e'
])
(ySpace, colors) = (1, cmap(np.linspace(0, 1, len(artists))))
xExtend = 2
# Stats -----------------------------------------------------------------------
artistsT0 = list(dfRanksR.index)
ranksDate = list(dfRanksR.columns)[WIN_M-1]
ranksT0 = list(dfRanksR[ranksDate])
ranksDateF = list(dfRanksR.columns)[-1]
ranksTF = list(dfRanksR[ranksDateF])
# Ranks Plot ------------------------------------------------------------------
t = list(range(0, len(dates)+xExtend, 1))
xnew = np.linspace(0, max(t), 500)
yearTicks = [i for i, s in enumerate(dates) if '/01' in s]
dteTicks = [item[:4] for item in dates if '/01' in item]
(fig, ax) = plt.subplots(1, 1, figsize=(15, 3.5))
for i in range(len(artists)):
    y = RANKS-(np.asarray(dfRanksR.iloc[i])-1)*ySpace
    # spl = make_interp_spline(t, y, k=0)
    # power_smooth = spl(xnew)
    y[np.isnan(y)]=y[WIN_M]
    z = np.append(y, [y[-1]]*xExtend)
    plt.plot(
        t, z,
        lw=2, alpha=.75, color=colors[i],
        marker='.', markersize=0,
        solid_joinstyle='round',
        solid_capstyle='butt'
    )
ax.vlines(
    yearTicks, 0, 1, 
    lw=.5, ls=':', transform=ax.get_xaxis_transform(),
    color='w'
)
ax.vlines(
    [i-6 for i in yearTicks], 0, 1, 
    lw=.25, ls=':', transform=ax.get_xaxis_transform(),
    color='w'
)
for (art, pos) in zip(artistsT0, ranksT0):
    ax.text(
        -1, RANKS-ySpace*(int(pos)-1)-ySpace*.4, art, 
        ha='right', color='w', fontsize=8
    )
for (art, pos) in zip(artistsT0, ranksTF):
    ax.text(
        len(dates)-1+xExtend+1, RANKS-ySpace*(int(pos)-1)-ySpace*.4, art, 
        ha='left', color='w', fontsize=8
    )
ax.set_aspect(.2/ax.get_data_ratio(), adjustable='box')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.get_xaxis().set_ticks(yearTicks)
a = ax.get_xticks().tolist()
for i in range(len(a)):
    a[i] = dteTicks[i]
ax.get_xaxis().set_ticklabels(a)
ax.get_yaxis().set_ticks([])
ax.spines['bottom'].set_color('white')
ax.tick_params(axis='x', colors='white')
ax.set_xlim(ax.get_xlim()[0], len(dates)-1+xExtend)
plt.savefig(
    stp.IMG_PATH + 'artistsRank.png',
    dpi=RESOLUTION, orientation='portrait', papertype=None, format=None,
    facecolor='k', edgecolor='w',
    transparent=True,
    bbox_inches='tight', pad_inches=0, metadata=None
)
plt.close('all')
