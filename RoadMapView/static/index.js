const ALL_CLEAR = 0;
const RAW_POTHOLES = 1;
const RAW_ROADS = 2;
const SNAPPED_ROAD = 3;
var TIME_OUT_DEBUG = 0;

var map;
var lastBox;

var markers = []
var potholes = []
var boxes = []
var road_segs = []

var show_bounding_box = false;
var whatToShow = ALL_CLEAR;


function getColorFromRating(rating){
    if(rating==3)return "#00ff00" //green "#008a0b"
    if(rating<3 && rating>2) return "#00a0ff" //blue
    if(rating==2)return "#fe9700" //orange
    if(rating<2 && rating>1) return "#ff0000" //red
    if(rating<=1)return "#000000" //black

    // if(rating==3)return "#007811"
    // if(rating<3 && rating>2) return "#b4ce7a"
    // if(rating==2)return "#b6873c"
    // if(rating<2 && rating>1) return "#c56b30"
    // if(rating<=1)return "#ff0000"
}

function erase_bounding_box(){
    for(var box in boxes)
        boxes[box].setMap(null);
    
    boxes = []
}

function clear_roads(){
    for (var road in road_segs) {
        road_segs[road].setMap(null)
    }
    road_segs = []
}

function clear_potholes(){
    for (var hole in potholes){
        potholes[hole].setMap(null)
    }
    potholes = []
}

function clear_all(){
    clear_roads()
    clear_potholes()
    erase_bounding_box()
    console.log("all clear")
}

function see_bounding_box(box){
    var bounding_box = new google.maps.Polyline({
        path:box,
        geodesic: true,
        strokeColor: '#000',
        strokeOpacity: 1.0,
        strokeWeight: 5
    })

    boxes.push(bounding_box);
    bounding_box.setMap(map);
}

function toggle_bounding_box(){
    if(!show_bounding_box){
        // TIME_OUT_DEBUG = 2000
        see_bounding_box(lastBox)
        show_bounding_box = true
    } else {
        // TIME_OUT_DEBUG = 0   
        erase_bounding_box()
        show_bounding_box = false
    }
}

function see_raw_roads(){
    whatToShow = RAW_ROADS
    bbox = getBoundingBox()
    get_map_data_for(map,bbox)
}

function see_raw_potholes(){
    whatToShow = RAW_POTHOLES
    bbox = getBoundingBox()
    get_raw_potholes(map,bbox)
}

function see_road_quality(){
    whatToShow = SNAPPED_ROAD
    bbox = getBoundingBox()
    get_pothole_data_for(map,bbox)
}

function see_nothing(){
    whatToShow = ALL_CLEAR
    clear_all()
}

function getBoundingBox(){
    ne_lng=map.getBounds().getNorthEast().lng()
    ne_lat=map.getBounds().getNorthEast().lat()
    sw_lng=map.getBounds().getSouthWest().lng()
    sw_lat=map.getBounds().getSouthWest().lat()

    ne = [ne_lat, ne_lng]
    sw = [sw_lat, sw_lng]

    xmin=sw[1]
    ymin=sw[0]
    xmax=ne[1]
    ymax=ne[0]

    bbox = [xmin, ymin, xmax, ymax]

    return bbox
}

