var mymap = L.map('mapid').setView([49.399482163452944, 13.473201829182102], 3);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(mymap);

mapMarkers1 = [];
mapMarkers5 = [];

var flightIcon = L.icon({
  iconUrl: 'airplane.png',
  iconSize:     [30, 30], // size of the icon
  popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});

// Establishes a persistent connection to the server endpoint '/topic/flightdata'.
// This allows the server to stream data (Server-Sent Events or SSE) to the client
// in real-time, which is used here to receive live flight data updates.
var source = new EventSource('/topic/flightdata'); 
source.addEventListener('message', function(e){

  console.log('Message');
  obj = JSON.parse(e.data);
  console.log(obj);

  // Check if the airline is 'Ryanair'
  if(obj.airline == 'Ryanair') {
    // Remove all existing markers for Ryanair flights
    for (var i = 0; i < mapMarkers1.length; i++) {
      mymap.removeLayer(mapMarkers1[i]);
    }

    // Create a new marker for the current flight
    marker1 = L.marker([obj.latitude, obj.longitude], {icon: flightIcon}).addTo(mymap);

    // If there are existing markers, draw a line connecting the previous marker to the new marker
    if (mapMarkers1.length > 0) {
      line1 = L.polyline([mapMarkers1[mapMarkers1.length-1].getLatLng(),marker1.getLatLng()], {color:'blue'}).addTo(mymap);
    }

    // Add the new marker to the list of markers
    mapMarkers1.push(marker1);
  }
  
  // Check if the airline is 'Lufthansa'
  if(obj.airline == 'Lufthansa') {
    // Remove all existing markers for Lufthansa flights
    for (var i = 0; i < mapMarkers5.length; i++) {
      mymap.removeLayer(mapMarkers5[i]);
    }

    // Create a new marker for the current flight
    marker5 = L.marker([obj.latitude, obj.longitude], {icon: flightIcon}).addTo(mymap);

    // If there are existing markers, draw a line connecting the previous marker to the new marker
    if (mapMarkers5.length > 0) {
      line5 = L.polyline([mapMarkers5[mapMarkers5.length-1].getLatLng(),marker5.getLatLng()], {color:'yellow'}).addTo(mymap);
    }

    // Add the new marker to the list of markers
    mapMarkers5.push(marker5);
  }
}, false);