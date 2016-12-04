//Initialize to get global scope
var map;            // A scaled graphical representation of the ground viewed from above
var emphMarker;     // This is the marker that will be used to highlight a location
var dataSummary;       // To hold a percentage value of the "goodness" of the current data set
var dat;

function initMap() {

    var myLatLng = {lat: 37.8714258, lng: -122.258618}; // This is South Hall, Berkeley

    map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    scaleControl: true,
    center: myLatLng
    });



    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
      searchBox.setBounds(map.getBounds());
    });

    var markers = [];
    // Listen for the event fired when the user selects a location and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
          var places = searchBox.getPlaces();

          if (places.length == 0) {
            return;
          }

          // Clear out the old markers.
          markers.forEach(function(marker) {
            marker.setMap(null);
            marker = null;
          });
          markers = [];

          // For each place, get the icon, name and location.
          var bounds = new google.maps.LatLngBounds();
          places.forEach(function(place) {
            if (!place.geometry) {
              console.log("Returned place contains no geometry");
              return;
            }
            var icon = {
              // url: place.icon,  //This edit keeps the normal markers;  the place icons are weird
              size: new google.maps.Size(71, 71),
              origin: new google.maps.Point(0, 0),
              anchor: new google.maps.Point(17, 34),
              scaledSize: new google.maps.Size(25, 25)
            };

            // Create a marker for each place.
            markers.push(new google.maps.Marker({
              map: map,
              icon: icon,
              title: place.name,
              position: place.geometry.location
            }));

            //markerCluster.addMarkers(markers)

            if (place.geometry.viewport) {
              // Only geocodes have viewport.
              bounds.union(place.geometry.viewport);
            } else {
              bounds.extend(place.geometry.location);
            }
          });
          map.fitBounds(bounds);
        });



  var marker = new google.maps.Marker({
    position: myLatLng,
    map: map,
    title: 'Hello World!'
  });

  emphMarker = new google.maps.Marker({
    position: myLatLng,
    // map: null,
    map: map,
    setAnimation: google.maps.Animation.DROP,
    icon: 'http://maps.google.com/mapfiles/kml/pal4/icon48.png',
    //icon: 'images/ios7-circle-filled.svg',
    size:16,
    draggable:true,
    visible:false
  });

  google.maps.event.addListener(map, 'bounds_changed',
      function() {
        var bounds = map.getBounds();
        console.log(bounds);
        var ne = bounds.getNorthEast(); // LatLng of the north-east corner
        var sw = bounds.getSouthWest(); // LatLng of the south-west corder
        var nw = new google.maps.LatLng(ne.lat(), sw.lng());
        var se = new google.maps.LatLng(sw.lat(), ne.lng());


        markers.forEach(function(marker) {
            marker.setMap(null);
            marker=null;
          });
          markers = [];

        var markerCluster = new MarkerClusterer(map, [],
                {
                imagePath: 'images/m',
                maxZoom: '10',
                minimumClusterSize: '6'
            });


        var sms = fetchSites(ne,sw,map, markerCluster);

      });



}; //end of initMap

