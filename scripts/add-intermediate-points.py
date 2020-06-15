import json
from geopy.distance import great_circle
from geographiclib.geodesic import Geodesic
from geopy import distance
import geopy
import math

min_distance_in_m = 10

def bearing_tuple(t1,t2):
    # return get_bearing(t1.latitude,t1.longitude,t2.latitude,t2.longitude)
    latitude1 = math.radians(t1.latitude)
    latitude2 = math.radians(t2.latitude)
    longitude1 = math.radians(t1.longitude)
    longitude2 = math.radians(t2.longitude)
    y = math.sin(longitude2-longitude1) * math.cos(latitude2)
    x = math.cos(latitude1)*math.sin(latitude2) - math.sin(latitude1)*math.cos(latitude2)*math.cos(longitude2-longitude1)
    brng = math.degrees(math.atan2(y, x))
    return brng

# def get_bearing(lat1, lat2, long1, long2):
#     brng = Geodesic.WGS84.Inverse(lat1, long1, lat2, long2)['azi1']
#     return brng

def getNextPoint(t1,bearing):
    # # Define a general distance object, initialized with a distance of 1 km.
    # d = geopy.distance.VincentyDistance(meters = min_distance_in_m)
    # # Use the `destination` method with a bearing of 0 degrees (which is north)
    # # in order to go from point `start` 1 km to north.
    # bearing = bearing*((22/7)/180)

    # return d.destination(point=t1, bearing=bearing)
    # return distance.distance(meters=min_distance_in_m).destination(t1,bearing) 
    R = 6371 #Radius of the Earth
    brng = math.radians(bearing) #Bearing is 90 degrees converted to radians.
    d = min_distance_in_m/1000 #Distance in km

    #lat2  52.20444 - the lat result I'm hoping for
    #lon2  0.36056 - the long result I'm hoping for.

    lat1 = math.radians(t1.latitude) #Current lat point converted to radians
    lon1 = math.radians(t1.longitude) #Current long point converted to radians

    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) +
        math.cos(lat1)*math.sin(d/R)*math.cos(brng))

    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),
                math.cos(d/R)-math.sin(lat1)*math.sin(lat2))

    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)

    return geopy.Point(lat2,lon2)

def calculateDistance(t1,t2):
    return great_circle(t1,t2).meters

def run():
    content =""

    with open('tmp/op.json', 'r') as content_file:
        content = content_file.read()

    content = content.replace("var somepoints = ","")
    json_data = json.loads(content)

    for way in json_data:
        # print ("id" + str(way['id']))
        curr=None
        prev = None
        for latlongs in way['latlongs']:
            if not prev:
                prev = geopy.Point(latlongs["lat"],latlongs["lng"])
                continue
            curr = geopy.Point(latlongs["lat"],latlongs["lng"])
            distance = calculateDistance(prev,curr)
            bearing = bearing_tuple(prev,curr)
            # print("distance "+str(distance) +" bearing "+ str(bearing))
            prev = curr

    print("++++++++++++++++++++++++")


    new_json_data = []
    for way in json_data:
        payload ={}
        payload['id'] = way['id']
        payload['latlongs'] = []
        curr = None
        prev = None
        for latlongs in way['latlongs']:
            if not prev:
                prev = geopy.Point(latlongs["lat"],latlongs["lng"])
                payload['latlongs'].append(latlongs)
                continue
            curr = geopy.Point(latlongs["lat"],latlongs["lng"])
            # print ("prev  " + prev.format_decimal() )
            bearing = bearing_tuple(prev,curr)
            distance = calculateDistance(prev,curr)
            distance = int(distance)
            # print ("bearing  " + str(bearing) + " distance " + str(distance) )
            if distance > min_distance_in_m:
                np = getNextPoint(prev,bearing)
                payload['latlongs'].append({
                        "lat":np.latitude,
                        "lng": np.longitude
                    })
                # print ("np  " + np.format_decimal())
                for i in range(int(distance/min_distance_in_m -1) ):
                    # print(i+1)
                    np = getNextPoint(np,bearing)
                    # print ("np  " + str(np))
                    payload['latlongs'].append({
                        "lat":np.latitude,
                        "lng": np.longitude
                    })
            payload['latlongs'].append({
                    "lat":curr.latitude,
                    "lng":curr.longitude
            })
            prev = curr
        new_json_data.append(payload)
    f = open("tmp/all_road_10m_min_distance.json", "w")
    f.write("var all_road_10m_min_distance = " + json.dumps(new_json_data))
    f.close()

    # for way in new_json_data:
    #     # print ("id" + str(way['id']))
    #     curr = None
    #     prev = None
    #     for latlongs in way['latlongs']:
    #         if not prev:
    #             prev = geopy.Point(latlongs["lat"],latlongs["lng"])
    #             continue
    #         curr = geopy.Point(latlongs["lat"],latlongs["lng"])
    #         distance = calculateDistance(prev,curr)
    #         bearing = bearing_tuple(prev,curr)
    #         # print ("prev  " + prev.format_decimal() + " curr " + curr.format_decimal() )
    #         # print("distance "+str(distance) +" bearing "+ str(bearing))
    #         prev = curr