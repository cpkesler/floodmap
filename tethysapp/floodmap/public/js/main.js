//Here we are declaring the projection object for Web Mercator
var projection = ol.proj.get('EPSG:3857');

//Define Basemap
//Here we are declaring the raster layer as a separate object to put in the map later
var baseLayer = new ol.layer.Tile({
    source: new ol.source.OSM({})
});

var range_length = range_list.length
var range_input = range_list[0].toString().split(".").join("")

//Define all WMS Sources:
var FloodMap =  new ol.source.TileWMS({
        url:'http://geoserver.byu.edu/arcgis/services/HANDfloodmap/Flood_' + range_input + '/MapServer/WmsServer?',

        params:{
            LAYERS:"2",
//            FORMAT:"image/png", //Not a necessary line, but maybe useful if needed later
        },
        crossOrigin: 'Anonymous' //This is necessary for CORS security in the browser
        });

var AddressPoints =  new ol.source.TileWMS({
        url:'http://geoserver.byu.edu/arcgis/services/Handfloodmap/Flood_' + range_input + '/MapServer/WmsServer?',

        params:{
            LAYERS:"0",
//            FORMAT:"image/png", //Not a necessary line, but maybe useful if needed later
        },
        crossOrigin: 'Anonymous' //This is necessary for CORS security in the browser
        });

var LandCover =  new ol.source.TileWMS({
        url:'http://geoserver.byu.edu/arcgis/services/HANDfloodmap/Flood_' + range_input + '/MapServer/WmsServer?',

        params:{
            LAYERS:"1",
//            FORMAT:"image/png", //Not a necessary line, but maybe useful if needed later
        },
        crossOrigin: 'Anonymous' //This is necessary for CORS security in the browser
        });

//Define all WMS layers
//The gauge layers can be changed to layer.Image instead of layer.Tile (and .ImageWMS instead of .TileWMS) for a single tile
var address = new ol.layer.Tile({
    source:AddressPoints
    });

var land = new ol.layer.Tile({
    source:LandCover
    });

var flood = new ol.layer.Tile({
    source:FloodMap
    }); //Thanks to http://jsfiddle.net/GFarkas/tr0s6uno/ for getting the layer working

//Set opacity of layers
flood.setOpacity(0.8);
land.setOpacity(0.8);
address.setOpacity(0.7);

sources = [AddressPoints, FloodMap, LandCover];
layers = [baseLayer, address, flood, land];

//Establish the view area. Note the reprojection from lat long (EPSG:4326) to Web Mercator (EPSG:3857)
var view = new ol.View({
        center: [-9750000, 3920000],
        projection: projection,
        zoom: 12,
    })

//Declare the map object itself.
var map = new ol.Map({
    target: document.getElementById("map"),
    layers: layers,
    view: view,
});

map.addControl(new ol.control.ZoomSlider());

//This function is ran to set a listener to update the map size when the navigation pane is opened or closed
(function () {
    var target, observer, config;
    // select the target node
    target = $('#app-content-wrapper')[0];

    observer = new MutationObserver(function () {
        window.setTimeout(function () {
            map.updateSize();
        }, 350);
    });

    config = {attributes: true};

    observer.observe(target, config);
}());

//Here we set the styles and inital setting for the slider bar (https://jqueryui.com/slider/#steps)
$(function() {
        if (window.location.search.indexOf('short_range') != -1) {
            var label_text = window.location.search.indexOf('flood_forecast') != -1 ? 'Time Step (hour):' : 'Flood Depth (meter):'
        }
        else {
            var label_text = window.location.search.indexOf('flood_forecast') != -1 ? 'Time Step (x3 hours):' : 'Flood Depth (meter):'
        }
    $( "#label" ).text(label_text)
    $( "#slider" ).slider({
      value:1,
      min: 1,
      max: range_length,
      step: 1,
      slide: function( event, ui ) {
      var range_value = range_list[ui.value - 1][1];
        $( "#amount" ).val( ui.value );
        var decimal_value = range_value.toString().split(".").join("")
        var url = 'http://geoserver.byu.edu/arcgis/services/HANDfloodmap/Flood_' + decimal_value + '/MapServer/WmsServer?';
        LandCover.setUrl(url);
        FloodMap.setUrl(url);
        AddressPoints.setUrl(url);
        $( "#house_count").text(range_list[ui.value - 1][2]);

      }
    });
    $( "#amount" ).val( $( "#slider" ).slider( "value" ) );
  });