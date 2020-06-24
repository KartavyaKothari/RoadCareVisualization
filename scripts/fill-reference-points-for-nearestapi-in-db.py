import os,django
import json

from RoadMapView.models import RoadData,RoadPoint
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.geos import MultiPoint
import math

# from django.db.transaction import commit_on_success
from django.db import transaction

content = ""

def bearing_tuple(t1,t2):
    # return get_bearing(t1.latitude,t1.longitude,t2.latitude,t2.longitude)
    # latitude1 = math.radians(t1.latitude)
    latitude1 = math.radians(t1.x)
    # latitude2 = math.radians(t2.latitude)
    latitude2 = math.radians(t2.x)
    # longitude1 = math.radians(t1.longitude)
    longitude1 = math.radians(t1.y)
    # longitude2 = math.radians(t2.longitude)
    longitude2 = math.radians(t2.y)
    y = math.sin(longitude2-longitude1) * math.cos(latitude2)
    x = math.cos(latitude1)*math.sin(latitude2) - math.sin(latitude1)*math.cos(latitude2)*math.cos(longitude2-longitude1)
    brng = (math.degrees(math.atan2(y, x)) + 360) %360
    return brng

@transaction.atomic
def run():
    
    RoadPoint.objects.all().delete()

    with open('tmp/all_road_10m_min_distance_mumbai.json', 'r') as content_file:
        content = content_file.read()

    content = content.split("=")[1]
    json_data = json.loads(content)

    for v in json_data:
        rdo = RoadData.objects.filter(osm_id=str(v['id']))[0]
        latlons= v['latlongs']
        
        sequence_no=0
        prev_pt = None
        bearing =-1
        for lt in latlons:
            pt = Point(lt['lng'],lt['lat'])
            sequence_no+=1
            if prev_pt == None:
                bearing = -1
            else:
                bearing = bearing_tuple(prev_pt,pt)
            rp = RoadPoint(point=pt,roaddata =rdo,bearing = bearing , sequence_number = sequence_no)
            prev_pt = pt
            
            rp.save()

    print(len( RoadPoint.objects.all()))