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
from PIL import Image
import numpy as np
from itertools import compress

(CTRY_CODE, bkg, transpBG) = ('US', 1, True)
##############################################################################
# Aesthetics parameters
##############################################################################
(WIDTH, HEIGHT, RESOLUTION) = (3840/2, 2160/2, 500)
(CTRY_NAME, cmap, font) = stp.CNTRY_CODE[CTRY_CODE]
##############################################################################
# Read artists file
##############################################################################
data = pd.read_csv(stp.DATA_PATH + stp.USR + '_cln.csv', parse_dates=[3])
artists = sorted(data.get('Artist').unique())
artistCount = data.groupby('Artist').size().sort_values(ascending=False)
##############################################################################
# Read geo file and filter artists by geography
##############################################################################
dataG = pd.read_csv(stp.DATA_PATH + stp.USR + '_mbz.csv')
filter = dataG['Geo_1'].isin(stp.CNTRY_ALIAS[CTRY_CODE])
fDataG = dataG[filter]
artistsG = sorted(fDataG.get('Artist').unique())
artistsG = fDataG['Artist']
fArtists = set(artistsG)
##############################################################################
# Filter Counts with Geo
##############################################################################
names = artistCount.index.values
counts = list(artistCount)
geoFilter = [i in fArtists for i in names]
pairedCounts = list(zip(names, counts))
artistCountFinal = dict(compress(pairedCounts, geoFilter))
##############################################################################
# Wordcloud
##############################################################################
if transpBG:
    bgCol = "rgba(1, 1, 1, 0)"
else:
    bgCol = "Black"
mask = np.array(Image.open(stp.GIS_PATH + 'MSK_' + CTRY_CODE + '.png'))
wordcloudDef = WordCloud(
        width=WIDTH, height=HEIGHT, max_words=5000,
        relative_scaling=.4, min_font_size=8, prefer_horizontal=.8,
        background_color=bgCol, mode="RGBA",
        colormap=cmap, font_path=stp.FONT_PATH + font, mask=mask
    )
wordcloud = wordcloudDef.generate_from_frequencies(artistCountFinal)
ax1 = plt.axes(frameon=False)
plt.figure(figsize=(20, 20*(HEIGHT / WIDTH)), facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.tight_layout(pad=0)
plt.axis("off")
outPath = stp.IMG_PATH + 'MAP_' + CTRY_CODE + '.png'
if transpBG:
    plt.savefig(
            outPath,
            dpi=RESOLUTION, orientation='portrait', papertype=None, format=None,
            transparent=True,
            bbox_inches='tight', pad_inches=.1, metadata=None
        )
else:
    plt.savefig(
            outPath,
            dpi=RESOLUTION, orientation='portrait', papertype=None, format=None,
            facecolor='k', edgecolor='k',
            transparent=True,
            bbox_inches='tight', pad_inches=.1, metadata=None
        )
plt.close('all')
print(outPath)