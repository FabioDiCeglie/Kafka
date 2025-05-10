var mymap = L.map('mapid').setView([49.399482163452944, 13.473201829182102], 3);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(mymap);

mapMarkers1 = [];

var flightIcon = L.icon({
  iconUrl: 'static/airplane.png',
  iconSize:     [30, 30], // size of the icon
  popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
});

var source = new EventSource('/topic/flightdata'); 
source.addEventListener('message', function(e){

  console.log('Message');
  obj = JSON.parse(e.data);
  console.log(obj);

  if(obj.airline == 'Ryanair') {
    for (var i = 0; i < mapMarkers1.length; i++) {
      mymap.removeLayer(mapMarkers1[i]);
    }
    marker1 = L.marker([obj.latitude, obj.longitude], {icon: flightIcon}).addTo(mymap);
    if (mapMarkers1.length > 0) {
      line1 = L.polyline([mapMarkers1[mapMarkers1.length-1].getLatLng(),marker1.getLatLng()], {color:'blue'}).addTo(mymap);
    }
    mapMarkers1.push(marker1);
  }
  
  if(obj.airline == 'Lufthansa') {
    for (var i = 0; i < mapMarkers5.length; i++) {
      mymap.removeLayer(mapMarkers5[i]);
    }
    marker5 = L.marker([obj.latitude, obj.longitude], {icon: flightIcon}).addTo(mymap);
    if (mapMarkers5.length > 0) {
      line5 = L.polyline([mapMarkers5[mapMarkers5.length-1].getLatLng(),marker5.getLatLng()], {color:'yellow'}).addTo(mymap);
    }
    mapMarkers5.push(marker5);
  }
}, false);