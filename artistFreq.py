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
import setup as stp
import pandas as pd
# import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from matplotlib.colors import LinearSegmentedColormap


cdict = {
        'red':   [(0.0, 1, 1), (0.5,  0.8, 0.8), (1.0,  0.6, 0.6)],
        'green': [(0.0,  1, 1), (0.5, 0.8, 0.8), (1.0,  0.6, 0.6)],
        'blue':  [(0.0, 1, 1), (0.5,  0.8, 0.8), (1.0,  .75, .75)]
    }
cpalette = LinearSegmentedColormap('DarkBlue1', cdict, N=126)

(WIDTH, HEIGHT, RESOLUTION) = (851*4, 315*4, 750)
##############################################################################
# Read artists file
##############################################################################
data = pd.read_csv(stp.DATA_PATH + stp.USR + '_art.csv', parse_dates=[3])
artists = sorted(data.get('Artist').unique())
artistCount = data.groupby('Artist').size().sort_values(ascending=False)

##############################################################################
# Wordcloud
##############################################################################
wordcloudDef = WordCloud(
        width=WIDTH, height=HEIGHT, max_words=2000,
        relative_scaling=.5, min_font_size=5,
        background_color='rgba(0, 0, 0, 1)', mode='RGBA',
        colormap=cpalette, font_path=stp.FONT
    )
wordcloud = wordcloudDef.generate_from_frequencies(artistCount)
# ax1 = plt.axes(frameon=False)
plt.figure(figsize=(20, 20*(HEIGHT / WIDTH)), facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.tight_layout(pad=0)
plt.axis("off")
plt.savefig(
        stp.IMG_PATH + '/ART_WDC.png',
        dpi=RESOLUTION, facecolor='Black', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches='tight',
        metadata=None
    )
