#!/bin/bash

# python Lastfm_clean.py
# python MusicBrainz_download.py

python PlayByHour_polar.py 2012 1 2013 1 "True"
python PlayByHour_polar.py 2013 1 2014 1 "True"
python PlayByHour_polar.py 2014 1 2015 1 "True"
python PlayByHour_polar.py 2015 1 2016 1 "True"
python PlayByHour_polar.py 2016 1 2017 1 "True"
python PlayByHour_polar.py 2017 1 2018 1 "True"
python PlayByHour_polar.py 2018 1 2019 1 "True"
python PlayByHour_polar.py 2019 1 2020 1 "True"
python PlayByHour_polar.py 2020 1 2021 1 "True"
python PlayByHour_polar.py 2021 1 2022 1 "True"
python PlayByHour_polar.py 2022 1 2023 1 "True"

python PlayByHour_polar.py 2012 8 2017 5 "False"
python PlayByHour_polar.py 2017 5 2023 10 "False"

python PlayByHour_polar.py 2012 8 2023 11 "False"