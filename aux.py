##############################################################################
#  _           _    __           _   _ _
# | |         | |  / _|         | | | (_)
# | | __ _ ___| |_| |_ _ __ ___ | | | |_ ____
# | |/ _` / __| __|  _| '_ ` _ \| | | | |_  /
# | | (_| \__ \ |_| | | | | | | \ \_/ / |/ /
# |_|\__,_|___/\__|_| |_| |_| |_|\___/|_/___|
#
# ----------------------------------------------------------------------------
# Functions definitions
##############################################################################
import keys
import csv
import setup as stp
import musicbrainzngs as mb
from collections import Counter
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from mpl_toolkits.basemap import Basemap
geolocator = Nominatim(user_agent=keys.GEO_USR)


def doGeocode(address):
    """Recursive function to geocode whilst handling timeout exception.

    Parameters
    ----------
    address : string
        String of the address that needs to be geocoded.

    Returns
    -------
    type
        Geocode information.

    """
    try:
        return geolocator.geocode(address)
    except (GeocoderTimedOut):
        return doGeocode(address)


def geocodeEntries(info):
    """Handles the geocoding info from the MusicBrainz database.

    Parameters
    ----------
    info : tuple
        Lastfm geocode triplet: (_, country, city)

    Returns
    -------
    list
        Returns the list of the geocoded entry (lat, long, address), and pads
        entries with no available information.

    """
    (tmp, p1, p2) = (info, info[1], info[2])
    if p1 is None:
        p1 = ''
    if p2 is None:
        p2 = ''
    location = doGeocode(p1 + ' ' + p2)
    if location is None:
        tmp.extend(stp.GEO_SIZE * [None])
    else:
        tmp.extend([location.latitude, location.longitude])
        gcList = [i.strip() for i in location.address.split(',')]
        gcList.reverse()
        tmp.extend(padList(gcList, stp.GEO_SIZE))
    return tmp


def getArtistInfo(artist, topGenres=3):
    srch = mb.search_artists(artist=artist).get('artist-list')
    if len(srch) > 0:
        info = mb.search_artists(artist=artist).get('artist-list')[0]
        (id, name, country, city, genre) = (
                info.get('id'), info.get('name'), info.get('country'),
                getArea(info), getTopGenres(info, topGenres=topGenres)
            )
        tmp = [name, country, city, id]
        tmp.extend(genre)
        return tmp
    else:
        tmp = [artist, None, None, None]
        tmp.extend(topGenres * [None])
        return tmp


def padList(lst, n):
    lst.extend([None] * n)
    lst = lst[:n]
    return lst


def getTopGenres(info, topGenres=3):
    tags = info.get('tag-list')
    # Check that genres are available
    if tags is not None:
        lst = []
        for i in info.get('tag-list'):
            lst.append((int(i.get('count')), i.get('name')))
        lst.sort(reverse=True)
        # Check that there are enough tags and pad with None
        if (len(lst) >= topGenres):
            return [i[1] for i in lst[0:topGenres]]
        else:
            tmp = [i[1] for i in lst[0:len(lst)]]
            return padList(tmp, topGenres)
    else:
        return [None] * topGenres


def getArea(info):
    area = info.get('begin-area')
    if area is not None:
        city = area.get('name')
        if city is not None:
            return city
    else:
        return None


def generateMBHeader(topGenres, geoSize):
    partA = ['Artist', 'MB_Geo1', 'MB_Geo2', 'MB_Hash']
    gnrPad = ['Gen_' + str(i) for i in range(1, topGenres + 1)]
    geoPad = ['Geo_' + str(i) for i in range(1, geoSize + 1)]
    partA.extend(gnrPad)
    partA.extend(['Lat', 'Lon'])
    partA.extend(geoPad)
    return partA


def createBasemapInstance(minLat, maxLat, minLon, maxLon, pad=1.5):
    base = Basemap(
            projection='merc',
            lat_0=(maxLat - minLat)/2, lon_0=(maxLon - minLon)/2,
            resolution='l', area_thresh=0.1,
            llcrnrlon=minLon - pad, llcrnrlat=minLat - pad,
            urcrnrlon=maxLon + pad, urcrnrlat=maxLat + pad,
            epsg=4269
        )
    return base


def rescaleRGBA(colorsTuple, colors=255):
    return [i/colors for i in colorsTuple]


def writeFrequencyDictToCSV(path, countryDict):
    with open(path, 'w') as f:
        for key in countryDict.keys():
            f.write("%s,%s\n" % (key, countryDict[key]))


def getCountryFrequencies(mbzData, countryFix, label='Geo_1'):
    cntry = [x for x in list(mbzData[label]) if str(x) != 'nan']
    cntryClean = [countryFix.get(n, n) for n in cntry]
    cntryFreq = dict(Counter(cntryClean))
    return cntryFreq


def removeBanned(lastfmData, label='Artist'):
    return lastfmData[~lastfmData[label].isin(stp.BAN)]


def getPlaycount(clnData, label='Artist'):
    artistCount = clnData.groupby(label).size().sort_values(ascending=False)
    return artistCount


def parseFromMusicbrainz(clnData):
    artists = sorted(clnData['Artist'].unique())
    artNum = len(artists)
    # Generate output path
    FILE_PATH = stp.DATA_PATH + stp.USR
    # print('Parsing from musicbranz!\n')
    with open(FILE_PATH + '_mbz.csv', mode='w') as mbFile:
        mbWriter = csv.writer(mbFile, quoting=csv.QUOTE_MINIMAL)
        header = generateMBHeader(stp.TOP_GENRES, stp.GEO_SIZE)
        mbWriter.writerow(header)
        with open(FILE_PATH + '_dbg.txt', 'w') as out:
            for (i, art) in enumerate(artists):
                # Parse musicbranz database
                info = getArtistInfo(art, topGenres=stp.TOP_GENRES)
                txt = '\t Parsed: {}/{}: {} [{} - {}]'.format(
                    str(i+1).zfill(3), str(artNum).zfill(3), 
                    art, info[0], info[1]
                )
                print(txt)
                info = geocodeEntries(info)
                mbWriter.writerow('{}, {}, {}'.format(art, info[0], info[1]))
                out.write(txt + '\n')
            # print('\t- Parsed: {0}/{1}'.format(i+1, artNum), end='\r')
    # print('Finished!                      ')
