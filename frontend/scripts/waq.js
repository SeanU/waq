
//Initialize to get global scope
var map;            // A scaled graphical representation of the ground viewed from above
var emphMarker;     // This is the marker that will be used to highlight a location
var dataSummary;       // To hold a percentage value of the "goodness" of the current data set
var dat;
var markers=[];
var predictionTableNumber = 1;


function initMap() {

    var myLatLng = {lat: 37.8714258, lng: -122.258618}; // This is South Hall, Berkeley

    map = new google.maps.Map(document.getElementById('map'), {
    zoom: 12,
    scaleControl: true,
    center: myLatLng,
    minZoom:10,
    disableDoubleClickZoom: true

    });                

    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    //map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
    var im_click_loc = {
    url: 'images/bluestar.png',
    // size: new google.maps.Size(16, 16),
    origin: new google.maps.Point(0, 0),
    anchor: new google.maps.Point(0, 20)
    };


    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
      searchBox.setBounds(map.getBounds());
    });

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

    // Drop a pin and fetch modeled pollutants on double-click
    google.maps.event.addListener(map, "dblclick", function(event) {
        // place a marker
        placeMarker(event.latLng);
        console.log('Marker placed at ', event.latLng);
        // display the lat/lng in your form's lat/lng fields
        //document.getElementById("latFld").value = event.latLng.lat();
        //document.getElementById("lngFld").value = event.latLng.lng();
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
        icon: im_click_loc,
        size:16,
        draggable:true,
        visible:false
        });


    var timeout;
    resetSummaryChart();
    google.maps.event.addListener(map, 'bounds_changed', function () {
        window.clearTimeout(timeout);
        timeout = window.setTimeout(function () {
        redraw(markers);
        },500);
    })
        // Enable filters to re-query data
        $('#AirCheck')[0].addEventListener('change', function (){redraw(markers)}, false);
        $('#WaterCheck')[0].addEventListener('change', function (){redraw(markers)}, false);
        $('#pollutantDropdown').change( function(){redraw(markers)});
        $('#statusDropdown').change(function(){redraw(markers)});

}; //end of initMap


function redraw(markers) {
    console.log('Redrawing');
    resetSummaryChart();
  
    var bounds = map.getBounds();
    var ne = bounds.getNorthEast(); // LatLng of the north-east corner
    var sw = bounds.getSouthWest(); // LatLng of the south-west corder
    var nw = new google.maps.LatLng(ne.lat(), sw.lng());
    var se = new google.maps.LatLng(sw.lat(), ne.lng());                                                
    
    console.log("Markers: ", markers);

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


    fetchSites(ne,sw,map, markerCluster);
    resetSummaryChart();
    populateTable();
      

}



function placeMarker(location) {
    var contentString = 'Dambyote!';

    console.log(location);
    var infowindow = new google.maps.InfoWindow({
          content: fetchInfoWindowHeader(location)
        });

    populateMarkerTable(location);
    var im_dog = {
            url: 'images/waqdog.png',
            // size: new google.maps.Size(16, 16),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(0, 0)
            };


    var marker = new google.maps.Marker({
        position: location, 
        map: map,
        icon: 'images/waqdog.png'
    });

    marker.addListener('click', function() {
          infowindow.open(map, marker);
        });

    marker.addListener('dblclick', function() {
      marker.setMap(null);
    });


    infowindow.open(map,marker);

    // add marker in markers array
    //markers.push(marker);

} // end of placeMarker

function fetchInfoWindowHeader(){
    var headerMarkup = `
    <div class="infowindow">
        <table class='markertable' id="markertable`+predictionTableNumber+`">
            <thead>
                <tr>
                    <th data-formatter="CardFormatter"> Contaminant </th>
                    <th> Estimated Status </th>
                </tr>
            </thead>
        </table>
    </div>`;

            return headerMarkup;

}

function populateMarkerTable(loc) {
    
    var modelWaterURL = 'http://api.waq.dog:5000/getPrediction?type=Water&lat=' + loc.lat() + '&lng=' + loc.lng();
    var modelAirURL = 'http://api.waq.dog:5000/getPrediction?type=Air&lat=' + loc.lat() + '&lng=' + loc.lng();


    

    $.getJSON(modelWaterURL, function(thisPrediction){

        $.each(thisPrediction,function(datapoint){

            thisRow = thisPrediction[datapoint];
            console.log('Datapoint: ', datapoint);
            $('#markertable'+predictionTableNumber+' tr:last').after('<tr><td data-field=status>'+thisRow.contaminant+'</td><td>'+thisRow.status+'</td></tr>');
            
        });

    console.log('Prediction: ', thisPrediction);
    predictionTableNumber += 1;

    });
};


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
        var newPosition = new google.maps.LatLng(parseFloat(marker.position.lat().toFixed(5)), parseFloat(marker.position.lng().toFixed(5)));
        console.log(newPosition);
        emphMarker.setPosition(newPosition);
        console.log('Table: \n', $('#table'));

        // Scan the table to find the matching row(s) & highlight it/them.
        // # Start with i=3 to skip the header rows end a -1 to skip footer
        for (var i = 0, len = dtNodes.length-2; i<len; i++) {
            console.log(dtData.length, i);
            thisLatFloat = parseFloat(dtData[i].lat).toFixed(5);
            thisLonFloat = parseFloat(dtData[i].lng).toFixed(5);
            var thisPosition = new google.maps.LatLng(thisLatFloat,thisLonFloat);

            console.log('This Position: ', Number(thisPosition.lat()).toFixed(5), Number(thisPosition.lng()).toFixed(5), '  New Position: ', Number(newPosition.lat()).toFixed(5), Number(newPosition.lng()).toFixed(5));

                if (thisPosition.equals(newPosition)){
                    //Highlight any row with a matching location
                    console.log('dtn',dtNodes);
                    dtNodes[i+1].classList.add('success');
                    console.log('Row/marker match! Row=', i, '. ', thisPosition, newPosition);
                    
                    var scrollPx = (i-5)/(len+1) * $table[0].scrollHeight;
                    console.log('Scroll Px: ', scrollPx, ' / ', $table[0].scrollHeight);
                    $table.bootstrapTable('scrollTo',scrollPx);
                    //$table[0].scrollIntoView();
                }

            };
};
}

