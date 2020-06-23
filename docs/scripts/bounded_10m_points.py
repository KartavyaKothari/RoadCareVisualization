import pandas as pd
import json

max_lat = 19.251647
min_lon = 72.821591
min_lat = 19.021189
max_lon = 72.978486

def run():
    with open('tmp/all_road_10m_min_distance.json','r') as f:
        data = f.read()

    data = json.loads(data.split("=")[1])

    list_of_bounded_latlons = []

    for i,road in enumerate(data):
        shouldAdd = True
        for point in road['latlongs']:
            if not (max_lat >= point['lat'] >= min_lat and max_lon >= point['lng'] >= min_lon) :
                shouldAdd = False
                break
        if shouldAdd:
            list_of_bounded_latlons.append(road)


    with open("tmp/all_road_10m_min_distance_mumbai.json","w") as f:
        f.write("var all_road_10m_min_distance = "+json.dumps(list_of_bounded_latlons))

    # print(len(data),len(list_of_bounded_latlons))
