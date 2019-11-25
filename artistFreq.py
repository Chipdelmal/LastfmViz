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

import setup as stp
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
# %matplotlib inline

##############################################################################
# Aesthetics parameters
##############################################################################
(WIDTH, HEIGHT, RESOLUTION) = (3840, 2160, 500)

##############################################################################
# Read artists file
##############################################################################
data = pd.read_csv(stp.DATA_PATH + stp.USR + '_artists.csv', parse_dates=[3])

##############################################################################
# Process artists
##############################################################################
artists = sorted(data.get('Artist').unique())
artistCount = data.groupby('Artist').size().sort_values(ascending=False)
artistCount.to_csv(stp.STAT_PATH + '/artistsPlaycount.csv', header=False)

##############################################################################
# Wordcloud
##############################################################################
wordcloudDef = WordCloud(
        width=WIDTH, height=HEIGHT, max_words=2000,
        relative_scaling=1, min_font_size=15,
        background_color='Black', colormap='Purples'
    )
wordcloud = wordcloudDef.generate_from_frequencies(artistCount)
ax1 = plt.axes(frameon=False)
plt.figure(figsize=(20, 20*(HEIGHT / WIDTH)), facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.tight_layout(pad=0)
plt.axis("off")
plt.savefig(
        stp.IMG_PATH + '/artistWordcloud.png',
        dpi=RESOLUTION, facecolor='k', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches='tight',
        metadata=None
    )

##############################################################################
# Barchart
##############################################################################
# artistCount[0:30].plot.bar()
# plt.xticks(rotation=90)
# plt.xlabel("")
# plt.ylabel("Play Count")
