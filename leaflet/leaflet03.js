//https://mappinggis.com/2013/06/como-crear-un-mapa-con-leaflet/s
var mymap = L.map('map').setView([-23.986253, -56.865234], 8);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(mymap);

L.marker([-23.986253, -56.865234]).addTo(mymap)
	.bindPopup("<b>Marcador</b><br />Soy un popup").openPopup();

L.circle([51.508, -0.11], 500, {
	color: 'red',
	fillColor: '#f03',
	fillOpacity: 0.5
}).addTo(mymap).bindPopup("I am a circle.");

L.polygon([
	[51.509, -0.08],
	[51.503, -0.06],
	[51.51, -0.047]
]).addTo(mymap).bindPopup("I am a polygon.");


L.geoJson(distrito, {
	onEachFeature: function (feature, layer) {
		layer.bindPopup('<h1>' + feature.properties.DEPARTAMEN + '</h1><p>Distrito: ' + feature.properties.DISTRITO + '</p>');
	}
}).addTo(mymap);

var popup = L.popup();

function onMapClick(e) {
	popup
		.setLatLng(e.latlng)
		.setContent("You clicked the map at " + e.latlng.toString() + feature.properties.DISTRITO)
		.openOn(mymap);
}

mymap.on('click', onMapClick);
