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
BASE_PATH = '/home/chipdelmal/Documents/LastfmViz/'
# BASE_PATH = '/Users/sanchez.hmsc/odrive/Mega/LastfmViz/'
(DATA_PATH, STAT_PATH, IMG_PATH, FONT_PATH, GIS_PATH, MSK_PATH) = (
        BASE_PATH + 'data/',
        BASE_PATH + 'stats/',
        BASE_PATH + 'img/',
        BASE_PATH + 'fonts/',
        BASE_PATH + 'gis/',
        BASE_PATH + 'msk/'
    )
FONT = FONT_PATH + 'Prompt-Thin.ttf'
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
cdict = {
        'red':   [(0.0, 1, 1), (0.6, .8, .8), (.85, 0.75, 0.75), (1.0,  .50, .50)],
        'green': [(0.0, 1, 1), (0.6, .8, .8), (.85, 0.450, 0.450), (1.0,  .5, .5)],
        'blue':  [(0.0, 1, 1), (0.6, .8, .8), (.85, 0.750, 0.750), (1.0,  .80, .80)]
    }
cMapW = LinearSegmentedColormap('WB', cdict, N=256)
# https://www.schemecolor.com/united-kingdom-uk-flag-colors.php
cdict = {
        'red':   [(0.0, .8, .8),    (0.2, .8, .8),     (0.25,  1, 1),    (0.5, 1, 1),   (0.8,  1, 1),   (.85,  0, 0),           (1.0,  0, 0)],
        'green': [(0.0, .08, .08),  (0.2,  .08, .08),  (0.25,  1, 1),    (0.5, 1, 1),   (0.8,  1, 1),   (.85,  0.15, 0.15),    (1.0,  0.15, 0.15)],
        'blue':  [(0.0, .17, .17),  (0.2, .17, .17),   (0.25,  1, 1),    (0.5, 1, 1),   (0.8,  1, 1),   (.85,  .5, .5),         (1.0,  .5, .5)]
    }
cMapUK = LinearSegmentedColormap('WB', cdict, N=256)
# https://www.schemecolor.com/united-states-of-america-flag-colors.php
cdict = {
        'red':   [(0.0, .7, .7),    (0.2, .7, .7),     (0.35,  1, 1),    (0.5,  1, 1),   (0.75,  1, 1),   (.9, .23, .23),   (1.0,  .23, .23)],
        'green': [(0.0,  .13, .13), (0.2,  .13, .13),  (0.35,  1, 1),    (0.5, 1, 1),    (0.75,  1, 1),   (.9, .23, .23),   (1.0,  .23, .23)],
        'blue':  [(0.0, .2, .2),  (0.2, .2, .2),   (0.35,  1, 1),    (0.5,  1, 1),   (0.75,  1, 1),   (.9, .43, .43),   (1.0,  .43, .43)]
    }
cMapUS = LinearSegmentedColormap('WB', cdict, N=256)
# https://www.schemecolor.com/canada-flag-colors.php
cdict = {
        'red':   [(0, 1, 1), (0.425, 1, 1), (0.575,  1, 1), (1,  1, 1)],
        'green': [(0, 0, 0), (0.425, 0, 0), (0.575,  1, 1), (1,  1, 1)],
        'blue':  [(0, 0, 0), (0.425, 0, 0), (0.575,  1, 1), (1,  1, 1)]
    }
cMapCAN = LinearSegmentedColormap('WB', cdict, N=256)
# https://www.schemecolor.com/australia-flag-colors.php
cdict = {
        'red':   [(0, 1, 1), (0.1, 1, 1), (0.3,  1, 1), (0.5,  1, 1),   (0.7,  1, 1), (.9, 0, 0), (1,  0, 0)],
        'green': [(0, 0, 0), (0.1, 0, 0), (0.3,  1, 1), (0.5,  1, 1),   (0.7,  1, 1), (.9, 0, 0), (1,  0, 0)],
        'blue':  [(0, 0, 0), (0.1, 0, 0), (0.3,  1, 1), (0.5,  1, 1),   (0.7,  1, 1), (.9, .54, .54), (1, .54, .54)]
    }
