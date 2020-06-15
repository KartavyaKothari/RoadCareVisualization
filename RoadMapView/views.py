from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic import TemplateView
from .models import RoadData,RoadPoint,RoadPothole,RoadPothole_snapped
import json
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Polygon
from django.db.models import Q

class RoadView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(RoadView, self).get_context_data(**kwargs)
        rd = RoadData.objects.all()
        all_road_data = []
        for r in rd:
            temp={}
            temp['id']=r.osm_id
            temp['latlongs']=[]
            for ll in r.multipoint:
                temp['latlongs'].append({
                    "lat":ll.y,
                    "lng":ll.x
                })
            all_road_data.append(temp)
        context['all_road_data'] = json.dumps(all_road_data)
        return context

def nearest_road(request):
    print("Nearest Road")
    print(float(request.GET.get("lat")))
    print(float(request.GET.get("lng")))
    lat = float(request.GET.get("lat"))
    lng = float(request.GET.get("lng"))
    
    input_pt = Point(lng,lat)
    output_pt=None
    
    start_distance = 50
    end_distance = 200
    
    iterations = int((end_distance-start_distance) / start_distance)
    
    for i in range(1,iterations+1):
        matched_points = RoadPoint.objects.filter(point__distance_lt=(input_pt,D(m=start_distance*i))).annotate(distance=Distance('point',input_pt)).order_by("distance")
        print("Distance " + str(start_distance *i))

        if len(matched_points) != 0:
            print(len(matched_points))
            print(matched_points)
            output_pt = matched_points[0]
            print(output_pt)
            break
    op = {
        "lat":output_pt.point.y,
        "lng":output_pt.point.x,
        "bearing":output_pt.bearing
    }
    print(json.dumps(op))
    return HttpResponse(json.dumps(op), content_type='application/json')

def binarySearchwithTolerance(arr, x,t):
    l=0
    r=len(arr)-1
    while l <= r: 
        mid = int(l + (r - l)/2)
        if abs(arr[mid].bearing - x) <= t: 
            # we found someone in tolerance
            index =mid
            lb= -1
            for i in range(index,l-1,-1):
                if abs(arr[i].bearing-x) > t:
                    break
                lb = i
            index = mid
            ub =-1
            for i in range(index,r+1,1):
                if abs(arr[i].bearing -x) > t:
                    break
                ub = i
            return (lb,ub)
        elif arr[mid].bearing > x: 
            r = mid - 1
        else: 
            l = mid + 1
    return None


def get_potholes_from_db(request):
    message = {'err':"some error"}

    if request.method == 'POST':
        bbox = request.POST.getlist('bounds[]')
        print(bbox)

        bbox = (bbox[0],bbox[1],bbox[2],bbox[3])

        geom = Polygon.from_bbox(bbox)

        # print("Geom ", geom[0][0][0])
        box = [{'lat':geom[0][0][1],
                'lng':geom[0][0][0]},
                {'lat':geom[0][1][1],
                'lng':geom[0][1][0]},
                {'lat':geom[0][2][1],
                'lng':geom[0][2][0]},
                {'lat':geom[0][3][1],
                'lng':geom[0][3][0]},
                {'lat':geom[0][0][1],
                'lng':geom[0][0][0]}
                ]

        # rp = RoadPothole.objects.all()
        # print(rp[0].point)
        rp = RoadPothole_snapped.objects.filter(point__within=geom).distinct('point')
        print("count :",rp.count())
        all_pothole_data = []

        # print(rp[0])

        for r in rp:
            # print(r[0],r[1])
            # temp={}
            # temp['id']=r.osm_id
            # temp['latlongs']=[]
            # for ll in r.multipoint:
            #     temp['latlongs'].append({
            #         "lat":ll.y,
            #         "lng":ll.x
            #     })
            all_pothole_data.append({ 'lat' : r.point.y , 'lng' : r.point.x })

        message = {'list': all_pothole_data,'geom':box}

    return JsonResponse(message)

def get_roads_from_db(request):
    message = "Some error"
    if request.method ==  'POST':
        bbox = request.POST.getlist('bounds[]')
        print(bbox)

        bbox = (bbox[0],bbox[1],bbox[2],bbox[3])

        geom = Polygon.from_bbox(bbox)

        # print("Geom ", geom[0][0][0])
        box = [{'lat':geom[0][0][1],
                'lng':geom[0][0][0]},
                {'lat':geom[0][1][1],
                'lng':geom[0][1][0]},
                {'lat':geom[0][2][1],
                'lng':geom[0][2][0]},
                {'lat':geom[0][3][1],
                'lng':geom[0][3][0]},
                {'lat':geom[0][0][1],
                'lng':geom[0][0][0]}
                ]

        # rd = RoadData.objects.all()
        rd = RoadData.objects.filter(Q(multipoint__within=geom)|Q(multipoint__intersects=geom))
        print("count :",rd.count())
        all_road_data = []

        for r in rd:
            temp={}
            temp['id']=r.osm_id
            temp['latlongs']=[]
            for ll in r.multipoint:
                temp['latlongs'].append({
                    "lat":ll.y,
                    "lng":ll.x
                })
            all_road_data.append(temp)
            # print(temp)

        # ne = (19.136605420061482, 72.91854322098668)
        # sw = (19.12949450339526, 72.90821877901332)

        # xmin=sw[1]
        # ymin=sw[0]
        # xmax=ne[1]
        # ymax=ne[0]

        # bbox = (xmin, ymin, xmax, ymax)

        # geom = Polygon.from_bbox(bbox)
        # q = RoadPoint.objects.filter(point__within=geom)
        # print(q)
        # all_road_data = ['a','b','c']
        # print
        message = {'list': all_road_data,'geom':box}

    return JsonResponse(message)

def nearest_road_same_direction(request):
    print("nearest_road_same_direction")
    print(float(request.GET.get("lat")))
    print(float(request.GET.get("lng")))
    lat = float(request.GET.get("lat"))
    lng = float(request.GET.get("lng"))
    bearing = float(request.GET.get("bearing"))
    tolerance = 10
    input_pt = Point(lng,lat)
    output_pt=None
    start_distance = 150
    end_distance = 1500
    iterations = int((end_distance-start_distance) / start_distance)
    for i in range(1,iterations+1):
        matched_points = RoadPoint.objects.filter(point__distance_lt=(input_pt,D(m=start_distance*i))).annotate(distance=Distance('point',input_pt)).order_by("bearing")

        indices = binarySearchwithTolerance(matched_points,bearing,tolerance)
        print("len ", len(matched_points)," indices",indices)
        if indices == None:
            print("No points found in the bearing " , bearing , " tolerance ", tolerance , " distance ",start_distance*i)
            continue
        else:
            # filterqueryset = matched_points[indices[0],indices[1]]
            filterdlist = []
            for i in range(indices[0],indices[1]+1):
                filterdlist.append( [matched_points[i].point,matched_points[i].bearing,matched_points[i].distance])
            filterdlist.sort(key = lambda x : x[2])
            
        print("Distance " + str(start_distance *i))

        if len(filterdlist) != 0:
            print(len(filterdlist))
            print("filteredlist",filterdlist)
            output_pt = filterdlist[0]
            print(output_pt)
            break
    op = {
        "lat":output_pt[0].y,
        "lng":output_pt[0].x,
        "bearing":output_pt[1],
        "distance":output_pt[2].m
    }
    print(json.dumps(op))
    return HttpResponse(json.dumps(op), content_type='application/json')