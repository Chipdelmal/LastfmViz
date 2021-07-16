# [Last.fm](https://www.last.fm/) dataViz

**[Under development]**

1. Download your [Last.fm](https://www.last.fm/) history with: https://benjaminbenben.com/lastfm-to-csv/
2. Place your CSV file in the [data](./data) folder.
3. Change your paths and username in [setup](./setup.py).
4. Modify the *BAN* list in the [setup](./setup.py) file as needed.
5. Create a *keys.py* file with the following contents:

```
# Lastfm API Credentials
(API_KEY, SHRD_SECRT) = (API_KEY_STRING, API_SHARED_SECRET_STRING)
AUTH = 'AUTHOR_STRING'
# MusicBrainz agent
(MB_NM, MB_V, MB_URL) = (APP_NAME, APP_VER, APP_HOME)
(MB_USR, MB_PSW) = (MB_USER_STRING, MB_USER_PASSWORD)
# Geolocator
(GEO_USR) = (APP_NAME)
```

Inspired by: [Analyzing Last.fm Listening History](https://geoffboeing.com/2016/05/analyzing-lastfm-history/) by [gboeing](https://geoffboeing.com/author/geoff/).


<hr>

## Common Uses

### Artist Playcount Wordcloud

1. Run [Lastfm_clean](./Lastfm_clean.py).
2. Run [MusicBrainz_download](./MusicBrainz_download.py).
3. Download a country or region's [SHP file](https://gadm.org/download_country_v3.html) and place it in the gis folder.
3. Run [Map_mask.py](./Map_mask.py) with the country code.
4. Run [Wordcloud_Masked.py](./Wordcloud_masked.py) with the country code.


### Artist Masked Wordcloud


<hr>

##  Files

* [setup.py](./setup.py): Paths, username, and 'banned list' settings.
* [clean.py](./clean.py): Routines to clean up the database.
* [musicBrainz.py](./musicBrainz): Mixes the database with MB information on genres and geographies.

<hr>

## Author

<img src="./media/pusheen.jpg" height="130px" align="middle"><br>

[Héctor M. Sánchez C.](https://chipdelmal.github.io/)
