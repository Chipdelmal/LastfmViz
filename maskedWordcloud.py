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
# %matplotlib inline

##############################################################################
# Aesthetics parameters
##############################################################################
(WIDTH, HEIGHT, RESOLUTION) = (3840/2, 2160/2, 500)

##############################################################################
# Read artists file
##############################################################################
data = pd.read_csv(stp.DATA_PATH + stp.USR + '_art.csv', parse_dates=[3])
songs = sorted(data.get('Song').unique())
songCount = data.groupby('Song').size().sort_values(ascending=False)
mask = np.array(Image.open(stp.IMG_PATH + "MapGBMask.png"))

##############################################################################
# Wordcloud
##############################################################################
wordcloudDef = WordCloud(
        width=WIDTH, height=HEIGHT, max_words=2000,
        relative_scaling=1, min_font_size=20,
        background_color='Black', colormap='Purples',
        font_path=stp.FONT, mask=mask
    )
wordcloud = wordcloudDef.generate_from_frequencies(songCount)
ax1 = plt.axes(frameon=False)
plt.figure(figsize=(20, 20*(HEIGHT / WIDTH)), facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.tight_layout(pad=0)
plt.axis("off")
plt.savefig(
        stp.IMG_PATH + '/MapWordcloud.png',
        dpi=RESOLUTION, facecolor='k', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches='tight',
        metadata=None
    )
