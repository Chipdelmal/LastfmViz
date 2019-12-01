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
# import csv
# import keys
import numpy as np
import setup as stp
import pandas as pd
# import musicbrainzngs as mb
import matplotlib.pyplot as plt
# import matplotlib.patches as mpatches
from mpl_toolkits.basemap import Basemap
# %matplotlib inline

data = pd.read_csv(stp.DATA_PATH + stp.USR + '_mbz.csv')
entries = data.shape[0]
data.get('Geo_2').value_counts()
data = data.fillna('NA')

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
# map.arcgisimage(service="NatGeo_World_Map", xpixels=2000)
map.drawcoastlines(color=COLORS[5], linewidth=.25, zorder=1)
map.drawcoastlines(color=COLORS[5], linewidth=.25, zorder=1)
# map.drawcoastlines(color=COLORS[4], linewidth=.5, zorder=1)
map.fillcontinents(color=COLORS[5], lake_color=COLORS[5])
map.drawmapboundary(fill_color=COLORS[5])
# map.drawcountries(color=COLORS[0], linewidth=2)
plt.savefig(
        stp.IMG_PATH + "MapMask.png",
        dpi=1000, bbox_inches='tight', pad_inches=0.0, frameon=None
    )
plt.close()

###############################################################################
# Country Mask GIS
###############################################################################
# https://www.diva-gis.org/gdata
fig = plt.gcf()
ax = fig.add_subplot(111, label="1")
ax.axis('off')
map = Basemap(
            llcrnrlon=-3.8955253-10, llcrnrlat=53.8710916-10,
            urcrnrlon=-3.8955253+10., urcrnrlat=53.8710916+10,
            resolution='i', projection='merc',
            lat_0=54.8710916, lon_0=10.8955253)
map.drawcoastlines(color=COLORS[3], linewidth=.25, zorder=1)
map.fillcontinents(color=COLORS[3], lake_color=COLORS[3])
map.drawmapboundary(fill_color=COLORS[3])
# map.drawcoastlines()
data = map.readshapefile(stp.BASE_PATH + 'gis/GBR_adm/GBR_adm0', 'GB')
italy = data[4]
italy.set_facecolors('black')
italy.set_alpha(1)
plt.savefig(
        stp.IMG_PATH + "MapGBMask.png",
        dpi=1000, bbox_inches='tight', pad_inches=0.0, frameon=None
    )
plt.close()
