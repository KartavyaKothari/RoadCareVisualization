import os,django
import json

from RoadMapView.models import RoadPothole,RoadPoint,RoadPothole_snapped
from django.contrib.gis.geos import Point
from datetime import datetime, timedelta
import pandas as pd

from django.contrib.gis.geos import Polygon
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance

import time
import numpy as np

def run():
    # Delete previous data
    # RoadPothole_snapped.objects.all().delete()
    rp=RoadPothole.objects.all()

    # Seetting the nearest road api
    search_distance = 50
    time_req = []

    for r in rp:
        # output_pt=None
        input_pt = Point(r.point.x,r.point.y)

        start_time = time.time()
        matched_points = RoadPoint.objects.filter(point__distance_lt=(input_pt,D(m=search_distance)))
        time_req.append(time.time()-start_time)
        # if len(matched_points) != 0:
        #     output_pt = matched_points[0].point
        
        #     if RoadPothole_snapped.objects.filter(point=output_pt).exists():
        #         pothole = RoadPothole_snapped.objects.get(point=output_pt)
        #         pothole.rating = (pothole.rating*pothole.total_potholes+r.rating)/(pothole.total_potholes+1)
        #         pothole.total_potholes = pothole.total_potholes+1
        #     else:
        #         pothole = RoadPothole_snapped(point=output_pt,rating=r.rating,bearing=r.bearing,total_potholes=1)
            
        #     pothole.save()
    
    print(len(RoadPothole_snapped.objects.all()))
    time_req = np.array(time_req)
    print("Mean:",np.mean(time_req,axis=0)*1000,"(ms)"," Std:",np.std(time_req,axis=0)*1000,"(ms)")