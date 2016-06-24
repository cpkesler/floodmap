//Here we are declaring the projection object for Web Mercator
var projection = ol.proj.get('EPSG:3857');

//Define Basemap
//Here we are declaring the raster layer as a separate object to put in the map later
var baseLayer = new ol.layer.Tile({
    source: new ol.source.MapQuest({layer: 'osm'})
});

//Define all WMS Sources:
var LandCover =  new ol.source.TileWMS({
        url:'http://geoserver.byu.edu/arcgis/services/FloodMap/Flood_1/MapServer/WmsServer?',

        params:{
            LAYERS:"1",
//            FORMAT:"image/png", //Not a necessary line, but maybe useful if needed later
        },
        crossOrigin: 'Anonymous' //This is necessary for CORS security in the browser
        });

var FloodMap =  new ol.source.TileWMS({
        url:'http://geoserver.byu.edu/arcgis/services/FloodMap/Flood_1/MapServer/WmsServer?',

        params:{
            LAYERS:"0",
//            FORMAT:"image/png", //Not a necessary line, but maybe useful if needed later
        },
        crossOrigin: 'Anonymous' //This is necessary for CORS security in the browser
        });


//Define all WMS layers
//The gauge layers can be changed to layer.Image instead of layer.Tile (and .ImageWMS instead of .TileWMS) for a single tile
var land = new ol.layer.Tile({
    source:LandCover
    });

var flood = new ol.layer.Tile({
    source:FloodMap
    }); //Thanks to http://jsfiddle.net/GFarkas/tr0s6uno/ for getting the layer working

//Set opacity of layers
flood.setOpacity(0.5);
land.setOpacity(0.8);

sources = [FloodMap, LandCover];
layers = [baseLayer, flood, land];

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
    $( "#slider" ).slider({
      value:1,
      min: 1,
      max: 6,
      step: 1,
      slide: function( event, ui ) {
        $( "#amount" ).val( ui.value );
        var url = 'http://geoserver.byu.edu/arcgis/services/FloodMap/Flood_' + ui.value + '/MapServer/WmsServer?';
        LandCover.setUrl(url);
        FloodMap.setUrl(url);
      }
    });
    $( "#amount" ).val( $( "#slider" ).slider( "value" ) );
  });