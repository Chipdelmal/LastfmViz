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
from wordcloud import ImageColorGenerator
##############################################################################
# Aesthetics parameters
##############################################################################
(WIDTH, HEIGHT, RESOLUTION, ALPHA_BG) = (3840, 2160, 1000, 1)
##############################################################################
# Read artists file
##############################################################################
data = pd.read_csv(
        stp.DATA_PATH + stp.USR + '_vrs.csv',
        names=['Verse', 'Score']
    )
ranks = {
        str(data.iloc[i][0]): int(data.iloc[i][1]) for i in range(data.shape[0])
    }
# Mask data
mask = np.array(Image.open(stp.MSK_PATH + 'minipink.jpg'))
image_colors = ImageColorGenerator(mask)
# Wordcloud
wordcloudDef = WordCloud(
        width=WIDTH, height=HEIGHT, max_words=5000,
        relative_scaling=.8, min_font_size=8, prefer_horizontal=1,
        background_color="rgba(0, 0, 0, " + str(ALPHA_BG) + "1)", mode="RGBA",
        colormap='seismic',
        font_path=stp.FONT_PATH + 'WildernessTypeface-Regular.ttf'  # , mask=mask
    )
wordcloud = wordcloudDef.generate_from_frequencies(ranks)
ax1 = plt.axes(frameon=False)
# ax1.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
plt.figure()  # figsize=(20, 20*(HEIGHT / WIDTH)), facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.tight_layout(pad=0)
plt.axis("off")
plt.savefig(
        stp.IMG_PATH + 'VER_WDC.png',
        dpi=RESOLUTION,
        orientation='portrait', papertype=None, format=None,
        transparent=True, bbox_inches='tight', pad_inches=.1,
        metadata=None
    )
plt.close('all')
