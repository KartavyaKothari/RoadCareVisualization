from django.contrib.gis.db import models
from django.contrib.gis.geos import MultiPoint


# class RoadData(models.Model):
#     multipoint = models.MultiPointField()
#     osm_id = models.CharField(max_length=120)

#     def road_len(self):
#         return len(self.multipoint)
#     def __str__(self):
#         return str(self.osm_id)

class RoadPothole(models.Model):
    point = models.PointField()
    rating = models.FloatField()
    bearing = models.FloatField()

    def __str__(self):
        return "lat: "+str(self.point.x)+", lng: "+str(self.point.y)+", rating: "+str(self.rating)+", bearing: "+str(self.bearing)

# class RoadPothole_snapped(models.Model):
#     point = models.PointField()
#     rating = models.FloatField()
#     bearing = models.FloatField()
#     total_potholes = models.IntegerField()

#     def __str__(self):
#         return "lat: "+str(self.point.x)+", lng: "+str(self.point.y)+", rating: "+str(self.rating)+", bearing: "+str(self.bearing)
    
# class RoadPoint(models.Model):
#     point = models.PointField()
#     roaddata = models.ForeignKey(RoadData,on_delete=models.CASCADE)
#     bearing = models.FloatField()
#     sequence_number = models.IntegerField()

#     def __str__(self):
#         return str(self.point.x) +"," + str(self.point.y) + " TP: " + \
#             str(len(self.roaddata.multipoint)) + " BR " + str(self.bearing) + \
#                 " SQN "+ str(self.sequence_number)  

class RoadData_snapped(models.Model):
    multipoint = models.MultiPointField(srid=4326)
    osm_id = models.CharField(max_length=120)
    edge_length = models.FloatField()
    bearing = models.FloatField()
    center = models.PointField(srid=4326)
    sub_sequence = models.IntegerField(default=-1)

    rating = models.FloatField()
    total_potholes = models.IntegerField()

    
    def road_len(self):
        return len(self.multipoint)
    def __str__(self):
        return "pk:{} | multipoint:{},osm_id:{},center:{},length:{},bearing:{},sub_seq:{}".format(self.osm_id,self.multipoint,\
            self.osm_id,self.center,self.edge_length,self.bearing,self.sub_sequence)

class RoadData(models.Model):
    multipoint = models.MultiPointField(srid=4326)
    osm_id = models.CharField(max_length=120)
    edge_length = models.FloatField()
    bearing = models.FloatField()
    center = models.PointField(srid=4326)
    sub_sequence = models.IntegerField(default=-1)

    
    def road_len(self):
        return len(self.multipoint)
    def __str__(self):
        return "pk:{} | multipoint:{},osm_id:{},center:{},length:{},bearing:{},sub_seq:{}".format(self.osm_id,self.multipoint,\
            self.osm_id,self.center,self.edge_length,self.bearing,self.sub_sequence)