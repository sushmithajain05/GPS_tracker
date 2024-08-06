
from .views import get_all_locations,filtered_map_view, manage_location, map_view,login_view,signup,HomePage,loc_add,ListPage,NavPage,mapPage
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('manage_location/', manage_location, name='manage_location'),
    path('get_all_locations/', get_all_locations, name='get_all_locations'),
    path('location_map/map/', map_view, name='map_view'),
    path('location_map/filtered_map/', filtered_map_view, name='filtered_map_view'),
    path('login/', login_view, name='login'),
    path('signup/', signup, name='signup'),
    path('', HomePage, name='home'),
    path('add_loc/',loc_add,name='add_loc'),
    path('table/',ListPage,name='table'),
    path('navbar', NavPage, name ='navbar'),
    path('maps/', mapPage, name ='maps'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)