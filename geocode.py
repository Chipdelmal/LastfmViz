
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="lastfm")
location = geolocator.geocode("175 5th Avenue NYC")
print(location.latitude, location.longitude, location.address)
