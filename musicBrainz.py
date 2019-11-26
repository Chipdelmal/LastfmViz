# import aux
import keys
import musicbrainzngs as mb


mb.auth(keys.MB_USR, keys.MB_PSW)
mb.set_useragent("lastfm", "0.1", "http://chipdelmal.github.io")

# artist_id = "c5c2ea1c-4bde-4f4d-bd0b-47b200bf99d6"
# result = mb.get_artist_by_id(artist_id)

artist = 'Radiohead'
info = mb.search_artists(artist=artist).get('artist-list')[0]
(id, name, country, genre) = (
        info.get('id'), info.get('name'), info.get('country'),
        aux.getTopGenres(info, top=3)
    )
print('{0}, {1}, {2}, {3}'.format(id, name, country, genre))
