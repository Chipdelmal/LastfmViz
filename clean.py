##############################################################################
#  _           _    __           _   _ _
# | |         | |  / _|         | | | (_)
# | | __ _ ___| |_| |_ _ __ ___ | | | |_ ____
# | |/ _` / __| __|  _| '_ ` _ \| | | | |_  /
# | | (_| \__ \ |_| | | | | | | \ \_/ / |/ /
# |_|\__,_|___/\__|_| |_| |_| |_|\___/|_/___|
#
# ----------------------------------------------------------------------------
# Data cleaning routines
##############################################################################

import setup as stp
import pandas as pd

##############################################################################
# Read and shape CSV
##############################################################################
dataRaw = pd.read_csv(
        stp.DATA_PATH + stp.USR + '.csv',
        header=None, parse_dates=[3],
        names=['Artist', 'Album', 'Song', 'Date']
    )

##############################################################################
# Process artists: remove artists present in the BAN list
##############################################################################
artistsRaw = sorted(dataRaw.get('Artist').unique())
data = dataRaw[~dataRaw['Artist'].isin(stp.BAN)]
fixedTime = pd.to_datetime(
            data["Date"],
            unit='ms').dt.tz_localize('UTC').dt.tz_convert(stp.TIMEZONE)
data = data.assign(Date=fixedTime)
data.to_csv(stp.DATA_PATH + stp.USR + '_art.csv', index=False)

##############################################################################
# Process artists: Counts Ranking
##############################################################################
artists = sorted(data.get('Artist').unique())
artistCount = data.groupby('Artist').size().sort_values(ascending=False)
artistCount.to_csv(stp.STAT_PATH + '/artistsPlaycount.csv', header=False)

##############################################################################
# Process songs: Counts Ranking
##############################################################################
songs = sorted(data.get('Song').unique())
songCount = data.groupby('Song').size().sort_values(ascending=False)
songCount.to_csv(stp.STAT_PATH + '/songsPlaycount.csv', header=False)
