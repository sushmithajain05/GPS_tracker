
from .views import get_all_locations,filtered_map_view, manage_location, map_view,showmap,showroute
from django.urls import path


urlpatterns = [
    path('manage_location/', manage_location, name='manage_location'),
    path('get_all_locations/', get_all_locations, name='get_all_locations'),
    path('showmap/', showmap, name='showmap'),
    path('showroute/<str:lat1>/<str:long1>/<str:lat2>/<str:long2>/', showroute, name='showroute'),

    path('map/', map_view, name='map_view'),  
    path('filtered_map/', filtered_map_view, name='filtered_map'),
    
]


