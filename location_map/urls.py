
from .views import get_all_locations,filtered_map_view, manage_location, map_view,login_view,signup,loc_add,ListPage,NavPage,mapPage,showmap,showroute,map_polyline,map_polygon,logout_view
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('manage_location/', manage_location, name='manage_location'),
    path('get_all_locations/', get_all_locations, name='get_all_locations'),
    path('location_map/map/', map_view, name='map_view'),
    path('location_map/filtered_map/', filtered_map_view, name='filtered_map_view'),
    path('', login_view, name='login'),
    path('signup/', signup, name='signup'),
   
    path('add_loc/',loc_add,name='add_loc'),
    path('table/',ListPage,name='table'),
    path('navbar', NavPage, name ='navbar'),
    path('maps/', mapPage, name ='maps'),
    path('map1/', showmap, name='showmap'),
    path('filtered_map1/', showroute, name='showroute'),
    path('polyline/', map_polyline, name='map_polyline'),
    path('polygon/', map_polygon, name='map_polygon'),
    path('logout/', logout_view, name='logout'),
  

]

