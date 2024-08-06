from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date
from .models import Location
from .serializers import LocationSerializer
import json
import requests
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignupForm, LoginForm
from django.contrib import messages
from django.urls import reverse

def HomePage(request):
    return render(request,'location_map/home.html')
def NavPage(request):
    return render(request,'location_map/navbar.html')
def mapPage(request):
    return render(request,'location_map/maps.html')

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
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            if not username:
                form.add_error('username', 'Username is required.')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect(reverse('login'))  # Redirect to the login page

        return render(request, 'location_map/signup.html', {'form': form})
    else:
        form = SignupForm()
        return render(request, 'location_map/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('add_loc'))  # Ensure 'add_loc' is the name of your URL pattern for adding locations
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'location_map/login.html', {'form': form})

def loc_add(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        latitude = request.POST.get("latitude")
        longitude = request.POST.get("longitude")

        if name and latitude and longitude:
            l = Location(name=name, latitude=latitude, longitude=longitude)
            l.save()
            return redirect("table")  # Ensure 'table' is the name of your URL pattern for the target page
        else:
            # Handle the case where one of the fields is missing
            return render(request, "location_map/add_loc.html", {"error": "All fields are required."})

    return render(request, "location_map/add_loc.html")


def ListPage(request):
    loc=Location.objects.all()
    return render(request,"location_map/table.html",{'loc':loc})




def get_route(start, end):
    url = f"http://router.project-osrm.org/route/v1/driving/{start[1]},{start[0]};{end[1]},{end[0]}?overview=full&geometries=polyline"
    response = requests.get(url)
    data = response.json()
    if data.get('routes'):
        return data['routes'][0]['geometry']
    return None


def map_view(request):
    date_str = request.GET.get('date')
    locations = []

    if date_str:
        date = parse_date(date_str)
        locations = Location.objects.filter(created_at__date=date)
    else:
        locations = Location.objects.all()

    location_data = [
        {
            'name': loc.name,
            'latitude': float(loc.latitude),
            'longitude': float(loc.longitude)
        }
        for loc in locations
    ]
    routes = []
    if len(location_data) > 1:
        for i in range(len(location_data) - 1):
            start = (location_data[i]['latitude'], location_data[i]['longitude'])
            end = (location_data[i + 1]['latitude'], location_data[i + 1]['longitude'])
            route = get_route(start, end)
            if route:
                routes.append(route)

    no_data = len(location_data) == 0

    return render(request, 'location_map/map.html', {'locations': location_data, 'routes': routes, 'date_str': date_str, 'no_data': no_data})

def filtered_map_view(request):
    date_str = request.GET.get('date')
    locations = []

    if date_str:
        date = parse_date(date_str)
        locations = Location.objects.filter(created_at__date=date)

    location_data = [
        {
            'name': loc.name,
            'latitude': float(loc.latitude),
            'longitude': float(loc.longitude)
        }
        for loc in locations
    ]
    routes = []
    if len(location_data) > 1:
        for i in range(len(location_data) - 1):
            start = (location_data[i]['latitude'], location_data[i]['longitude'])
            end = (location_data[i + 1]['latitude'], location_data[i + 1]['longitude'])
            route = get_route(start, end)
            if route:
                routes.append(route)

    no_data = len(location_data) == 0

    return render(request, 'location_map/filtered_map.html', {'locations': location_data, 'routes': routes, 'date_str': date_str, 'no_data': no_data})









