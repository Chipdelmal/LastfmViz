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

##############################################################################
# Setup PATHs
##############################################################################
# Working directories
(BASE_PATH, OUT_PATH) = (
        '/Users/sanchez.hmsc/Documents/GitHub/lastfmViz/', 'out'
    )

# Load CSV with history data
(HIST_PATH, HIST_NAME) = (
        '/Users/sanchez.hmsc/Documents/GitHub/lastfmViz/data/',
        'chipmaligno.csv'
    )

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
artists= sorted(data.get('Artist').unique())
artistCount = data.groupby('Artist').size().sort_values(ascending=False)
artistCount.to_csv(
        BASE_PATH + OUT_PATH + '/artistsPlaycount.csv',
        header=False
    )
