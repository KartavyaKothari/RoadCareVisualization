import os,django
import json
from RoadMapView.models import RoadData
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.geos import MultiPoint

# from django.db.transaction import commit_on_success
from django.db import transaction

content =""
file_name = 'tmp/all_road_10m_min_distance_mumbai.json'

@transaction.atomic
def run():
    with open(file_name, 'r') as content_file:
        content = content_file.read()

    RoadData.objects.all().delete()

    content = content.split("=")[1]
    json_data = json.loads(content)
    
    for v in json_data:
        latlons= v['latlongs']
        mp = MultiPoint()
        for lt in latlons:
            pt = Point(lt['lng'],lt['lat'])
            mp.append(pt)
        rd = RoadData(multipoint=mp,osm_id=str(v['id']))
        # print(rd)
        rd.save()
    
    print(len( RoadData.objects.all()))