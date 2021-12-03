##############################################################################
#  _           _    __           _   _ _
# | |         | |  / _|         | | | (_)
# | | __ _ ___| |_| |_ _ __ ___ | | | |_ ____
# | |/ _` / __| __|  _| '_ ` _ \| | | | |_  /
# | | (_| \__ \ |_| | | | | | | \ \_/ / |/ /
# |_|\__,_|___/\__|_| |_| |_| |_|\___/|_/___|
#
# ----------------------------------------------------------------------------
# Artists frequencies routines
##############################################################################
# import math
import aux as aux
import datetime
import setup as stp
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from sys import argv

(WIDTH, HEIGHT, RESOLUTION) = (1920, 1920, 750)
(yLo, yHi) = ((2012, 1), (2013, 1))
(yLo, yHi) = (
    (argv[1], argv[2]), 
    (argv[3], argv[4])
)
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
# Count
##############################################################################
artists = sorted(data.get('Artist').unique())
artistCount = data.groupby('Artist').size().sort_values(ascending=False)
######################################################################
# Wordcloud
##############################################################################
cmap = aux.colorPaletteFromHexList([
    '#011627', '#004e89', '#011627', '#ff006e'
])
########
wordcloudDef = WordCloud(
        width=WIDTH, height=HEIGHT, max_words=2000,
        relative_scaling=.5, min_font_size=8, font_path=stp.FONT,
        background_color='white', #mode='RGBA',
        colormap=cmap # stp.cMap
    )
wordcloud = wordcloudDef.generate_from_frequencies(artistCount)
plt.figure(figsize=(20, 20*(HEIGHT / WIDTH)), facecolor='w')
plt.imshow(wordcloud, interpolation='bilinear')
plt.tight_layout(pad=0)
plt.axis("off")
plt.savefig(
        stp.IMG_PATH + '/ART_WDC-{}_{}.png'.format(yLo[0], yHi[0]),
        dpi=RESOLUTION, facecolor='white', edgecolor='white',
        orientation='portrait', papertype=None, format=None,
        transparent=True, bbox_inches='tight', pad_inches=.1,
        metadata=None
    )
