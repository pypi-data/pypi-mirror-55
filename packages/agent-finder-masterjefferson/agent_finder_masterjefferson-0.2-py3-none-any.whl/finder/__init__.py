
__version__ = "1.0.0"

import googlemaps
import os

gmaps = googlemaps.Client(key=os.environ['GOOGLE_MAPS_API_KEY'])