function initMap() {
    var iit_location = {lat: 19.124910138009756, lng: 72.91621232284234};
    
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 19,
        center: iit_location,
        scaleControl: true
    });

    var centerControlDiv = document.createElement('div');
    var centerControl = new CenterControl(centerControlDiv, map, "Clear all");
    centerControlDiv.index = 1;
    centerControlDiv.addEventListener('click', function () {
        see_nothing()
    });
    map.controls[google.maps.ControlPosition.LEFT_CENTER].push(centerControlDiv);

    var centerControlDiv2 = document.createElement('div');
    var centerControl2 = new CenterControl(centerControlDiv2, map, "Show road quality");
    centerControlDiv2.index = 2;
    centerControlDiv2.addEventListener('click', function () {
        see_road_quality()
    });
    map.controls[google.maps.ControlPosition.LEFT_CENTER].push(centerControlDiv2);

    var centerControlDiv3 = document.createElement('div');
    var centerControl3 = new CenterControl(centerControlDiv3, map, "Show predictions");
    centerControlDiv3.index = 3;
    centerControlDiv3.addEventListener('click', function () {
        see_raw_potholes()
    });
    map.controls[google.maps.ControlPosition.LEFT_CENTER].push(centerControlDiv3);

    var centerControlDiv4 = document.createElement('div');
    var centerControl4 = new CenterControl(centerControlDiv4, map, "Show roads");
    centerControlDiv4.index = 4;
    centerControlDiv4.addEventListener('click', function () {
        see_raw_roads()
    });
    map.controls[google.maps.ControlPosition.LEFT_CENTER].push(centerControlDiv4);

    var centerControlDiv5 = document.createElement('div');
    var centerControl5 = new CenterControl(centerControlDiv5, map, "Toggle bounding box");
    centerControlDiv5.index = 5;
    centerControlDiv5.addEventListener('click', function () {
        toggle_bounding_box()
    });
    map.controls[google.maps.ControlPosition.LEFT_CENTER].push(centerControlDiv5);

    // var centerControlDiv56 = document.createElement('div');
    // var centerControl6 = new CenterControl(centerControlDiv6, map, <img src="{% load static 'legen.png' %}"></img>);
    // centerControlDiv6.index = 6;
    // centerControlDiv6.addEventListener('click', function () {
    //     toggle_bounding_box()
    // });
    // map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(centerControlDiv6);

    google.maps.event.addListener(map, 'click', function (event) {
        console.log(event.latLng.toJSON())
        addMarker(event.latLng, map);
    });

    google.maps.event.addListener(map, 'idle', function (event) {
        bbox = getBoundingBox()

        console.log(bbox)

        clear_all()

        window.setTimeout(function(){
            switch(whatToShow) {
                case ALL_CLEAR:
                    clear_all()
                    break;
                case RAW_POTHOLES:
                    get_raw_potholes(map,bbox)
                    break;
                case RAW_ROADS:
                    get_map_data_for(map,bbox)
                    break;
                case SNAPPED_ROAD:
                    get_pothole_data_for(map,bbox)
                    break;
                default:
                    clear_all()
            }
        },TIME_OUT_DEBUG)
    });

    function addMarker(location, map) {
        if (markers.length == 0) {
            counter = 0
        }
        counter++
        var marker = new google.maps.Marker({
            position: location,
            label: "Marked Point " + counter,
            map: map,
            draggable: true
        });
        markers.push(marker)

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {
                lat_lon_obj = JSON.parse(this.responseText);
                var marker_changed = new google.maps.Marker({
                    position: lat_lon_obj,
                    label: "New Point " + counter,
                    map: map,
                    draggable: true
                });
                markers.push(marker_changed)
            }
        };

        xhttp.open("GET", "nearest_road?lat= " + location.lat() + "&lng=" + location.lng(), true);
        xhttp.send();
    }
}

function get_pothole_data_for(map,bbox){
    $.ajax({
        url: '/road_data/show/get_potholes_from_db',
        data: {
          'csrfmiddlewaretoken': csrf_token,
            'bounds[]':bbox
      },
        type: 'POST'
      }).done(function(response){
        console.log(response['list']);

        lastBox = response['geom'];

        if(show_bounding_box)
            see_bounding_box(lastBox)
        
        all_road_10m_min_distance = response['list']

        for (var points in all_road_10m_min_distance) {
            var seg = new google.maps.Polyline({
                path:
                    [all_road_10m_min_distance[points]['latlongs'][0],
                    all_road_10m_min_distance[points]['latlongs'][1]]
                ,
                geodesic: true,
                strokeColor: getColorFromRating(all_road_10m_min_distance[points]['rating']),
                strokeOpacity: 1.0,
                strokeWeight: 5
            });
            seg.idfromopenstreet = all_road_10m_min_distance[points]["id"]
            seg.addListener("click", function () {
                var infowindow = new google.maps.InfoWindow({
                    content: this.idfromopenstreet.toString()
                });
                infowindow.setPosition(this.midLatLang);
                infowindow.open(map)
            })

            road_segs.push(seg)
        }        

        for (var road in road_segs) {
            road_segs[road].setMap(map)
        }
    });
}

