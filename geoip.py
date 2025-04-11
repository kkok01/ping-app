import geoip2.database
import os

def get_country(ip):
    try:
        with geoip2.database.Reader("/app/GeoLite2-Country.mmdb") as reader:
            response = reader.country(ip)
            return response.country.name
    except:
        return "Unknown"