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
import keys
import setup as stp
import pandas as pd
import musicbrainzngs as mb

print('* Downloading data from MusicBrainz')
# Logging in
mb.auth(keys.MB_USR, keys.MB_PSW)
mb.set_useragent(keys.MB_NM, keys.MB_V, keys.MB_URL)
# Read artists list and write CSV and parse musicbrainz to file
data = pd.read_csv(stp.DATA_PATH + stp.USR + '_cln.csv', parse_dates=[3])
aux.parseFromMusicbrainz(data)
