import requests

def get_station_coordinates(station_name):
    query = f"""
    [out:json];
    node["railway"="station"]["name"="{station_name}"];
    out;
    """
    response = requests.get(f"http://overpass-api.de/api/interpreter?data={query}")
    data = response.json()
    if data['elements']:
        station = data['elements'][0]
        return (station['lat'], station['lon'])
    else:
        return None