//https://mappinggis.com/2013/06/como-crear-un-mapa-con-leaflet/s
var mymap = L.map('map').setView([-23.986253, -56.865234], 8);

L.geoJson(departamento).addTo(mymap);
//L.geoJson(distrito).addTo(mymap);

var popup = L.popup();

function onMapClick(e) {
	popup
		.setLatLng(e.latlng)
		.setContent('texto=' + feature.properties.DEPARTAMEN)
		.openOn(mymap);
}

mymap.on('click', onMapClick);
//mymap.bindPopup('<h1>'+feature.properties.DEPARTAMEN+'</h1><p>name: '+feature.properties.DISTRITO+'</p>')
