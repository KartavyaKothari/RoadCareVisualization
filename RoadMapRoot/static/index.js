var debugs = []
var reds = []
var greens = []
var map;
var markers = []
var counter = 0
var TIME_OUT_DEBUG = 0;
var potholes = []

// $.ajax({
//     url: '/mapdist/get_line/',
//     data: {
//       'csrfmiddlewaretoken': csrf_token
//   },
//     type: 'POST'
//   }).done(function(response){
//     console.log(response);
//   });


function initMap() {
    var iit_location = {lat: 19.124910138009756, lng: 72.91621232284234};
    // console.log(somepoints)
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 19,
        center: iit_location,
        scaleControl: true
    });

    var centerControlDiv = document.createElement('div');
    var centerControl = new CenterControl(centerControlDiv, map);

    centerControlDiv.index = 1;
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(centerControlDiv);
    
    color_red = 0xFF0000
    color_blue = 0x0000FF
    color_green = 0x00FF00
    
    
    


    // sleep(3000)
    // ne_lng=map.getBounds().getNorthEast().lng()
    // console.log(ne_lng)
    // ne_lat=map.getBounds().getNorthEast().lat()

    // sw_lng=map.getBounds().getSouthWest().lng()
    // sw_lat=map.getBounds().getSouthWest().lat()

    // ne = (ne_lat, ne_lng)
    // sw = (sw_lat, sw_lng)

    // xmin=sw[1]
    // ymin=sw[0]
    // xmax=ne[1]
    // ymax=ne[0]


    // var index = 0;
    // var color = 0000;

    // all_road_10m_min_distance = JSON.parse(all_d)

    // for (var points in all_road_10m_min_distance) {
    //     total_points = all_road_10m_min_distance[points]['latlongs'].length
    //     pt = 0
    //     while (pt < total_points) {
    //         // color =color +0xFF ;
    //         index++;
    //         if (index % 3 == 1) {
    //             color = color_red;
    //         } else if (index % 3 == 2) {
    //             color = color_green;
    //         } else if (index % 3 == 0) {
    //             color = color_blue;
    //         }
    //         if (typeof all_road_10m_min_distance[points]['latlongs'][pt + 1] != "undefined") {
    //             var flightPath = new google.maps.Polyline({
    //                 path:
    //                     [all_road_10m_min_distance[points]['latlongs'][pt],
    //                     all_road_10m_min_distance[points]['latlongs'][pt + 1]]
    //                 ,
    //                 geodesic: true,
    //                 strokeColor: "#0f0", //change color for every line
    //                 strokeOpacity: 1.0,
    //                 strokeWeight: 5
    //             });
    //             flightPath.idfromopenstreet = all_road_10m_min_distance[points]["id"]
    //             flightPath.midLatLang = all_road_10m_min_distance[points]['latlongs'][pt]
    //             flightPath.addListener("click", function () {
    //                 // console.log(this.idfromopenstreet)
    //                 var infowindow = new google.maps.InfoWindow({
    //                     content: this.idfromopenstreet.toString()
    //                 });
    //                 infowindow.setPosition(this.midLatLang);
    //                 infowindow.open(map)
    //             })

    //             // console.log([all_road_10m_min_distance[points]['latlongs'][pt],
    //             //     all_road_10m_min_distance[points]['latlongs'][pt+1]])
    //             //flightPath.setMap(map);
    //             debugs.push(flightPath)
    //         }else console.log("total_points"+total_points+" , pt"+" "+pt)
    //         pt = pt + 1;
    //     }
    // }

    // for (var line in debugs) {
    //     debugs[line].setMap(map)
    // }
 
    // get_map_data_for(map,[72.90847462056415, 19.12949450339526, 72.91828737943585, 19.136605420061482])


    // for (var points in all_road_10m_min_distance) {
    //     total_points = all_road_10m_min_distance[points]['latlongs'].length
        
    //     index++;
    //     if (index % 3 == 1) {
    //         color = color_red;
    //     } else if (index % 3 == 2) {
    //         color = color_red;
    //     } else if (index % 3 == 0) {
    //         color = color_red;
    //     }
    //     if (typeof all_road_10m_min_distance[points]['latlongs'] != "undefined") {
    //         var flightPath = new google.maps.Polyline({
    //             path:all_road_10m_min_distance[points]['latlongs'],
    //             geodesic: true,
    //             strokeColor: '#' + ("00000" + color.toString(16)).substr(color.toString(16).length - 1), //change color for every line
    //             strokeOpacity: 1.0,
    //             strokeWeight: 5
    //         });
    //         flightPath.idfromopenstreet = all_road_10m_min_distance[points]["id"]
    //         flightPath.midLatLang = all_road_10m_min_distance[points]['latlongs'][(total_points/2)]
    //         flightPath.addListener("click", function () {
    //             console.log(this.midLatLang)
    //             var infowindow = new google.maps.InfoWindow({
    //                 content: this.idfromopenstreet.toString()
    //             });
    //             infowindow.setPosition(this.midLatLang);
    //             infowindow.open(map)
    //         })

    //         reds.push(flightPath)
    //     }
    // }




    google.maps.event.addListener(map, 'click', function (event) {
        console.log(event.latLng.toJSON())
        addMarker(event.latLng, map);
    });

    google.maps.event.addListener(map, 'idle', function (event) {
    
        console.log(map.getBounds().getNorthEast().lng())
        // console.log(event.latLng.toJSON())
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

        console.log(bbox)

        for (var line in reds) {
            reds[line].setMap(null)
        }
        reds = []

        for (var hole in potholes){
            potholes[hole].setMap(null)
        }
        potholes = []

        console.log("all clear")

        window.setTimeout(function(){
            get_map_data_for(map,bbox)
        },TIME_OUT_DEBUG)
    });

    // Adds a marker to the map.
    function addMarker(location, map) {
        // Add the marker at the clicked location, and add the next-available label
        // from the array of alphabetical characters.
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
                // alert( lat);
            }
        };

        xhttp.open("GET", "nearest_road?lat= " + location.lat() + "&lng=" + location.lng(), true);

        xhttp.send();
    }

    // for (var points in all_points){
    //     var flightPath = new google.maps.Polyline({
    //         path: all_points[points]['latlongs'],
    //         geodesic: true,
    //         strokeColor: '#00FF00',
    //         strokeOpacity: 0.5,
    //         strokeWeight: 2
    //     });
    //     flightPath.idfromopenstreet = all_points[points]["id"]
    //     flightPath.midLatLang = all_points[points]['latlongs'][0]
    //     flightPath.addListener("click",function(){
    //         console.log(this.idfromopenstreet)
    //         var infowindow = new google.maps.InfoWindow({
    //             content: this.idfromopenstreet.toString()
    //         });
    //         infowindow.setPosition(this.midLatLang);
    //         infowindow.open(map)
    //     }) 

    //     //flightPath.setMap(map);
    //     greens.push(flightPath);
    // }
    // console.log(JSON.parse(map+"").getBounds())
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
        console.log(response['list'][0]);
        console.log({lat: 72.90909269756398, lng: 19.125626230321046});

        // marker = new google.maps.Marker({
        //     position: {lng: 72.90909269756398, lat: 19.125626230321046},
        //     map: map,
        //     // icon: icons['parking'].icon
        //     icon: {
        //         path: google.maps.SymbolPath.CIRCLE,
        //         fillColor: '#00f',
        //         fillOpacity: 0.6,
        //         strokeColor: '#00f',
        //         strokeOpacity: 0.9,
        //         strokeWeight: 1,
        //         scale: 3
        //     }
        // });

        var skipPoints = 1
        var zoom = map.zoom

        // if(zoom < 18 && zoom >=8){
        //     skipPoints = (18 - zoom)*5
        // }

        response['list'].forEach(myFunction);
        function myFunction(item,index){
            if(index%skipPoints==0){
                color = "#00f"
                // console.log(item)
                // {lat: 72.90909269756398, lng: 19.125626230321046}
                // { lat: 19.133050, lng: 72.913381 }
                marker = new google.maps.Marker({
                    position: item,
                    map: map,
                    // icon: icons['parking'].icon
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
            // console.log(response)

    //     var flightPath = new google.maps.Polyline({
    //         path:response['geom'],
    //         geodesic: true,
    //         strokeColor: '#000', //change color for every line
    //         strokeOpacity: 1.0,
    //         strokeWeight: 5
    //     }).setMap(map);



    //     all_road_10m_min_distance = response['list']

    //     for (var points in all_road_10m_min_distance) {
    //         total_points = all_road_10m_min_distance[points]['latlongs'].length
    //         pt = 0
    //         while (pt < total_points) {
    //             // color =color +0xFF ;
    //             index++;
    //             if (index % 3 == 1) {
    //                 color = color_red;
    //             } else if (index % 3 == 2) {
    //                 color = color_red;
    //             } else if (index % 3 == 0) {
    //                 color = color_red;
    //             }
    //             if (typeof all_road_10m_min_distance[points]['latlongs'][pt + 1] != "undefined") {
    //                 var flightPath = new google.maps.Polyline({
    //                     path:
    //                         [all_road_10m_min_distance[points]['latlongs'][pt],
    //                         all_road_10m_min_distance[points]['latlongs'][pt + 1]]
    //                     ,
    //                     geodesic: true,
    //                     strokeColor: '#f00', //change color for every line
    //                     strokeOpacity: 1.0,
    //                     strokeWeight: 5
    //                 });
    //                 flightPath.idfromopenstreet = all_road_10m_min_distance[points]["id"]
    //                 flightPath.midLatLang = all_road_10m_min_distance[points]['latlongs'][pt]
    //                 flightPath.addListener("click", function () {
    //                     // console.log(this.idfromopenstreet)
    //                     var infowindow = new google.maps.InfoWindow({
    //                         content: this.idfromopenstreet.toString()
    //                     });
    //                     infowindow.setPosition(this.midLatLang);
    //                     infowindow.open(map)
    //                 })

    //                 // console.log([all_road_10m_min_distance[points]['latlongs'][pt],
    //                 //     all_road_10m_min_distance[points]['latlongs'][pt+1]])
    //                 //flightPath.setMap(map);
    //                 reds.push(flightPath)
    //             }else console.log("total_points"+total_points+" , pt"+" "+pt)
    //             pt = pt + 1;
    //         }
    //     }        

    //     for (var line in reds) {
    //         reds[line].setMap(map)
    //     }
    });
}

function get_map_data_for(map,bbox){
    var color = 0000
    var index = 0

    // map.setMap(null)

    $.ajax({
        url: '/road_data/show/get_roads_from_db',
        data: {
          'csrfmiddlewaretoken': csrf_token,
            'bounds[]':bbox
      },
        type: 'POST'
      }).done(function(response){
        console.log(response['list']);


        var flightPath = new google.maps.Polyline({
            path:response['geom'],
            geodesic: true,
            strokeColor: '#000', //change color for every line
            strokeOpacity: 1.0,
            strokeWeight: 5
        }).setMap(map);



        all_road_10m_min_distance = response['list']

        for (var points in all_road_10m_min_distance) {
            total_points = all_road_10m_min_distance[points]['latlongs'].length
            pt = 0
            while (pt < total_points) {
                // color =color +0xFF ;
                index++;
                if (index % 3 == 1) {
                    color = color_red;
                } else if (index % 3 == 2) {
                    color = color_red;
                } else if (index % 3 == 0) {
                    color = color_red;
                }
                if (typeof all_road_10m_min_distance[points]['latlongs'][pt + 1] != "undefined") {
                    var flightPath = new google.maps.Polyline({
                        path:
                            [all_road_10m_min_distance[points]['latlongs'][pt],
                            all_road_10m_min_distance[points]['latlongs'][pt + 1]]
                        ,
                        geodesic: true,
                        strokeColor: '#f00', //change color for every line
                        strokeOpacity: 1.0,
                        strokeWeight: 5
                    });
                    flightPath.idfromopenstreet = all_road_10m_min_distance[points]["id"]
                    flightPath.midLatLang = all_road_10m_min_distance[points]['latlongs'][pt]
                    flightPath.addListener("click", function () {
                        // console.log(this.idfromopenstreet)
                        var infowindow = new google.maps.InfoWindow({
                            content: this.idfromopenstreet.toString()
                        });
                        infowindow.setPosition(this.midLatLang);
                        infowindow.open(map)
                    })

                    // console.log([all_road_10m_min_distance[points]['latlongs'][pt],
                    //     all_road_10m_min_distance[points]['latlongs'][pt+1]])
                    //flightPath.setMap(map);
                    reds.push(flightPath)
                }else console.log("total_points"+total_points+" , pt"+" "+pt)
                pt = pt + 1;
            }
        }        

        for (var line in reds) {
            reds[line].setMap(map)
        }
    });
}

function CenterControl(controlDiv, map) {
    var chicago = { lat: 19.133050, lng: 72.913381 };

    // Set CSS for the control border.
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
    controlText.innerHTML = 'Clear all Markers';
    controlUI.appendChild(controlText);

    // Setup the click event listeners: simply set the map to Chicago.
    controlUI.addEventListener('click', function () {
        // map.setCenter(chicago);
        for (var m in markers) {
            markers[m].setMap(null)
        }
        markers = []
    });

}

// function toggleCheckbox(evt) {
//     // console.log(evt.value    + evt.checked)

//     if (map == undefined) {
//         alert("map not initialied");
//         return
//     }
//     if (evt.value == "red" && evt.checked) {
//         for (var line in reds) {
//             reds[line].setMap(map)
//         }
//         for (var line in greens) {
//             greens[line].setMap(null)
//         }
//     } else if (evt.value == "green" && evt.checked) {
//         for (var line in reds) {
//             reds[line].setMap(null)
//         }
//         for (var line in greens) {
//             greens[line].setMap(map)
//         }
//     } else if (evt.value == "both" && evt.checked) {
//         for (var line in reds) {
//             reds[line].setMap(map)
//         }
//         for (var line in greens) {
//             greens[line].setMap(map)
//         }
//     } else {
//         alert("Ooops Something bad")
//     }
// }


function sleep(milliseconds) {
    const date = Date.now();
    let currentDate = null;
    do {
      currentDate = Date.now();
    } while (currentDate - date < milliseconds);
  }