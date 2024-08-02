from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Location
from .serializers import LocationSerializer
import json
import requests
import polyline
import folium
from django.utils.dateparse import parse_date


@csrf_exempt
def manage_location(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            latitude = data.get('latitude')
            longitude = data.get('longitude')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not name or not latitude or not longitude:
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            # Create a new location entry
            location = Location(name=name, latitude=latitude, longitude=longitude)
            location.save()
            return JsonResponse({'success': 'Location added successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)
    

@csrf_exempt
def get_all_locations(request):
    if request.method == 'GET':
        locations = Location.objects.all()
        location_data = [
            {
                'name': loc.name,
                'latitude': loc.latitude,
                'longitude': loc.longitude
               
            }
            for loc in locations
        ]
        return JsonResponse(location_data, safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


def map_view(request):
    locations = Location.objects.all()
    if not locations:
        # If there are no locations, render an empty map
        map = folium.Map(location=[0, 0], zoom_start=2)
    else:
        # Center map on the first location
        first_location = locations[0]
        map = folium.Map(location=[first_location.latitude, first_location.longitude], zoom_start=7)

        latlngs = []
        for loc in locations:
            latitude = float(loc.latitude)
            longitude = float(loc.longitude)
            folium.Marker([latitude, longitude], popup=loc.name).add_to(map)
            latlngs.append([latitude, longitude])

        if latlngs:
            folium.PolyLine(latlngs, color='blue', weight=5, opacity=0.7).add_to(map)
            # Add markers for the start and end points
            folium.Marker(latlngs[0], popup='Start', icon=folium.Icon(color='green')).add_to(map)
            folium.Marker(latlngs[-1], popup='End', icon=folium.Icon(color='red')).add_to(map)
            map.fit_bounds(latlngs)

    map_html = map._repr_html_()
    return render(request, 'location_map/map.html', {'map_html': map_html})


def filtered_map_view(request):
    date_str = request.GET.get('date')
    locations = []

    if date_str:
        date = parse_date(date_str)
        locations = Location.objects.filter(created_at__date=date)

    if not locations:
        # If there are no locations for the selected date, render an empty map
        map = folium.Map(location=[0, 0], zoom_start=2)
    else:
        # Center map on the first location
        first_location = locations[0]
        map = folium.Map(location=[first_location.latitude, first_location.longitude], zoom_start=7)

        latlngs = []
        for loc in locations:
            latitude = float(loc.latitude)
            longitude = float(loc.longitude)
            folium.Marker([latitude, longitude], popup=loc.name, icon=folium.Icon(color='blue')).add_to(map)
            latlngs.append([latitude, longitude])

        if latlngs:
            folium.PolyLine(latlngs, color='red', weight=5, opacity=0.7).add_to(map)
            # Add markers for the start and end points
            folium.Marker(latlngs[0], popup='Start', icon=folium.Icon(color='green')).add_to(map)
            folium.Marker(latlngs[-1], popup='End', icon=folium.Icon(color='red')).add_to(map)
            map.fit_bounds(latlngs)

    map_html = map._repr_html_()
    return render(request, 'location_map/filtered_map.html', {'map_html': map_html, 'date_str': date_str})


def get_route(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    loc = "{},{};{},{}".format(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
    url = "http://router.project-osrm.org/route/v1/driving/"
    r = requests.get(url + loc) 
    if r.status_code != 200:
        return {}
    
    res = r.json()
    routes = polyline.decode(res['routes'][0]['geometry'])
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
    distance = res['routes'][0]['distance']
    
    out = {
        'route': routes,
        'start_point': start_point,
        'end_point': end_point,
        'distance': distance
    }

    return out


def showmap(request):
    locations = Location.objects.all()
    locations_data = [
        {'name': loc.name, 'latitude': float(loc.latitude), 'longitude': float(loc.longitude)}
        for loc in locations
    ]
    context = {'locations': json.dumps(locations_data)}
    return render(request, 'location_map/showmap.html', context)


def showroute(request, lat1, long1, lat2, long2):
    lat1, long1, lat2, long2 = float(lat1), float(long1), float(lat2), float(long2)
    route = get_route(long1, lat1, long2, lat2)
    
    m = folium.Map(location=[(lat1 + lat2) / 2, (long1 + long2) / 2], zoom_start=10)
    
    folium.PolyLine(route['route'], weight=8, color='blue', opacity=0.6).add_to(m)
    folium.Marker(location=route['start_point'], icon=folium.Icon(icon='play', color='green')).add_to(m)
    folium.Marker(location=route['end_point'], icon=folium.Icon(icon='stop', color='red')).add_to(m)
    
    m = m._repr_html_()  # Render the map in HTML
    context = {'map': m}
    
    return render(request, 'location_map/showroute.html', context)