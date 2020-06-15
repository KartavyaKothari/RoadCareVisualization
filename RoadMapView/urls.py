from django.urls import path
from django.conf.urls import url
from . import views
from .views import RoadView , nearest_road ,nearest_road_same_direction,get_roads_from_db,get_potholes_from_db

urlpatterns = [
    path('', RoadView.as_view(), name='showroad'),
    path('nearest_road_direction', nearest_road_same_direction, name='showroad'),
    path('nearest_road', nearest_road, name='showroad'),
    url(r'show/get_roads_from_db',get_roads_from_db),
    url(r'show/get_potholes_from_db',get_potholes_from_db)
]