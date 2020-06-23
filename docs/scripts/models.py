from django.contrib.gis.db import models
from django.contrib.gis.geos import MultiPoint


class RoadData():
    multipoint = models.MultiPointField()
    osm_id = models.CharField(max_length=120)

    def road_len(self):
        return len(self.multipoint)
    def __str__(self):
        return str(self.osm_id)

class RoadPothole():
    point = models.PointField()
    rating = models.FloatField()
    bearing = models.FloatField()

    def __str__(self):
        return "lat: "+str(self.point.x)+", lng: "+str(self.point.y)+", rating: "+str(self.rating)+", bearing: "+str(self.bearing)

class RoadPothole_snapped():
    point = models.PointField()
    rating = models.FloatField()
    bearing = models.FloatField()
    total_potholes = models.IntegerField()

    def __str__(self):
        return "lat: "+str(self.point.x)+", lng: "+str(self.point.y)+", rating: "+str(self.rating)+", bearing: "+str(self.bearing)
    
class RoadPoint():
    point = models.PointField()
    # roaddata = models.ForeignKey(RoadData,on_delete=models.CASCADE)
    bearing = models.FloatField()
    sequence_number = models.IntegerField()

    def __str__(self):
        return str(self.point.x) +"," + str(self.point.y) + " TP: " + \
            str(len(self.roaddata.multipoint)) + " BR " + str(self.bearing) + \
                " SQN "+ str(self.sequence_number)  


# >>> from django.contrib.gis.geos import Point
# >>> pnt = Point(5, 23)
# >>> pnt1 = Point(5, 22)
# >>> from django.contrib.gis.geos import MultiPoint
# >>> mp  = MultiPoint(pnt,pnt1)
# >>> mp
# <MultiPoint object at 0x1129f6808>
# >>> str(mp)
# 'MULTIPOINT (5 23, 5 22)'
# >>> from road_data.models import RoadData
# >>> RoadData(mp,"123")
# <RoadData: RoadData object (MULTIPOINT (5 23, 5 22))>
# >>> tt = RoadData(mp,"123")
# >>> tt.save
# tt.save(      tt.save_base(
# >>> tt.save()
