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
import csv
import keys
import setup as stp
import pandas as pd
import musicbrainzngs as mb

FILE_PATH = stp.DATA_PATH + 'chipmaligno_mb.csv'
# Logging in
mb.auth(keys.MB_USR, keys.MB_PSW)
mb.set_useragent("lastfm", "0.1", "http://chipdelmal.github.io")
# Read artists list
data = pd.read_csv(stp.DATA_PATH + stp.USR + '_artists.csv', parse_dates=[3])
artists = data['Artist'].unique()
# Write CSV
artNum = len(artists)
with open(FILE_PATH, mode='w') as employee_file:
    employee_writer = csv.writer(
            employee_file, delimiter=',', quotechar='"',
            quoting=csv.QUOTE_MINIMAL
        )
    for (i, art) in enumerate(artists):
        info = aux.getArtistInfo(art)
        employee_writer.writerow(info)
        print('Parsed: {0}/{1}'.format(i+1, artNum))
