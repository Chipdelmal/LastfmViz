##############################################################################
#  _           _    __           _   _ _
# | |         | |  / _|         | | | (_)
# | | __ _ ___| |_| |_ _ __ ___ | | | |_ ____
# | |/ _` / __| __|  _| '_ ` _ \| | | | |_  /
# | | (_| \__ \ |_| | | | | | | \ \_/ / |/ /
# |_|\__,_|___/\__|_| |_| |_| |_|\___/|_/___|
#
# ----------------------------------------------------------------------------
# Musicbrainz parser for places and genres
##############################################################################
import aux
import csv
import keys
import setup as stp
import pandas as pd
import musicbrainzngs as mb
# from geopy.geocoders import Nominatim

FILE_PATH = stp.DATA_PATH + stp.USR + '_mbz.csv'
# Logging in
mb.auth(keys.MB_USR, keys.MB_PSW)
mb.set_useragent("lastfm", "0.1", "http://chipdelmal.github.io")
# Read artists list
data = pd.read_csv(stp.DATA_PATH + stp.USR + '_art.csv', parse_dates=[3])
artists = data['Artist'].unique()[0:]
artists
# Write CSV
artNum = len(artists)
with open(FILE_PATH, mode='w') as mbFile:
    mbWriter = csv.writer(mbFile, quoting=csv.QUOTE_MINIMAL)
    header = aux.generateMBHeader(stp.TOP_GENRES, stp.GEO_SIZE)
    mbWriter.writerow(header)
    for (i, art) in enumerate(artists):
        # Parse musicbranz database
        info = aux.getArtistInfo(art, topGenres=stp.TOP_GENRES)
        info = aux.geocodeEntries(info)
        mbWriter.writerow(info)
        print('Parsed: {0}/{1}'.format(i+1, artNum))
