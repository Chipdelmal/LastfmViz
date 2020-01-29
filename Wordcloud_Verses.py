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
import math
import numpy as np
import setup as stp
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from wordcloud import ImageColorGenerator
from matplotlib.colors import LinearSegmentedColormap

##############################################################################
cdict = {
        'red':   [(0, .2, .2), (1,  .0, .0)],
        'green': [(0, .2, .2), (1,  .0, .0)],
        'blue':  [(0, .2, .2), (1,  .0, .0)]
    }
cMap = LinearSegmentedColormap('csMap', cdict, N=256)
##############################################################################
# Aesthetics parameters
##############################################################################
(WIDTH, HEIGHT, RESOLUTION) = (3840, 2160, 2000)
(REL_SCL, MIN_SIZE, MAX_WRD) = (.03, 8, 5000)
##############################################################################
# Read artists file
##############################################################################
data = pd.read_csv(
        stp.DATA_PATH + stp.USR + '_vrs.csv',
        names=['Verse', 'Score']
    )
ranks = {
        str(data.iloc[i][0]):
            math.log(int(data.iloc[i][1])) for i in range(data.shape[0])
    }
# Mask data
mask = np.array(Image.open(stp.MSK_PATH + 'minipink.jpg'))
image_colors = ImageColorGenerator(mask)
# Wordcloud
wordcloudDef = WordCloud(
        width=WIDTH, height=HEIGHT, max_words=MAX_WRD,
        relative_scaling=REL_SCL, min_font_size=MIN_SIZE, prefer_horizontal=1,
        background_color="rgba(0, 0, 0, 1)", mode="RGBA",
        colormap=cMap,
        font_path=stp.FONT_PATH + 'mytype.ttf'  # , mask=mask
    )
wordcloud = wordcloudDef.generate_from_frequencies(ranks)
ax1 = plt.axes(frameon=False)
# ax1.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.figure()  # figsize=(20, 20*(HEIGHT / WIDTH)), facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.tight_layout(pad=0)
plt.axis("off")
plt.savefig(
        stp.IMG_PATH + 'VER_WDC.png', dpi=RESOLUTION,
        orientation='portrait', papertype=None, format=None, transparent=True,
        bbox_inches='tight', pad_inches=0, metadata=None
    )
plt.close('all')