function get_raw_potholes(map,bbox){
    $.ajax({
        url: '/road_data/show/get_raw_potholes',
        data: {
          'csrfmiddlewaretoken': csrf_token,
            'bounds[]':bbox
      },
        type: 'POST'
      }).done(function(response){
        console.log(response['list'][0]);

        lastBox = response['geom'];

        if(show_bounding_box)
            see_bounding_box(lastBox)

        var skipPoints = 10
        var zoom = map.zoom

        response['list'].forEach(myFunction);
        function myFunction(item,index){
            if(index%skipPoints==0){
                color = getColorFromRating(item['rating'])

                marker = new google.maps.Marker({
                    position: item['pot_loc'],
                    map: map,
                    icon: {
                        path: google.maps.SymbolPath.CIRCLE,
                        fillColor: color,
                        fillOpacity: 0.6,
                        strokeColor: color,
                        strokeOpacity: 0.9,
                        strokeWeight: 1,
                        scale: 3
                    }
                });

                potholes.push(marker)
            }
        }
    });
}

function get_map_data_for(map,bbox){
    $.ajax({
        url: '/road_data/show/get_roads_from_db',
        data: {
          'csrfmiddlewaretoken': csrf_token,
            'bounds[]':bbox
      },
        type: 'POST'
      }).done(function(response){
        console.log(response['list']);

        lastBox = response['geom'];

        if(show_bounding_box)
            see_bounding_box(lastBox)
        
        all_road_10m_min_distance = response['list']

        for (var points in all_road_10m_min_distance) {
            var seg = new google.maps.Polyline({
                path: [all_road_10m_min_distance[points]['latlongs'][0],all_road_10m_min_distance[points]['latlongs'][1]],
                geodesic: true,
                strokeColor: '#f00',
                strokeOpacity: 1.0,
                strokeWeight: 5
            });
            seg.idfromopenstreet = all_road_10m_min_distance[points]["id"]
            seg.midLatLang = all_road_10m_min_distance[points]['latlongs'][0]
            seg.addListener("click", function () {
                var infowindow = new google.maps.InfoWindow({
                    content: this.idfromopenstreet.toString()
                });
                infowindow.setPosition(this.midLatLang);
                infowindow.open(map)
            })

            road_segs.push(seg)
        }        

        for (var road in road_segs) {
            road_segs[road].setMap(map)
        }
    });
}

function CenterControl(controlDiv, map, text) {
    var controlUI = document.createElement('div');
    controlUI.style.backgroundColor = '#fff';
    controlUI.style.border = '2px solid #fff';
    controlUI.style.borderRadius = '3px';
    controlUI.style.boxShadow = '0 2px 6px rgba(0,0,0,.3)';
    controlUI.style.cursor = 'pointer';
    controlUI.style.marginBottom = '22px';
    controlUI.style.textAlign = 'center';
    controlUI.title = 'Click to recenter the map';
    controlDiv.appendChild(controlUI);

    // Set CSS for the control interior.
    var controlText = document.createElement('div');
    controlText.style.color = 'rgb(25,25,25)';
    controlText.style.fontFamily = 'Roboto,Arial,sans-serif';
    controlText.style.fontSize = '16px';
    controlText.style.lineHeight = '38px';
    controlText.style.paddingLeft = '5px';
    controlText.style.paddingRight = '5px';
    controlText.innerHTML = text;
    controlUI.appendChild(controlText);
}

function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);
}

// see_raw_roads()
// see_raw_potholes()
// see_road_quality()
see_nothing()