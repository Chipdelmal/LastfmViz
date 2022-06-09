#!/bin/bash

python Lastfm_clean.py
python MusicBrainz_download.py

python artistFreq.py 2012 1 2013 1
python artistFreq.py 2013 1 2014 1
python artistFreq.py 2014 1 2015 1 
python artistFreq.py 2015 1 2016 1 
python artistFreq.py 2016 1 2017 1 
python artistFreq.py 2017 1 2018 1 
python artistFreq.py 2018 1 2019 1 
python artistFreq.py 2019 1 2020 1 
python artistFreq.py 2020 1 2021 1 
python artistFreq.py 2021 1 2022 1 
python artistFreq.py 2022 1 2023 1 

# python artistFreq.py 2012 1 2023 1 