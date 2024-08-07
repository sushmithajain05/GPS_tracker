
from .views import get_all_locations,filtered_map_view, manage_location, map_view,login_view,signup,loc_add,ListPage,NavPage,mapPage,showmap,showroute,map_polyline,map_polygon,logout_view,train_route_view,TrainStationListView,TrainStationCreateView,upload_file_view
from django.urls import path


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
  

    path('api/train-stations/', TrainStationListView.as_view(), name='train_station_list'),
    path('api/train-stations/add/', TrainStationCreateView.as_view(), name='train_station_create'),
    path('train_route/', train_route_view, name='train_route'),

    path('upload/', upload_file_view, name='upload_file'),



]

