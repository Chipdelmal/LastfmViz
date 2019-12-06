##############################################################################
#  _           _    __           _   _ _
# | |         | |  / _|         | | | (_)
# | | __ _ ___| |_| |_ _ __ ___ | | | |_ ____
# | |/ _` / __| __|  _| '_ ` _ \| | | | |_  /
# | | (_| \__ \ |_| | | | | | | \ \_/ / |/ /
# |_|\__,_|___/\__|_| |_| |_| |_|\___/|_/___|
#
# ----------------------------------------------------------------------------
# Setting up paths and other globals
##############################################################################


from matplotlib.colors import LinearSegmentedColormap
# from matplotlib.colors import ListedColormap

##############################################################################
# Setup PATHs
##############################################################################
USR = 'chipmaligno'
BASE_PATH = '/Users/sanchez.hmsc/odrive/sanchez.hmsc@berkeley.edu/lastfmViz/'
(DATA_PATH, STAT_PATH, IMG_PATH, FONT_PATH, GIS_PATH) = (
        BASE_PATH + 'data/',
        BASE_PATH + 'stats/',
        BASE_PATH + 'img/',
        BASE_PATH + 'fonts/',
        BASE_PATH + 'gis/'
    )
FONT = FONT_PATH + 'ARCADE.ttf'
(TOP_GENRES, GEO_SIZE, TIMEZONE) = (3, 6, 'US/Pacific')
##############################################################################
# Color palette
##############################################################################
cdict = {
        'red':   [(0.0, 1, 1), (0.5,  0.85, 0.85), (1.0,  0.5, 0.5)],
        'green': [(0.0,  1, 1), (0.5, 0.85, 0.85), (1.0,  0.5, 0.5)],
        'blue':  [(0.0, 1, 1), (0.5,  0.85, 0.85), (1.0,  .9, .9)]
    }
# https://www.schemecolor.com/united-kingdom-uk-flag-colors.php
cMap = LinearSegmentedColormap('WB', cdict, N=256)
cdict = {
        'red':   [(0.0, .8, .8),    (0.1, .8, .8),     (0.25,  1, 1),    (0.5, 1, 1),   (0.75,  1, 1),   (.9,  0, 0),           (1.0,  0, 0)        ],
        'green': [(0.0, .08, .08), (0.1,  .08, .08),  (0.25,  1, 1),    (0.5, 1, 1),    (0.75,  1, 1),   (.9,  0.15, 0.15),    (1.0,  0.15, 0.15)  ],
        'blue':  [(0.0, .17, .17),  (0.1, .17, .17),   (0.25,  1, 1),    (0.5, 1, 1),   (0.75,  1, 1),   (.9,  .5, .5),         (1.0,  .5, .5)       ]
    }
cMapUK = LinearSegmentedColormap('WB', cdict, N=256)
# https://www.schemecolor.com/united-states-of-america-flag-colors.php
cdict = {
        'red':   [(0.0, .7, .7),    (0.1, .7, .7),     (0.25,  1, 1),    (0.5,  1, 1),   (0.75,  1, 1),   (.9, .23, .23),   (1.0,  .23, .23)],
        'green': [(0.0,  .13, .13), (0.1,  .13, .13),  (0.25,  1, 1),    (0.5, 1, 1),    (0.75,  1, 1),   (.9, .23, .23),   (1.0,  .23, .23)],
        'blue':  [(0.0, .2, .2),  (0.1, .2, .2),   (0.25,  1, 1),    (0.5,  1, 1),   (0.75,  1, 1),   (.9, .43, .43),   (1.0,  .43, .43)]
    }
cMapUS = LinearSegmentedColormap('WB', cdict, N=256)
[i / 256 for i in (0, 36, 125)]

##############################################################################
# Ban list: Artists excluded from the analyses
##############################################################################
BAN = set([
        'Aperture Science Psychoacoustics Laboratory',
        'Band Of Horses?i', "Chip's iTouch", 'Chïp',
        'Crossroads Guitar Festival', 'Douglas Adams',
        'Dr. Steven Novella', 'El Explicador', 'El Explicador - XEITE',
        'El trío de tres', 'Enrique Ganem y María de los Ángeles Aranda',
        'Franco De Vita', 'Fuster', 'G3', 'Hombres G Con Ha-ash',
        'Howstuffworks.com', 'Live Aid', 'Love Album', 'Abril',
        'Koji Kondo/Mahito Yokota/Toru Minegishi/Yasuaki Iwata',
        'Mass Effect', 'Michael Bublé', 'Nature Publishing Group',
        'Rock En Tu Idioma', 'SGU Productions', 'Startalk radio',
        "The Skeptics' Guide to the Universe", '[unknown]', 'chipdelmal',
        'dawsons creek', 'iHeartRadio & HowStuffWorks', 'XTC',
        'Fraser Cain & Dr. Pamela Gay', 'Mychael Danna & Rob Simonsen'
        'Chicago Public Media', 'Rebecca Watson of Curiosity Aroused',
        'Desiree Schell & K.O. Myers', 'Rebecca Watson', 'Mägo de Oz',
        'David Summers', 'Stanislaw Lem', 'MishCatt', 'NPR', 'Portal',
        'Rata Blanca', 'Starcraft', 'Hombres G', 'Mecano', 'Ramon Mirabet',
        'Pereza', 'Ana Carolina', 'Seu Jorge', 'Hello Seahorse!',
        'Alexandre Desplat', 'Science of Sleep', 'Robert Schumann',
        'Charles Darwin'
    ])
##############################################################################
# Countries corrections
##############################################################################
CNTRY_FIX = {
        'United States of America': 'United States',
        'New Zealand / Aotearoa': 'New Zealand',
        'Ireland': 'United Kingdom'
    }
CNTRY_BOX = {
        'US': [-126, 24, -65, 50],
        'UK': [-8.6500072, 49.863187, 1.7632199, 58.75],
        'CAN': [-141.00686645507812, 41.67692565917997, -52.61888885498027, 70]
    }
CNTRY_CODE = {
        'UK': ('United Kingdom', cMapUK, 'EarthKid'),
        'DNK': 'Danmark',
        'US': ('United States', cMapUS, 'Howdoyousleep'),
        'CAN': ('Canada', cMap, 'ABEAKRG'),
        'SWE': 'Sverige'
    }
