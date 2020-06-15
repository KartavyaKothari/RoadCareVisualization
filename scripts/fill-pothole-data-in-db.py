import os,django
import json

from RoadMapView.models import RoadPothole,RoadPoint,RoadPothole_snapped
from django.contrib.gis.geos import Point
from datetime import datetime, timedelta
import pandas as pd

from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

def run():
    # Delete previous data
    RoadPothole.objects.all().delete()

    last_one_week_data = pd.read_json('tmp/last_one_week_data.json')

    for row in last_one_week_data.iterrows():
        # print(row[0])
        rating = 0
        pothole = RoadPothole(point=Point(row[1]['lng'],row[1]['lat']),rating=rating,bearing=row[1]['bearing'])
        pothole.save()

    print(len( RoadPothole.objects.all()))