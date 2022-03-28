import math
from sys import argv
import datetime
import aux as aux
import setup as stp
import numpy as np
import pandas as pd
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
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

artistsPlayed = dataF['Artist'].unique()
artistCounts = dataF.groupby('Artist').size()
