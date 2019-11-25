##############################################################################
#  _           _    __           _   _ _
# | |         | |  / _|         | | | (_)
# | | __ _ ___| |_| |_ _ __ ___ | | | |_ ____
# | |/ _` / __| __|  _| '_ ` _ \| | | | |_  /
# | | (_| \__ \ |_| | | | | | | \ \_/ / |/ /
# |_|\__,_|___/\__|_| |_| |_| |_|\___/|_/___|
#
##############################################################################
# Lastfm scrobbles visualizer
##############################################################################

import aux
# import creds
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
%matplotlib inline

##############################################################################
# Setup PATHs
##############################################################################
# Working directories
(BASE_PATH, OUT_PATH, IMG_PATH) = (
        '/Users/sanchez.hmsc/Documents/GitHub/lastfmViz/', 'out', 'img'
    )

# Load CSV with history data
(HIST_PATH, HIST_NAME) = (
        '/Users/sanchez.hmsc/Documents/GitHub/lastfmViz/data/',
        'chipmaligno.csv'
    )

(WIDTH, HEIGHT, RESOLUTION) = (3840, 2160, 500)

##############################################################################
# Read and shape CSV
##############################################################################
dataRaw = pd.read_csv(
        HIST_PATH + HIST_NAME,
        header=None, parse_dates=[3],
        names=['Artist', 'Album', 'Song', 'Date']
    )

##############################################################################
# Process artists
##############################################################################
artistsRaw = sorted(dataRaw.get('Artist').unique())
# Remove artists present in the BAN list
data = dataRaw[~dataRaw['Artist'].isin(aux.BAN)]
artists = sorted(data.get('Artist').unique())
artistCount = data.groupby('Artist').size().sort_values(ascending=False)
artistCount.to_csv(
        BASE_PATH + OUT_PATH + '/artistsPlaycount.csv',
        header=False
    )


# Barchart
artistCount[0:30].plot.bar()
plt.xticks(rotation=90)
plt.xlabel("")
plt.ylabel("Play Count")
plt.show()

# Wordcloud
wordcloudDef = WordCloud(
        width=WIDTH, height=HEIGHT, max_words=2000,
        relative_scaling=1, min_font_size=10,
        background_color='Black', colormap='Purples'
    )
wordcloud = wordcloudDef.generate_from_frequencies(artistCount)
ax1 = plt.axes(frameon=False)
plt.figure(figsize=(20, 20*(HEIGHT/WIDTH)), facecolor='k')
plt.imshow(wordcloud, interpolation='bilinear')
plt.tight_layout(pad=0)
plt.axis("off")
plt.savefig(
        IMG_PATH + '/artistWordcloud.png',
        dpi=RESOLUTION, facecolor='k', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches=None, pad_inches='tight',
        metadata=None
    )
