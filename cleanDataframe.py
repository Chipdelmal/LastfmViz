
from os import path
import pandas as pd
import numpy as np
from datetime import date, timedelta
from graph_tool.all import *
from mpl_chord_diagram import chord_diagram
import matplotlib.pyplot as plt
import setup as stp

(T_THRESHOLD, P_THRESHOLD) = (timedelta(minutes=30), 100)
(yLo, yHi) = ((1969, 1), (2023, 1))
yLo = [int(i) for i in yLo]
yHi = [int(i) for i in yHi]
###############################################################################
# Read Data
###############################################################################
pBase = path.join(stp.DATA_PATH, stp.USR)
DTA_CLN = pd.read_csv(pBase+'_cln.csv', parse_dates=[3])
DTA_MBZ = pd.read_csv(pBase+'_mbz.csv')
# Add Interval Column ---------------------------------------------------------
dteCpy = DTA_CLN['Date'].copy()
DTA_CLN['Interval'] = pd.to_datetime(dteCpy, errors='coerce', utc=True)
DTA_CLN['Interval'] = DTA_CLN['Interval'].dt.tz_localize(None).dt.to_period('D')
###############################################################################
# Read Data
###############################################################################
DTA_CLN = DTA_CLN.drop_duplicates()
(dLo, dHi) = (date(yLo[0], yLo[1], 1), date(yHi[0], yHi[1], 1))
msk = [
    ((i.date()>=dLo) and (i.date()<dHi)) 
    if (type(i) is not float) else (False) for i in DTA_CLN['Date']
]
DTA_CLN = DTA_CLN.loc[msk]
arts = sorted(list(DTA_CLN['Artist'].unique()))
###############################################################################
# Check for Inflated Counts
###############################################################################
banDict = {}
for artist in arts:
    probe = DTA_CLN[DTA_CLN['Artist'] == artist].copy()
    probe['Date'] = pd.to_datetime(probe['Date'], errors='coerce', utc=True)
    probe['Interval'] = probe['Date'].dt.tz_localize(None).dt.to_period('D')
    counts = probe.groupby('Interval').size().sort_values(ascending=False)
    dayObjs = list(counts[counts > P_THRESHOLD].index)
    banDates = [date(i.year, i.month, i.day) for i in dayObjs]
    if len(banDates) > 0:
        banDict[artist] = banDates
###############################################################################
# Remove Bans
###############################################################################
DTA_CLN['Interval'] = pd.to_datetime(
    DTA_CLN['Date'].copy(), errors='coerce', utc=True
)
DTA_CLN['Interval'] = DTA_CLN['Interval'].dt.tz_localize(None).dt.to_period('D')