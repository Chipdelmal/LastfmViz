#!/bin/bash


MSK='False'
# Clean the Lastfm dataset ----------------------------------------------------
python Lastftm_clean.py
# Download geocode data from musicbrainz --------------------------------------
python MusicBrainz_download.py
# Generate map masks ----------------------------------------------------------
if [[ "$MSK" = "True" ]]; then
    python Map_mask.py 'AUS'
    python Map_mask.py 'CAN'
    python Map_mask.py 'UK'
    python Map_mask.py 'US'
fi
# Generate wordclouds ---------------------------------------------------------
python Wordcloud_Masked.py 'RST'
python Wordcloud_Masked.py 'US'
python Wordcloud_Masked.py 'UK'
python Wordcloud_Masked.py 'AUS'
python Wordcloud_Masked.py 'CAN'