function mapTableCrossLink(marker=null,e=null, row=null, $element=null){
    console.log('Map/table link function activated.  Marker: ', marker);
    emphMarker.setVisible(true);
    if (marker==null){ // if a table line was clicked
        $('.success').removeClass('success');
        $($element).addClass('success');
        console.log('Table row clicked. ', row, row.lat, row.lng );
        //emphMarker.setMap(null);
        var newPosition = new google.maps.LatLng(parseFloat(row.lat), parseFloat(row.lng));
        console.log(newPosition);
        emphMarker.setPosition(newPosition);
        //emphMarker.setMap(map);
        console.log("Element: \n", $element);
        console.log("Row: \n", row);
    }
    else { // assume a marker was clicked
        console.log('Success: ', $('.success'));
        $('.success').removeClass('success');

        var $table = $('#table');
        var dtNodes = $('tr');
        var dtData = $table.bootstrapTable('getData');

        console.log('Map marker clicked. ', marker, marker.position.lat(), marker.position.lng() );
        var newPosition = new google.maps.LatLng(parseFloat(marker.position.lat()), parseFloat(marker.position.lng()));
        console.log(newPosition);
        emphMarker.setPosition(newPosition);
        console.log('Table: \n', $('#table'));

        // Scan the table to find the matching row(s) & highlight it/them.
        // # Start with i=3 to skip the header rows end a -1 to skip footer
        for (var i = 3, len = dtNodes.length-1; i < len; i++) {
            console.log(dtData.length, i);
            thisLatFloat = parseFloat(dtData[i+1].lat);
            thisLonFloat = parseFloat(dtData[i+1].lng);
            var thisPosition = new google.maps.LatLng(thisLatFloat,thisLonFloat);
                if (thisPosition.equals(newPosition)){

                    //Highlight any row with a matching location
                    console.log('dtn',dtNodes);
                    dtNodes[i].classList.add('success');
                    console.log('Row/marker match! Row=', i, '. ', thisPosition, newPosition);

                    var scrollPx = (i-5)/(len+1) * $table[0].scrollHeight;
                    console.log('Scroll Px: ', scrollPx, ' / ', $table[0].scrollHeight);
                    $table.bootstrapTable('scrollTo',scrollPx);
                    //$table[0].scrollIntoView();
                }

            };
};
}
function fetchSites(ne,sw,map, markerCluster) {
    // REST Query Structure:
    //     /getWaterSites/:SWLat/:SWLon/:NELat/:NELon
    //     http://130.211.86.94:8080/getWaterSites/34.80/-117.040/34.99/-117.050


    markerCluster.clearMarkers(); // present a clean image after zooming and panning
    data=null;

    //var water_api_url = "http://130.211.86.94:8080/getWaterSites/";
    //var water_api_url = "http://130.211.86.94:8080/getMeasurementData/";
    var water_api_url = "http://130.211.86.94:8080/getMeasurements/Water/";
    var air_api_url = "http://130.211.86.94:8080/getMeasurements/Air/";

    console.log(ne.lat(), ne.lng());
    console.log(sw.lat(), sw.lng());

    water_api_url += sw.lat() + '/' + ne.lng() + '/' + ne.lat() + '/' + sw.lng();
    air_api_url += sw.lat() + '/' + ne.lng() + '/' + ne.lat() + '/' + sw.lng();

    water_api_url="http://130.211.86.94:8080/getMeasurements/Water/37.82710141535922/-122.03889143750001/37.915723534380355/-122.47834456250001";
    air_api_url="http://130.211.86.94:8080/getMeasurements/Air/37.82710141535922/-122.03889143750001/37.915723534380355/-122.47834456250001";

    console.log(water_api_url);
    console.log(air_api_url);

    var sensorMarkers = [];


    // ########. Fetch air data, process, and add to map
    $.getJSON(air_api_url, function(data) {

    //data is the JSON string

        console.log('Number of return datapoints: '+data.length);

        var image = 'http://findicons.com/files/icons/1156/fugue/16/water.png';
        var im_green = {
            url: 'images/green_cloud.png',
            size: new google.maps.Size(16, 16),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(0, 0)
            };

        var im_orange = {
            url: 'images/amber-cloud.png',
            size: new google.maps.Size(16, 16),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(0, 0)
            };

        var im_red = {
            url: 'images/red-cloud.png',
            size: new google.maps.Size(16, 16),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(0, 0)
            };


        // loop through each point returned from the API
        $.each(data,function(datapoint){

            thisRow = data[datapoint];

            var thisLatLng = {lat: Number(thisRow.lat), lng: Number(thisRow.lng)};
            var thisColor = thisRow.status.substring(0,5);

            //console.log(thisColor);

            if (thisColor.substring(0,3)=='Red'){
                thisIcon = im_red,
                //thisLabel = "\u2620";
                thisLabel = "!";
                //font-size = 12;
            }
            else if (thisColor=='Green'){
                thisIcon=im_green,
                thisLabel='.';
            }
            else if (thisColor=='Orange'){
                thisIcon=im_amber,
                thisLabel="*";
            }

            else {
                thisIcon=image;
            }
            //console.log(thisLatLng);

            thisTitle = '';
            thisTitle += 'Site ID: \t\t\t' + thisRow.site_id + '\n';
            thisTitle += 'Measurement: \t' + thisRow.contaminant + ' in ';

            thisTitle +=    thisRow.contaminant_type + ' (' + thisRow.contaminant_cat + ')\n';
            thisTitle += 'Value: \t\t\t' + thisRow.value + '\n';

            thisTitle += 'Measured on: \t\t' + thisRow.measurement_date + ' at ' + thisRow.measurement_time + '\n';

            thisSize = new google.maps.Size(16, 16);

            var thismarker = new google.maps.Marker({
                position: thisLatLng,
                map: map,
                icon: thisIcon,
                title: thisTitle,
                size: thisSize,
                label: thisLabel
            });

            // Add a marker click listener
            // which highlights the table row
            thismarker.addListener('click',
                function() {
                    mapTableCrossLink(marker=thismarker);
                    });

            thismarker.addListener('dblclick',
                function() {
                    console.log('Map marker double-clicked.  Centering map on marker.');
                    map.setCenter(thismarker.getPosition());
                    });


            //console.log('Pushing point')
            sensorMarkers.push(thismarker);
            markerCluster.addMarker(thismarker);
        });
        //populateTable(data,clearOld=true);
    });

    // ########. Fetch water data, process, and add to map
    $.getJSON(water_api_url, function(data) {

    //data is the JSON string

        console.log('Number of return datapoints: '+data.length);

        var image = 'http://findicons.com/files/icons/1156/fugue/16/water.png';
        var im_green = {
            url: 'images/green-water.png',
            size: new google.maps.Size(16, 16),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(0, 0)
            };

        var im_amber = {
            url: 'images/amber-water.png',
            size: new google.maps.Size(16, 16),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(0, 0)
            };

        var im_red = {
            url: 'images/red-water.png',
            size: new google.maps.Size(16, 16),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(0, 0)
            };


        // loop through each point returned from the API
        $.each(data,function(datapoint){

            thisRow = data[datapoint];

            var thisLatLng = {lat: Number(thisRow.lat), lng: Number(thisRow.lng)};
            var thisColor = thisRow.status.substring(0,5);

            //console.log(thisColor);

            if (thisColor.substring(0,3)=='Red'){
                thisIcon = im_red,
                //thisLabel = "\u2620";
                thisLabel = "!";
                //font-size = 12;
            }
            else if (thisColor=='Green'){
                thisIcon=im_green,
                thisLabel='.';
            }
            else if (thisColor=='Amber'){
                thisIcon=im_amber,
                thisLabel="*";
            }

            else {
                thisIcon=image;
            }
            //console.log(thisLatLng);

            thisTitle = '';
            thisTitle += 'Site ID: \t\t\t' + thisRow.site_id + '\n';
            thisTitle += 'Measurement: \t' + thisRow.contaminant + ' in ';

            thisTitle +=    thisRow.contaminant_type + ' (' + thisRow.contaminant_cat + ')\n';
            thisTitle += 'Value: \t\t\t' + thisRow.value + '\n';

            thisTitle += 'Measured on: \t\t' + thisRow.measurement_date + ' at ' + thisRow.measurement_time + '\n';

            thisSize = new google.maps.Size(16, 16);


            //console.log(thisLatLng);
            var thismarker = new google.maps.Marker({
                position: thisLatLng,
                map: map,
                icon: thisIcon,
                title: thisTitle,
                size: thisSize,
                label: thisLabel
            });


            thismarker.addListener('click',
                function() {
                    mapTableCrossLink(marker=thismarker);
                    });

            thismarker.addListener('dblclick',
                function() {
                    console.log('Map marker double-clicked.  Centering map on marker.');
                    map.setCenter(thismarker.getPosition());
                    });

            sensorMarkers.push(thismarker);
            markerCluster.addMarker(thismarker);
        });
        //populateTable(data);
    });

return sensorMarkers;

}  // end of function fetchSites

