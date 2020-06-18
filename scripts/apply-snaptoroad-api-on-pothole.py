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
    RoadPothole_snapped.objects.all().delete()
    rp=RoadPothole.objects.all()

    # Seetting the nearest road api
    start_distance = 50
    end_distance = 100
    iterations = int((end_distance-start_distance) / start_distance)

    # debug_cnt = 0

    for r in rp:
    #     if(index==50):
    #         exit()
        # print(debug_cnt)
        # debug_cnt = debug_cnt+1
        output_pt=None
        input_pt = Point(r.point.x,r.point.y)
        flag=True
        for i in range(1,iterations+1):
            matched_points = RoadPoint.objects.filter(point__distance_lt=(input_pt,D(m=start_distance*i)))
            # print("mp: ",matched_points)
            if len(matched_points) != 0:
                flag=False
                output_pt = matched_points[0]
                break
        if(flag==True):
            output_pt=input_pt
        else:
            output_pt=output_pt.point
        # print(row[0])
        # rating = 0
        
        if RoadPothole_snapped.objects.filter(point=output_pt).exists():
            pothole = RoadPothole_snapped.objects.get(point=output_pt)
            pothole.rating = (pothole.rating*pothole.total_potholes+r.rating)/(pothole.total_potholes+1)
            pothole.total_potholes = pothole.total_potholes+1
            # print(pothole.rating)
            # pothole = RoadPothole_snapped(point=output_pt,rating=rating,bearing=r.bearing,total_potholes=0)
        else:
            pothole = RoadPothole_snapped(point=output_pt,rating=r.rating,bearing=r.bearing,total_potholes=1)
        
        pothole.save()

        # if not RoadPothole_snapped.objects.filter(point=output_pt):
        #     pothole = RoadPothole_snapped(point=output_pt,rating=rating,bearing=r.bearing,total_potholes=0)
        #     pothole.save()
        # pothole = RoadPothole_snapped(point=output_pt,rating=rating,bearing=r.bearing)
        # pothole.save()
        # print("Point conversion",input_pt,output_pt)
    
    print(len( RoadPothole_snapped.objects.all()))