function getFilterStates(){
    // Returns a string that can be used directly in the API
    console.log('Fetching current filter states.');
    var polStat  = $('#pollutantDropdown :selected').text();
    var statStat = $('#statusDropdown :selected').text();
    var waterStat = $('#WaterCheck')[0].checked;
    var airStat = $('#AirCheck')[0].checked;

    console.log('States: ', polStat, statStat,waterStat,airStat);

    var outString = ''

    if ( (polStat != '')&(polStat != 'Pollutant (Any)') ){
        outString += '&contaminant=' + polStat;
    }

    if ( (statStat != '')&(statStat != 'Status (Any)') ){
        outString += '&status=' + statStat;
    }

    if (airStat && !waterStat){
        outString += '&type=Air';
    };
    if ((!airStat && waterStat)){
        outString += '&type=Water';
    };

    // Ignore case where both are unchecked

    return outString

}
function fetchSites(ne,sw,map, markerCluster) {
    
    resetSummaryChart(); //sets the summary plot bars to zero
    markerCluster.resetViewport(); // present a clean image after zooming and panning
    data=null;

    $('#statusDropdown :selected').text();

    var data_api_url = "http://api.waq.dog:8080/getMeasurements?";

    data_api_url += 'SWLat='+sw.lat() + '&SWLon=' + sw.lng() +'&NELat='+ne.lat() + '&NELon='+ ne.lng();
    data_api_url += getFilterStates();

    console.log(data_api_url);

    //var sensorMarkers = [];


    // ########. Fetch water data, process, and add to map
    $.getJSON(data_api_url, function(data) {

    //data is the JSON string
        
        console.log('Number of return datapoints: '+data.length);

        var image = 'http://findicons.com/files/icons/1156/fugue/16/water.png';
        var im_green = {
            url: 'images/greenwater.png',
            // size: new google.maps.Size(16, 16),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(0, 0)
            };

        var im_amber = {
            url: 'images/amberwater.png',
            // size: new google.maps.Size(16, 16),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(0, 0)
            };
        
        var im_red = {
            url: 'images/redwater.png',
            // size: new google.maps.Size(16, 16),
            origin: new google.maps.Point(0, 0),
            anchor: new google.maps.Point(0, 0)
            };

        
        // loop through each point returned from the API
        $.each(data,function(datapoint){

            thisRow = data[datapoint];

            var thisLatLng = {lat: Number(thisRow.lat), lng: Number(thisRow.lng)};
            var thisColor = thisRow.status.substring(0,5);
            
            //console.log(thisColor);

            if (thisColor.substring(0,3)=='red'){
                thisIcon = im_red;
                //thisLabel = "\u2620";
                // thisLabel = "!";
                //font-size = 12;
            }
            else if (thisColor=='green'){
                thisIcon=im_green;
                // thisLabel='.';
            }
            else if (thisColor=='amber'){
                thisIcon=im_amber;
                // thisLabel="*";
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
                size: thisSize
                // label: thisLabel
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
            
            //sensorMarkers.push(thismarker);
            markers.push(thismarker);
            markerCluster.addMarker(thismarker);
        });
        populateTable(data,clearOld=true);
        makeSummaryChart(data); 
    });

return markers;

}  // end of function fetchSites

//################################################################
// Enable a clickable row that kicks an action turns green

function populateTable(dat,clearOld=false) {
    if (dat){
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
    }
}; // end of function populateTable




// This formats the "baseball cards" for the contaminants in the table
function CardFormatter(value, row, index) {
    if (value=="Lead"){
        if (row.contaminant_type.toLowerCase()=='air'){
            return "<a href='pollutantCards/lead_air.html' target='_blank'>"+value+"</a>";
        }
        else{
            return "<a href='pollutantCards/lead_water.html' target='_blank'>"+value+"</a>";   
        }
    }
    else{
        return "<a href='pollutantCards/"+row.contaminant.toLowerCase()+".html' target='_blank'>"+value+"</a>";
    }
}


function SigFigFormatter(value, row, index) {
    return Number(Number(value).toPrecision(3)).toExponential();
}

function resetSummaryChart() {
    var greenboxair = $('#green-prop-box-air');
    var yellowboxair = $('#amber-prop-box-air');
    var redboxair = $('#red-prop-box-air');

    greenboxair[0].style.width = 1+"px";
    yellowboxair[0].style.width = 1+"px";
    redboxair[0].style.width = 1+"px";

    var greenboxwater = $('#green-prop-box-water');
    var yellowboxwater = $('#amber-prop-box-water');
    var redboxwater = $('#red-prop-box-water');

    greenboxwater[0].style.width = 1+"px";
    yellowboxwater[0].style.width = 1+"px";
    redboxwater[0].style.width = 1+"px";
}

function makeSummaryChart(data) {
    console.log('Populating summary chart.');

    var greenboxAir= $('#green-prop-box-air');
    var yellowboxAir = $('#amber-prop-box-air');
    var redboxAir = $('#red-prop-box-air');
    var greenboxWater = $('#green-prop-box-water');
    var yellowboxWater = $('#amber-prop-box-water');
    var redboxWater= $('#red-prop-box-water');


    var greenCountAir = 0;
    var yellowCountAir = 0;
    var redCountAir = 0;
    var greenCountWater = 0;
    var yellowCountWater = 0;
    var redCountWater = 0;

    // Compute props
    $.each(data, function(datapoint){

        thisRow = data[datapoint];
        //console.log('This row: ', data);

        if (thisRow.contaminant_type=='Air'){
            if (thisRow.status=="green"){
                greenCountAir+=1;
            }
            else if (thisRow.status=="amber"){
                yellowCountAir+=1;
            }
            else if (thisRow.status=="red"){
                redCountAir+=1;
            }
            else {
                console.log("Error: Bad status for point ", thisRow.status);
            }
        }
        else {

            if (thisRow.status=="green"){
                greenCountWater+=1;
            }
            else if (thisRow.status=="amber"){
                yellowCountWater+=1;
            }
            else if (thisRow.status=="red"){
                redCountWater+=1;
            }
            else {
                console.log("Error: Bad status for point ", thisRow.status);
            }
        }

    });

    var totalCountAir = greenCountAir + yellowCountAir + redCountAir;
    var totalCountWater = greenCountWater + yellowCountWater + redCountWater;
    
    console.log(' Water Total Count: ', totalCountWater);
    console.log(' Water Green Count: ' + greenCountWater);
    console.log(100*greenCountWater/totalCountWater + '%');


    // Set box widths (Air)
    if (totalCountAir >= 1){
        greenboxAir[0].style.width = 100* greenCountAir/totalCountAir + '%';//'5%'
        yellowboxAir[0].style.width = 100*yellowCountAir/totalCountAir + '%';//'5%'
        redboxAir[0].style.width = 100*redCountAir/totalCountAir + '%';//'5%'
    }

    else {
        // If there are no data, don't show the bars
        greenboxAir[0].style.width = '0%';
        yellowboxAir[0].style.width = '0%';
        redboxAir[0].style.width = '0%';
    }

    // Set box widths (Water)
    if (totalCountWater >= 1){
        greenboxWater[0].style.width = 100* greenCountWater/totalCountWater + '%';//'5%'
        yellowboxWater[0].style.width = 100*yellowCountWater/totalCountWater + '%';//'5%'
        redboxWater[0].style.width = 100*redCountWater/totalCountWater + '%';//'5%'
    }

    else {
        // If there are no data, don't show the bars
        greenboxWater[0].style.width = '0%';
        yellowboxWater[0].style.width = '0%';
        redboxWater[0].style.width = '0%';
    }


} //end summary chart function



// Enable navigation bar buttons
$('#HomeButton').click(function() {
    $('.navpanebutton').removeClass("current");
    $('#homepane').removeClass("hidden");
    $('#knowmorepane').addClass("hidden");
    $('#contactuspane').addClass("hidden");  
    $('#HomeButton').addClass("current");
    });

$('#KnowMoreButton').click(function() {
    $('.navpanebutton').removeClass("current");
    $('#homepane').addClass("hidden");
    $('#contactuspane').addClass("hidden");
    $('#knowmorepane').removeClass("hidden");   
    $('#KnowMoreButton').addClass("current");
    });

$('#ContactUsButton').click(function() {
    $('.navpanebutton').removeClass("current");
    $('#contactuspane').removeClass("hidden");
    $('#knowmorepane').addClass("hidden");  
    $('#homepane').addClass("hidden");   
    $('#ContactUsButton').addClass("current");
    });

$('#BigMapButton').click(function() {
    $('.mapsizebutton').removeClass('current');
    $('#BigMapButton').addClass('current');
    $('#map-container').css('width','70%');
    $('#tools-container').css('width','29.5%');
    });

$('#BigTableButton').click(function() {
    $('.mapsizebutton').removeClass('current');
    $('#BigTableButton').addClass('current');
    $('#map-container').css('width','35%');
    $('#tools-container').css('width','64.5%');
    });