//################################################################
// Enable a clickable row that kicks an action turns green

function populateTable(dat,clearOld=false) {
    var $table = $('#table');
    jsonData = dat;
    // Add data to the table
    console.log('Adding ', jsonData.length, ' points to table.');
    // console.log('DT: ', typeof(jsonData));
    if (clearOld) {
        $table.bootstrapTable('load',jsonData);
    } else{
        $table.bootstrapTable('append',jsonData);
    }

    // Selecting a row highlights the position on a map
    $(function () {
        $table.on('click-row.bs.table',
            function (e, row, $element) {
                mapTableCrossLink(marker=null,e=e, row=row, $element=$element)
            });
    });
    console.log(jsonData);
    for (ii = 0; ii < jsonData.length; ii++) {
        console.log(jsonData['Status'][ii]);

    }

}; // end of function populateTable




// This formats the "baseball cards" for the contaminants in the table
function CardFormatter(value, row, index) {
  return "<a href='pollutantCards/"+row.contaminant.toLowerCase()+".html' target='_blank'>"+value+"</a>";
}


function makeSummaryChart() {
    FusionCharts.ready(function(){
    var fusioncharts = new FusionCharts({
    type: 'vbullet',
    renderAt: 'summaryChart',
    id: 'rev-bullet-2',
    width: '100%',
    height: '110%',
    dataFormat: 'json',
    dataSource: {
        "chart": {
            "theme": "fint",
            "lowerLimit": "0",
            "subCaptionFontSize": "11",
            "upperLimit": "1",
            "caption": "",
            "chartBottomMargin": "25",
            "chartTopMargin":"25",
            "chartLeftMargin":"0",
            "chartRightMargin":"0",
            "placeTicksInside":"1",
            "placeValuesInside":"1"
        },
        "colorRange": {
            "color": [{
                "minValue": "0",
                "maxValue": "1",
                "code": "#cccccc",
                "alpha": "25"
            }]
        },
        "value": "0.3",
        "target": "0.3"
    }
    }
    );
    fusioncharts.render();
    });

} //end summary chart function
