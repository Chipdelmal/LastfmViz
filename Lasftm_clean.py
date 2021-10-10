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
import aux
import setup as stp
import pandas as pd

print('* Cleaning dataset')
##############################################################################
# Read and shape CSV
##############################################################################
dataRaw = pd.read_csv(
        stp.DATA_PATH + stp.USR + '.csv',
        header=None, names=['Artist', 'Album', 'Song', 'Date'],
        parse_dates=[3]
    )
##############################################################################
# Process artists: remove artists present in the BAN list
##############################################################################
data = aux.removeBanned(dataRaw)
timeInfo = pd.to_datetime(data["Date"], unit='ms')
fixedTime = timeInfo.dt.tz_localize('UTC').dt.tz_convert(stp.TIMEZONE)
data = data.assign(Date=fixedTime)
data.to_csv(stp.DATA_PATH + stp.USR + '_cln.csv', index=False)
##############################################################################
# Process artists and songs rankings
##############################################################################
(artistCount, songCount) = (
        aux.getPlaycount(data, label='Artist'),
        aux.getPlaycount(data, label='Song')
    )
artistCount.to_csv(stp.STAT_PATH + '/ART_PLC.csv', header=False)
songCount.to_csv(stp.STAT_PATH + '/SNG_PLC.csv', header=False)
