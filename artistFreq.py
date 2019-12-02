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
# %matplotlib inline

(WIDTH, HEIGHT, RESOLUTION) = (851*4, 315*4, 500)
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
        relative_scaling=1, min_font_size=15,
        background_color='rgba(0, 0, 0, 1)', mode='RGBA',
        colormap='Purples', font_path=stp.FONT
    )
wordcloud = wordcloudDef.generate_from_frequencies(artistCount)
# ax1 = plt.axes(frameon=False)
plt.figure(figsize=(20, 20*(HEIGHT / WIDTH)), facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.tight_layout(pad=0)
plt.axis("off")
plt.savefig(
        stp.IMG_PATH + '/artistWordcloud.png',
        dpi=RESOLUTION, facecolor='Black', edgecolor='w',
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

# import matplotlib.pyplot as plt
# from matplotlib import cm
# from math import log10
#
#
# data = artistCount[:50]
# labels = list(data.axes[0])
# #number of data points
# n = len(data)
# #find max value for full ring
# k = 10 ** int(log10(max(data)))
# m = k * (1 + max(data) // k)
#
# #radius of donut chart
# r = 10
# #calculate width of each ring
# w = r / n
# #create colors along a chosen colormap
# colors = [cm.terrain(i / n) for i in range(n)]
# #create figure, axis
# fig, ax = plt.subplots()
# ax.axis("equal")
#
#
# #create rings of donut chart
# for i in range(n):
#     #hide labels in segments with textprops: alpha = 0 - transparent, alpha = 1 - visible
#     innerring, _ = ax.pie([m - data[i], data[i]], radius = r - 1 * i * w, startangle = 90, #labels = ["", labels[i]], labeldistance = 1 - 1 / (1.5 * (n - i)),
#     textprops = {"alpha": 0}, colors = ["white", colors[i]])
#     plt.setp(innerring, width = w, edgecolor = "white")
# #plt.figure(figsize=(2*r,2*r), facecolor='k')
# #plt.legend()
# #plt.show()
# plt.savefig(
#         stp.IMG_PATH + '/artistFrequencies.png',
#         dpi=  RESOLUTION, facecolor='w', edgecolor='w',
#         orientation='portrait', papertype=None, format=None,
#         transparent=False, bbox_inches=None, pad_inches='tight',
#         metadata=None
#     )
