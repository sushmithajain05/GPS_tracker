import requests
import json
import polyline
import folium
#for onclick map
def get_route1(waypoints):
    loc = ';'.join([f"{lon},{lat}" for lat, lon in waypoints])
    url = f"http://router.project-osrm.org/route/v1/driving/{loc}"
    params = {
        'overview': 'full',
        'geometries': 'polyline'
    }
    r = requests.get(url, params=params)
    if r.status_code != 200:
        return {}
    res = r.json()
    routes = polyline.decode(res['routes'][0]['geometry'])
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    end_point = [res['waypoints'][-1]['location'][1], res['waypoints'][-1]['location'][0]]
    distance = res['routes'][0]['distance']

    out = {
        'route': routes,
        'start_point': start_point,
        'end_point': end_point,
        'distance': distance
    }

    return out