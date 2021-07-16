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
import os
import aux
import glob
import shapefile
import setup as stp
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


(CTRY_CODE, AUTO_BBOX) = ('US', False)
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
# Read data ###################################################################
data = pd.read_csv(stp.DATA_PATH + stp.USR + '_mbz.csv')
entries = data.shape[0]
data.get('Geo_2').value_counts()
data = data.fillna('NA')
# Filter NA ###################################################################
coordinates = []
for i in range(0, entries):
    (lat, lon) = (data['Lat'].iloc[i], data['Lon'].iloc[i])
    if (lat != 'NA') and (lon != 'NA'):
        coordinates.append((lon, lat))
###############################################################################
# Country Mask GIS
###############################################################################
ix = 0
filesSHP = sorted(glob.glob(stp.GIS_PATH + CTRY_CODE + '_adm/' + '*.shp'))[ix]
fileID = filesSHP.split("/")[-1].split('.')[0]
if AUTO_BBOX:
    sf = shapefile.Reader(stp.GIS_PATH + CTRY_CODE + '_adm/' + fileID + '.dbf')
    bbox = sf.bbox
else:
    bbox = stp.CNTRY_BOX[CTRY_CODE]
print(bbox)
# Plot GIS
fig = plt.gcf()
ax = fig.add_subplot(111, label="1")
ax.axis('off')
map = Basemap(
        llcrnrlon=bbox[0], llcrnrlat=bbox[1],
        urcrnrlon=bbox[2], urcrnrlat=bbox[3],
        resolution='i', projection='merc'
    )
gisData = map.readshapefile(os.path.splitext(filesSHP)[0], CTRY_CODE)
map.drawcoastlines(color=COLORS[3], linewidth=.25, zorder=1)
map.fillcontinents(color=COLORS[3], lake_color=COLORS[3])
map.drawmapboundary(fill_color=COLORS[3])
lines = gisData[4]
lines.set_facecolors('black')
lines.set_alpha(1)
outPath = stp.GIS_PATH + 'MSK_' + CTRY_CODE + '.png'
plt.savefig(
        outPath,
        dpi=1000, bbox_inches='tight', pad_inches=0.0, frameon=None
    )
plt.close()
print(outPath)
print("Finished!")
