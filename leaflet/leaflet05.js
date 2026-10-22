// Inicializar mapa con soporte Canvas para alto rendimiento con más de 13.000 tramos de calles
var mymap = L.map('map', {
	preferCanvas: true
}).setView([-25.296, -57.60], 13);

// Capa base de OpenStreetMap
var osm = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
	maxZoom: 19,
	attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(mymap);

// Capa GeoJSON de Calles
var capaCalles = L.geoJson(calles, {
	style: function (feature) {
		return {
			color: '#e74c3c',
			weight: 2,
			opacity: 0.85
		};
	},
	onEachFeature: function (feature, layer) {
		if (feature.properties) {
			var nombre = feature.properties.nombre || 'Sin nombre';
			var abrev = feature.properties.abreviado ? '<br><i>(' + feature.properties.abreviado + ')</i>' : '';
			var longitud = feature.properties.longitud_m ? '<br><small>Longitud: ' + feature.properties.longitud_m + ' m</small>' : '';
			layer.bindPopup('<b>' + nombre + '</b>' + abrev + longitud);
		}
	}
}).addTo(mymap);

// Ajustar la vista para encuadrar toda la red de calles
mymap.fitBounds(capaCalles.getBounds());

// Control de capas
var baseMaps = {
	'OpenStreetMap': osm
};

var overlayMaps = {
	'Calles de Asunción': capaCalles
};

L.control.layers(baseMaps, overlayMaps, { collapsed: false }).addTo(mymap);

// Evento de clic en el mapa
var popup = L.popup();

function onMapClick(e) {
	popup
		.setLatLng(e.latlng)
		.setContent('Hiciste clic en el mapa en ' + e.latlng.toString())
		.openOn(mymap);
}

mymap.on('click', onMapClick);
