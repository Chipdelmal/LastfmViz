##############################################################################
#  _           _    __           _   _ _
# | |         | |  / _|         | | | (_)
# | | __ _ ___| |_| |_ _ __ ___ | | | |_ ____
# | |/ _` / __| __|  _| '_ ` _ \| | | | |_  /
# | | (_| \__ \ |_| | | | | | | \ \_/ / |/ /
# |_|\__,_|___/\__|_| |_| |_| |_|\___/|_/___|
#
# ----------------------------------------------------------------------------
# Spatial statistics for use in other analyses
##############################################################################

import aux
import setup as stp
import pandas as pd
from collections import Counter

##############################################################################
# Read data
##############################################################################
data = pd.read_csv(stp.DATA_PATH + stp.USR + '_mbz.csv')
##############################################################################
# Export country frequencies
##############################################################################
cntry = [x for x in list(data['Geo_1']) if str(x) != 'nan']
cntryClean = [stp.CNTRY_FIX.get(n, n) for n in cntry]
cntryFreq = Counter(cntryClean)
aux.writeFrequencyDictToCSV(stp.STAT_PATH + 'CTR_FRQ.csv', cntryFreq)
##############################################################################
# Explore
##############################################################################
set(cntry)
filter = (data['Geo_1'] == "Argentina")
data[filter]

# MB Country codes
cntry = [x for x in list(data['MB_Geo1']) if str(x) != 'nan']
cntryClean = [stp.CNTRY_FIX.get(n, n) for n in cntry]
set(cntryClean)
