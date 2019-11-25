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

##############################################################################
# Setup PATHs
##############################################################################
USR = 'chipmaligno'
BASE_PATH = '/Users/sanchez.hmsc/Documents/GitHub/lastfmViz/'
(DATA_PATH, STAT_PATH, IMG_PATH) = (
        BASE_PATH + 'data/',
        BASE_PATH + 'stats/',
        BASE_PATH + 'img/'
    )

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
        'Fraser Cain & Dr. Pamela Gay', 'Hombres G', 'Mecano'
    ])
