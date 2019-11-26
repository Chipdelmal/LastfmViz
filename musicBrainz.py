import keys
import musicbrainzngs as mb


mb.auth(keys.MB_USR, keys.MB_PSW)
mb.set_useragent("lastfm", "0.1", "http://chipdelmal.github.io")
mb.search_release_groups("Lucky Soul", type="group")
