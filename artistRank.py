
# import math
import cv2
import aux as aux
import datetime
import setup as stp
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib import font_manager
from sys import argv

RANKS = 10
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
# Rank
#############################################################################
dateSlice = dfFltrd['Date'].apply(lambda x: "%d/%d" % (x.month, x.year)).copy()
dfFltrd.insert(3, 'DateGroup', dateSlice)
dfFltrd.groupby(['Artist', 'DateGroup']).size()