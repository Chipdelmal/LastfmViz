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

##############################################################################
# Export country frequencies
##############################################################################
data = pd.read_csv(stp.DATA_PATH + stp.USR + '_mbz.csv')
cntryFreq = aux.getCountryFrequencies(data, stp.CNTRY_FIX)
aux.writeFrequencyDictToCSV(stp.STAT_PATH + 'CTR_FRQ.csv', cntryFreq)

##############################################################################
# Explore
##############################################################################
set(cntry)
filter = (data['Geo_1'] == "Suomi")
data[filter]
cntry = [x for x in list(data['MB_Geo1']) if str(x) != 'nan']
cntryClean = [stp.CNTRY_FIX.get(n, n) for n in cntry]
set(cntryClean)
cntryFreq
