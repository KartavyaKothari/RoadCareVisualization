import os,django
import json

from RoadMapView.models import RoadPothole,RoadData_snapped, RoadData
from django.contrib.gis.geos import Point
from datetime import datetime, timedelta
import pandas as pd

from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

# from django.db.transaction import commit_on_success
from django.db import transaction

import time
import numpy as np


@transaction.atomic
def run():
    # Delete previous data
    # RoadData_snapped.objects.all().delete()
    rp=RoadPothole.objects.all()

    # Seetting the nearest road api
    search_distance = 50

    for r in rp:
        input_pt = Point(r.point.x,r.point.y)

        # matched_points = RoadPoint.objects.filter(point__distance_lt=(input_pt,D(m=search_distance)))
        matched_points = RoadData_snapped.objects.filter(center__distance_lt=(input_pt,D(m=search_distance)))

        if len(matched_points) != 0:
            pothole = matched_points[0]
            pothole.rating = (pothole.rating*pothole.total_potholes+r.rating)/(pothole.total_potholes+1)
            pothole.total_potholes = pothole.total_potholes+1
            
            pothole.save()
    
    print(len(RoadData_snapped.objects.all()))
    # time_req = np.array(time_req)
    # print("Mean:",np.mean(time_req,axis=0)*1000,"(ms)"," Std:",np.std(time_req,axis=0)*1000,"(ms)")

    # multipoint = models.MultiPointField(srid=4326)
    # osm_id = models.CharField(max_length=120)
    # edge_length = models.FloatField()
    # bearing = models.FloatField()
    # center = models.PointField(srid=4326)
    # sub_sequence = models.IntegerField(default=-1)