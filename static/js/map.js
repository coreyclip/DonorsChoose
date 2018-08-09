

	
	
	
	var map = L.map('map').setView([37.8, -96], 4);

	L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		id: 'mapbox.high-contrast',
		accessToken: 'pk.eyJ1IjoiY29yZXljbGlwIiwiYSI6ImNqa2t0bm04dDBnYjAza3BiN2cxZjM0dGUifQ.BAX8W867DjXCDSOVVZ5RFw'
	}).addTo(map);


	// control that shows state info on hover
	var info = L.control();

	info.onAdd = function (map) {
		this._div = L.DomUtil.create('div', 'info');
		this.update();
		return this._div;
	};

	info.update = function (props) {
		this._div.innerHTML = '<h4>Approval By State</h4>' +  (props ?
			'<b style="color:black; font-weight: 900">' + props.name + '</b><br /> <b style="color:black; font-weight: 800">' + Math.round(props.approval * 100) + '% approved</b> <br />' + 
			'<b style="color:black; font-weight: 800">Avg. project cost: $' + Math.round(props.average_price) + '</b>'
			: 'Hover over a state');
		
	};

	info.addTo(map);


	// get color depending on population density value
	function getColor(d) {
		return d > .89 ? '#800026' :
				d > .87  ? '#BD0026' :
				d > .86  ? '#E31A1C' :
				d > .85  ? '#FC4E2A' :
				d > .84   ? '#FD8D3C' :
				d > .82   ? '#FEB24C' :
				d > .81   ? '#FED976' :
							'#FFEDA0';
	}

	function style(feature) {
		return {
			weight: 2,
			opacity: 1,
			color: 'white',
			dashArray: '3',
			fillOpacity: 0.7,
			fillColor: getColor(feature.properties.approval)
		};
	}

	function highlightFeature(e) {
		var layer = e.target;

		layer.setStyle({
			weight: 5,
			color: '#666',
			dashArray: '',
			fillOpacity: 0.7
		});

		if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
			layer.bringToFront();
		}

		info.update(layer.feature.properties);
	}

	var geojson;

	function resetHighlight(e) {
		geojson.resetStyle(e.target);
		info.update();
	}

	function zoomToFeature(e) {
		map.fitBounds(e.target.getBounds());
	}

	function onEachFeature(feature, layer) {
		layer.on({
			mouseover: highlightFeature,
			mouseout: resetHighlight,
			click: zoomToFeature
		});
	}

	geojson = L.geoJson(cleanStateData, {
		style: style,
		onEachFeature: onEachFeature
	}).addTo(map);

	map.attributionControl.addAttribution('Population data &copy; <a href="http://DonorsChoose.org/">DonorsChoose.org</a>');
