cMapAUS = LinearSegmentedColormap('WB', cdict, N=256)
[i / 256 for i in (0, 0, 0)]
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
    'Desiree Schell & K.O. Myers', 'Rebecca Watson', 'Starcraft',
    'Chicago Public Media', 'throughlinegroup.com', 'undefinedRadiohead',
    'throughlinegroup.com', 'moviepilot', 'Mario Galaxy Orchestra', 
    'NPR', 'Portal', 'Seu Jorge', 'Ana Carolina', 'MishCatt', 
    'Alexandre Desplat', 'Science of Sleep', 'Robert Schumann',
    'Charles Darwin', 'Stanislaw Lem', 'Moviepilot Supernews',
    'undefinedPixies', 'undefinedRyan Adams', 'undefinedWilco',
    
    'Mägo de Oz', 'David Summers', 
    'Rata Blanca',  'Hombres G', 'Mecano', 'Ramon Mirabet',
    'Pereza', 
    'El Tri', 'Café Tacvba', 'Caifanes', 'Nacha Pop', 
    'Maldita Vecindad Y Los Hijos Del Quinto Patio', 'Enanitos Verdes',
    'Soda Stereo', 'Los Prisioneros', 'Bacilos', 'Alaska y Dinarama', 
    'Duncan Dhu', 'Hello Seahorse!', 'Miguel Mateos', 'Los Enanitos Verdes'

    'Elliott Smith', 
])
##############################################################################
# Countries corrections
##############################################################################
CNTRY_FIX = {
        'United States of America': 'United States',
        'New Zealand / Aotearoa': 'Australia',
        'New Zealand': 'Australia',
        'Ireland': 'United Kingdom'
    }
CNTRY_ALIAS = {
        'CAN': {'Canada', 'CA'},
        'US': {'United States of America', 'United States', 'US'},
        'UK': {'United Kingdom', 'Ireland', 'UK'},
        'AUS': {'Australia', 'New Zealand', 'New Zealand / Aotearoa', 'AU'},
        'RST': {
                'Sverige', 'Ísland',# 'Australia',
                'Danmark', 'Canada', 'Deutschland',
                'Norge', 'New Zealand', 'Argentina', #'New Zealand / Aotearoa',
                'Suomi', 'Nederland', 'Россия', 'Slovensko'
            },
        'WLD': {
                'Sverige', 'Ísland', 'Australia',
                'Danmark', 'Canada', 'Deutschland',
                'Norge', 'New Zealand', 'Argentina', 'New Zealand / Aotearoa',
                'Suomi', 'Nederland', 'Россия', 'Slovensko'
            }
    }
CNTRY_BOX = {
        'US': [-126, 24, -65, 50],
        'UK': [-8.6500072, 49.863187, 1.7632199, 58.75],
        'CAN': [-141.00686645507812, 41.67692565917997, -52.62, 70],
        'AUS': [112.92, -39.2, 155, -9.22],
        'NZL': [185, -49, 179.06582641601568, -30]
    }
CNTRY_CODE = {
        'UK': ('United Kingdom', cMapUK, 'HACKED.ttf'),
        'DNK': 'Danmark',
        'US': ('United States', cMapUS, 'Howdoyousleep.ttf'),
        'CAN': ('Canada', cMapCAN, 'FEENC.ttf'),
        'SWE': 'Sverige',
        'AUS': ('Australia', cMapAUS, 'danger.otf'),
        'NZL': ('New Zealand', cMapAUS, 'URGHTYPEPERSONALUSE.otf'),
        'RST': ('World', cMapW, 'Friday Lovers.otf'),
        'WLD': ('World', cMapW, 'Friday Lovers.otf')
    }
