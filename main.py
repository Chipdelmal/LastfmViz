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

# Load libraries
import aux
import creds
import ignoredArtists as ign
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
data = pd.read_csv(
        HIST_PATH + HIST_NAME,
        header=None, parse_dates=[3],
        names=['Artist', 'Album', 'Song', 'Date']
    )

##############################################################################
# Process artists
##############################################################################
artists = sorted(data.get('Artist').unique())
# Export artists list
with open(BASE_PATH + OUT_PATH + '/artists.txt', "w") as output:
    output.write(str(artists))
ign.BAN
