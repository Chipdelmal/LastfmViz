
# import math
import aux as aux
import datetime
import setup as stp
import pandas as pd
import numpy as np
import matplotlib.pylab as ply
import matplotlib.pyplot as plt


RANKS = 25
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
(WIN_W, WIN_M) = (6, 1)
dfCountsR = dfCounts.rolling(window=WIN_W, axis=1, min_periods=WIN_M).median()
##############################################################################
# Rank
##############################################################################
dfRanks = dfCounts.rank(ascending=True, method='first', axis=0)
dfRanksR = dfCountsR.rank(ascending=True, method='first', axis=0)
##############################################################################
# Plots
##############################################################################
dates = sorted(list(dfCounts.columns))
artists = sorted(list(dfCounts.index))
(ySpace, colors) = (1, ply.cm.BuPu(np.linspace(0, 1, len(artists))))
# Ranks Plot ------------------------------------------------------------------
(fig, ax) = plt.subplots(1, 1, figsize=(15, 3.5))
for i in range(len(artists)):
    plt.plot(
        (np.asarray(dfRanksR.iloc[i])-1)*ySpace,
        lw=2, alpha=.6, color=colors[i],
        marker='.', markersize=0,
        solid_joinstyle='round',
        solid_capstyle='butt'
    )
ax.set_aspect(.1/ax.get_data_ratio(), adjustable='box')
ax.set_xlim(WIN_M, len(dates)-1)