
from os import path
import pandas as pd
import numpy as np
from datetime import date, timedelta
from graph_tool.all import *
from mpl_chord_diagram import chord_diagram
import matplotlib.pyplot as plt
import setup as stp

(TOP, T_THRESHOLD, P_THRESHOLD) = (150, timedelta(minutes=30), 200)
(yLo, yHi) = ((1969, 1), (2023, 1))
yLo = [int(i) for i in yLo]
yHi = [int(i) for i in yHi]
###############################################################################
# Read Data
###############################################################################
pBase = path.join(stp.DATA_PATH, stp.USR)
DTA_CLN = pd.read_csv(pBase+'_cln.csv', parse_dates=[3])
DTA_MBZ = pd.read_csv(pBase+'_mbz.csv')
DTA_CLN = DTA_CLN.drop_duplicates()               
msk = [
    (
        (i.date() >= date(yLo[0], yLo[1], 1)) and 
        (i.date() < date(yHi[0], yHi[1], 1))
    ) 
    if (type(i) is not float) else (False) for i in DTA_CLN['Date']
]
DTA_CLN = DTA_CLN.loc[msk]
###############################################################################
# Check for Inflated Counts
###############################################################################
probe = DTA_CLN[DTA_CLN['Artist'] == 'Band of Horses']
probe['Date'] = pd.to_datetime(probe['Date'], errors='coerce', utc=True)
probe['Interval'] = probe['Date'].dt.to_period('D')
probe.groupby('Interval').size().sort_values(ascending=False)


DTA_CLN['Date'].unique()