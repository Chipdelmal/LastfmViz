
from sys import argv
from os import path
import numpy as np
import pandas as pd
import pickle as pkl
from datetime import timedelta
import matplotlib.pyplot as plt
from quantecon import MarkovChain
from collections import Counter
import aux as aux
import setup as stp

if aux.isnotebook():
    (TOP, WRAN, ID) = (150, 5, 'C') 
else:
    (TOP, WRAN, ID) = (int(argv[1]), int(argv[2]), argv[3])
T_THRESHOLD = timedelta(minutes=60)
###############################################################################
# Read Data
###############################################################################
DTA_CLN = pd.read_csv(path.join(stp.DATA_PATH, stp.USR+'_fxd.csv'), parse_dates=[3])
DTA_MBZ = pd.read_csv(path.join(stp.DATA_PATH, stp.USR+'_mbz.csv'))          
###############################################################################
# Setup Structures
###############################################################################
arts = sorted(list(DTA_CLN['Artist'].unique()))
(artsNum, playNum) = (len(arts), DTA_CLN.shape[0])
artsCount = DTA_CLN.groupby('Artist').size().sort_values(ascending=False)
###############################################################################
# Filter Top
###############################################################################
artsTop = list(artsCount.index)[:TOP]
artsTopSet = set(artsTop)
###############################################################################
# Iterate Through Plays (Generate Transitions Matrix)
###############################################################################
tMat = aux.calcWeightedTransitionsMatrix(
    DTA_CLN, artsTop, windowRange=(1, WRAN), 
    timeThreshold=T_THRESHOLD, verbose=True
)
markovMat = aux.normalizeMatrix(tMat)
###############################################################################
# Get Song Counts
###############################################################################
art = artsTop[0]
artsSongDict = {}
for art in artsTop:
    songPlays = list(DTA_CLN[DTA_CLN['Artist']==art]['Song'])
    songCounts = Counter(songPlays)
    counts = np.array(list(songCounts.values()))
    countsNormalized = counts/sum(counts)
    countsDict = {s:n for (s, n) in zip(list(songCounts.keys()), countsNormalized)}
    artsSongDict[art] = countsDict
###############################################################################
# Markov
###############################################################################
mc = MarkovChain(markovMat, state_values=artsTop)
ss = mc.stationary_distributions[0]
ssPrint = ['{}: {}'.format(a, p) for (a, p) in zip(artsTop, ss)]
###############################################################################
# Simulate Trace
###############################################################################
songsNumber = 15
sChain = mc.simulate(ts_length=songsNumber, init='Caamp')
# Generate a random playlist --------------------------------------------------
playlist = []
ca = sChain[0]
for ca in sChain:
    (songs, probs) = (
        list(artsSongDict[ca].keys()), 
        list(artsSongDict[ca].values())
    )
    if len(songs) > 0:
        six = np.random.choice(len(probs), 1, p=probs)[0]
        playlist.append((ca, songs[six]))
        # Remove from the pool for no repetitions -----------------------------
        songs.pop(six); probs.pop(six)
        normProbs = np.asarray(probs)/sum(probs)
        artsSongDict[ca]= {s:p for (s, p) in zip(songs, normProbs)}
playlist




