import os,django
import json

from django.contrib.gis.geos import Point
from datetime import datetime, timedelta
import pandas as pd

from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

def getRating(data_t):
    a = data_t['p_bad']
    b = data_t['p_medium']
    c = data_t['p_good']

    if a>b:
        if a>c:
            return 1
        else: 
            return 3
    else:
        if b>c:
            return 2
        else:
            return 3 

def run():
    # Delete previous data
    RoadPothole.objects.all().delete()

    last_one_week_data = pd.read_json('tmp/last_one_week_data.json')

    for row in last_one_week_data.iterrows():
        # print(row[0])
        rating = getRating(row[1])
        # print(rating)
        pothole = RoadPothole(point=Point(row[1]['lng'],row[1]['lat']),rating=rating,bearing=row[1]['bearing'])
        pothole.save()
        
    print(len( RoadPothole.objects.all()))