#imports fro django
import os,django
import json

#model imports
from RoadMapView.models import RoadData_snapped
from django.contrib.gis.geos import Point,MultiPoint
from django.contrib.gis.measure import D
from geographiclib.geodesic import Geodesic 

from django.db import transaction

@transaction.atomic
def run():
    content =""
    with open('tmp/all_road_10m_min_distance_mumbai.json', 'r') as content_file:
        content = content_file.read()

    RoadData_snapped.objects.all().delete()

    content = content.split("=")[1]
    json_data = json.loads(content)
    for v in json_data:
        
        latlons= v['latlongs']
        counter = 0
        for latlon1,latlon2 in zip(latlons[0:],latlons[1:]):
            counter += 1
            geodesic_result = Geodesic.WGS84.Inverse(latlon1["lat"],latlon1["lng"],latlon2["lat"],latlon2["lng"]) # Geodesic.WGS84.Inverse(lat_1,lon_1,lat_2,lon_2)
            edge_length = geodesic_result['s12']
            bearing = geodesic_result['azi1']
            p1 = Point(latlon1["lng"],latlon1["lat"])
            p2 = Point(latlon2["lng"],latlon2["lat"])
            center = Point((latlon1["lng"] + latlon2["lng"])/2.0,(latlon1["lat"] + latlon2["lat"])/2.0)
            mp = MultiPoint(p1,p2)
            rd = RoadData_snapped(multipoint=mp,osm_id=str(v['id']),center=center,edge_length=edge_length,bearing=bearing,\
                sub_sequence=counter,rating = 3,total_potholes = 0)
            rd.save()
            # print(rd)
        
    print(len( RoadData_snapped.objects.all()))












# import os,django
# import json
# from RoadMapView.models import RoadData
# from django.contrib.gis.geos import Point
# from django.contrib.gis.measure import D
# from django.contrib.gis.geos import MultiPoint

# # from django.db.transaction import commit_on_success
# from django.db import transaction

# content =""
# file_name = 'tmp/all_road_10m_min_distance_mumbai.json'

# @transaction.atomic
# def run():
#     with open(file_name, 'r') as content_file:
#         content = content_file.read()

#     RoadData.objects.all().delete()

#     content = content.split("=")[1]
#     json_data = json.loads(content)
    
#     for v in json_data:
#         latlons= v['latlongs']
#         mp = MultiPoint()
#         for lt in latlons:
#             pt = Point(lt['lng'],lt['lat'])
#             mp.append(pt)
#         rd = RoadData(multipoint=mp,osm_id=str(v['id']))
#         # print(rd)
#         rd.save()
    
#     print(len( RoadData.objects.all()))