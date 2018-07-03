
// earthquake geojson
let queryUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_month.geojson"
//var queryUrl = "http://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2014-01-01&endtime=" + "2014-01-02&maxlongitude=-69.52148437&minlongitude=-123.83789062&maxlatitude=48.74894534&minlatitude=25.16517337";


// API link to fetch our geojson data of earthquakes
var APIlink_plates = "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json"

// define a function to scale the magnitdue
function markerSize(magnitude) {
    return magnitude * 3;
};

// Perform a GET request to the query URL
d3.json(queryUrl, function(data) {
    // Once we get a response, send the data.features object to the createEarthquakes function
   console.log(data);
   createEarthquakes(data.features);
   // Here we create a timeline control object on our map.
   var timelineControl = L.timelineSliderControl({
    formatOutput: function(date) {
      return new Date(date).toString();
    },
    // Setting the number of 'ticks' or frames that will be displayed on our map.
    steps: 2000
  });

  // We also create the timeline layer.
  var timeline = L.timeline(data, {
    getInterval: getInterval,
    pointToLayer: function(layerData, latlng) {
      return L.circleMarker(latlng, {
        radius: layerData.properties.mag * 6,
        color: getColor(layerData.properties.mag),
        opacity: 0.75,
        fillOpacity: 0.75,
        weight: 0
      }).bindPopup(
        "Magnitude: " +
        layerData.properties.mag +
        "<br>Location: " +
        layerData.properties.place
      );
    }
  });
  timelineControl.addTo(map);
  timelineControl.addTimelines(timeline);
  timeline.addTo(timelineLayer);
  timelineLayer.addTo(map);
  });

// Perform a GET request to the plates URL
d3.json(APIlink_plates, function(data) {
    // Once we get a response, send the data.features object to the createEarthquakes function
   console.log(data);
   createPlates(data);
  });




  // function for color based on magnitude
  function adjustColor(magnitude){
    let GreenScaler = 300 - Math.round(magnitude * 40)
    return `rgb(66, ${GreenScaler}, 88)`
  }



  function createEarthquakes(earthquakeData){  
  // Define a function we want to run once for each feature in the features array
  // Give each feature a popup describing the place and time of the earthquake
  function onEachQuake(feature, layer) {
    layer.bindPopup("<h3>" + feature.properties.place +
      "</h3><hr><p>" + new Date(feature.properties.time) + "</p>" + 
      "</h3><hr><p>" + "Magnitude: " + feature.properties.mag + "</p>");
    
        };

  // Create a GeoJSON layer containing the features array on the earthquakeData object
  // Run the onEachQuake function once for each piece of data in the array
  let earthquakes = L.geoJSON(earthquakeData, {
    pointToLayer: function(geoJsonPoint, latlng){
        return L.circleMarker(latlng, { radius: markerSize(geoJsonPoint.properties.mag) });
    },

    style: function (geoJsonFeature) {
        return {
            fillColor: adjustColor(geoJsonFeature.properties.mag),
            fillOpacity: 0.7,
            weight: 0.1,
            color: 'black'

        }
    },

    onEachQuake: onEachQuake,
    


    
  });

// Sending our earthquakes layer to the createMap function
createMap(earthquakes);

};



// create a layer group for faultlines

let tectonicplates = new L.LayerGroup();

function createPlates(PlateData){
    function onEachPlate(feature, layer){
        layer.bindPopup("<h3> Plate A: " + feature.properties.PlateA + "Plate B: " + feature.properties.PlateB +  "</h3>");
          };
    L.geoJSON(PlateData,{
        color: "#F26157",
        weight: 1.5
        }).addTo(tectonicplates);

        // add layer to map
        tectonicplates.addTo(map)
    };



function createMap(earthquakes){
    console.log('creating map...')

    let accessToken = "access_token=pk.eyJ1IjoiYnJ5YW5sb3dlIiwiYSI6ImNqZ3p2bThxNTA4M3Yyd25vdGQxY2xqeXQifQ.URpIhwM_YJcAJYOyzbZEdQ"

    let streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?" + 
            accessToken),
    
     darkMap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/dark-v9/tiles/256/{z}/{x}/{y}?" + 
            accessToken),
    
     highContrastMap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/outdoors-v10/tiles/256/{z}/{x}/{y}?" + 
            accessToken),
    
     SatelliteMap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/satellite-v9/tiles/256/{z}/{x}/{y}?" + 
            accessToken);



    let baseMaps = {
        "Street Map": streetmap,
        "Dark map": darkMap,
        "Satellite map": SatelliteMap,
        "High Contrast map": highContrastMap
    };

    //console.log("baseMaps", baseMaps)
    
    let overlayMaps = {
        Earthquakes: earthquakes,
        "Tectonic Plates": tectonicplates 
        
    };
    //console.log('overlayMaps', overlayMaps)

    // Create a map object
    let myMap = L.map("map", {
      center: [37.09, -95.71],
      zoom: 5,
      layers: [streetmap, earthquakes]
    });

    // Create a layer control
  // Pass in our baseMaps and overlayMaps
  // Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps).addTo(myMap);

    
    // create legend
    let legend = L.control({position:"bottomleft"});

    legend.onAdd = function(map) {

        let div = L.DomUtil.create('div'),
            // the magintude keys to be displayed on DOM   
            keys = [0, 1, 2, 3, 4, 5, 6],
            labels = [];

        div.innerHTML += "<h5 style='margin:2px background-color: bisque;'>Magnitude</h5>"
        
        for (let i = 0; i < keys.length; i++){
            div.innerHTML += '<i style="width:10px; height:10px; margin-right:5px; background-color:'+ adjustColor(keys[i]) + '">___</i>' + 
            keys[i] + (keys[i + 1] ? '&ndash;' + keys[i + 1] + '<br>': '+');
        }
    
        return div;

    };
    legend.addTo(myMap);


};






