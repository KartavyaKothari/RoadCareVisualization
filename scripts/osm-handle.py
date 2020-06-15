import xml.etree.ElementTree as ET
import json

def run():
    fileName = 'tmp/map.osm'

    tree = ET.iterparse(fileName)
    # root = tree.getroot()
    # root[1].attrib['id']
    # for evt,element in tree:
        # if i==0:
        #   continue
        # print(element.tag)
        # element.clear()

    map_node_lat_long = {}

    for evt,element in tree:
        if element.tag == 'node':
            # print(element.tag)
            map_node_lat_long[element.attrib['id']]={'lat':float(element.attrib['lat']),'lng':float(element.attrib['lon'])}
        # else: print(element.tag)
        element.clear()

    # print(map_node_lat_long)

    array_ways = []

    tree = ET.iterparse(fileName)

    for evt,element in tree:
        # print(element.tag)
        if element.tag == 'way':
            temp = {}
            temp['id'] = int(element.attrib['id'])
            temp['latlongs'] = []

            # print(temp)

            try:
                shouldContinue =False
                for tag in element:
                    # print(tag.tag)
                    if tag.tag == 'tag':
                        # print(tag.attrib)
                        if tag.attrib['k'] ==  "highway" and (tag.attrib['v']== "motorway" or tag.attrib['v']== "trunk" or tag.attrib['v']== "primary" or tag.attrib['v']== "secondary" or tag.attrib['v']== "tertiary" or tag.attrib['v']== "unclassified" or tag.attrib['v']== "residential" or tag.attrib['v']== "service"):
                            shouldContinue=True
                            break
                if not shouldContinue:
                    # print("Road arounf building" , way);
                    continue
            except:
                print("err")

            for nd in element:
                if nd.tag=='nd':
                    id = str(nd.attrib['ref'])
                    temp['latlongs'].append(map_node_lat_long[id])
            
            # print(temp)
            array_ways.append(temp)
            element.clear()
        
    with open('tmp/op.json', 'w') as f:
        json.dump(array_ways, f)
