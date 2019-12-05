##############################################################################
#  _           _    __           _   _ _
# | |         | |  / _|         | | | (_)
# | | __ _ ___| |_| |_ _ __ ___ | | | |_ ____
# | |/ _` / __| __|  _| '_ ` _ \| | | | |_  /
# | | (_| \__ \ |_| | | | | | | \ \_/ / |/ /
# |_|\__,_|___/\__|_| |_| |_| |_|\___/|_/___|
#
# ----------------------------------------------------------------------------
# Musicbrainz parser for geolocation and genres
##############################################################################
import aux
import numpy as np
import setup as stp
import pandas as pd
import matplotlib.pyplot as plt

# Setup Style #################################################################
PAD = 25
COLORS = [
        aux.rescaleRGBA((0, 76, 255, 255/2.5)),     # 0: Faded navy blue
        aux.rescaleRGBA((217, 3, 104, 255/1)),      # 1: Magenta
        aux.rescaleRGBA((37, 216, 17, 255/6)),      # 2: Bright green
        aux.rescaleRGBA((255, 255, 255, 255/5)),    # 3: White
        aux.rescaleRGBA((0, 169, 255, 255/7.5)),    # 4: Cyan
        aux.rescaleRGBA((0, 0, 0, 255/1)),          # 5: Black
        aux.rescaleRGBA((135, 147, 255, 255/1))
    ]
# Read MusicBrainz data #######################################################
data = pd.read_csv(stp.DATA_PATH + stp.USR + '_mbz.csv')
entries = data.shape[0]
# data.get('Geo_2').value_counts()
data = data.fillna('NA')
# Filter NA ###################################################################
coordinates = []
for i in range(0, entries):
    (lat, lon) = (data['Lat'].iloc[i], data['Lon'].iloc[i])
    if (lat != 'NA') and (lon != 'NA'):
        coordinates.append((lon, lat))
# Calculate boundary ##########################################################
(minLon, minLat) = np.amin(coordinates, 0)
(maxLon, maxLat) = np.amax(coordinates, 0)
# Export Map ##################################################################
fig = plt.gcf()
ax = fig.add_subplot(111, label="1")
ax.axis('off')
map = aux.createBasemapInstance(minLat, maxLat, minLon, maxLon, pad=PAD)
map.drawcoastlines(color=COLORS[3], linewidth=.25, zorder=1)
map.drawcoastlines(color=COLORS[3], linewidth=.25, zorder=1)
map.fillcontinents(color=COLORS[5], lake_color=COLORS[5])
map.drawmapboundary(fill_color=COLORS[5])
map.scatter(
        [i[0] for i in coordinates], [i[1] for i in coordinates],
        s=.01, alpha=.5, marker=".",
        edgecolors=COLORS[6], color=COLORS[6], zorder=2
    )
plt.savefig(
        stp.IMG_PATH + "ART_MAP.png",
        dpi=1000, bbox_inches='tight', pad_inches=0.0, frameon=None
    )
plt.close()
