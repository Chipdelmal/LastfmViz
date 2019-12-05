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
FONT = FONT_PATH + 'other/EarthKid.ttf'
(TOP_GENRES, GEO_SIZE, TIMEZONE) = (3, 6, 'US/Pacific')
##############################################################################
# Color palette
##############################################################################
cdict = {
        'red':   [(0.0, 1, 1), (0.5,  0.85, 0.85), (1.0,  0.5, 0.5)],
        'green': [(0.0,  1, 1), (0.5, 0.85, 0.85), (1.0,  0.5, 0.5)],
        'blue':  [(0.0, 1, 1), (0.5,  0.85, 0.85), (1.0,  .9, .9)]
    }
cMap = LinearSegmentedColormap('WB', cdict, N=256)
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
        'UK': [-8.6500072, 49.863187, 1.7632199, 60.8458677]
    }
CNTRY_CODE = {
        'DNK': 'Danmark',
        'US': 'United States',
        'CAN': 'Canada',
        'SWE': 'Sverige'
    }
