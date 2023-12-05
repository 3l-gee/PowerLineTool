import TLMDATA from './TLMSimpleFeatures.json' assert {type : 'json'}

//Cosnt
/////////////////////////////////////////////////////////////////////

var initialSelectedFeatures = $('#selectedFeatures tbody').html();

function featuresStyle (feature, resolution) {
  // Get the zoom level from the map
  const zoom = map.getView().getZoom();

  // Get the LineString geometry
  const geometry = feature.getGeometry();
  const coordinates = geometry.getCoordinates();

  // Create styles array
  const styles = [];

  // If zoom is greater than or equal to 14, apply the red stroke style
  if (zoom <= 8) {
    styles.push(new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: 'black',
        width: 2,
      }),
    }));
  } else {
    // Style for the first point
    styles.push(new ol.style.Style({
      geometry: new ol.geom.Point(coordinates[0]),
      image: new ol.style.RegularShape({
        points: 3,
        rotation: Math.PI * 4 / 3,
        radius: 8, // Adjust the radius based on the zoom level
        fill: new ol.style.Fill({
          color: 'blue',
        }),
      }),
    }));

    // Style for in-between points
    for (let i = 1; i < coordinates.length - 1; i++) {
      styles.push(new ol.style.Style({
        geometry: new ol.geom.Point(coordinates[i]),
        image: new ol.style.Circle({
          radius: 3, // Adjust the radius based on the zoom level
          fill: new ol.style.Fill({
            color: 'black',
          }),
        }),
      }));
    }

    // Style for the last point
    styles.push(new ol.style.Style({
      geometry: new ol.geom.Point(coordinates[coordinates.length - 1]),
      image: new ol.style.RegularShape({
        points: 3,
        rotation: 0 + Math.PI / 3,
        radius: 8, // Adjust the radius based on the zoom level
        fill: new ol.style.Fill({
          color: 'red',
        }),
      }),
    }));

    styles.push(new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: 'black',
        width: 2,
      }),
    }));
  }

  return styles;
}


function selected (feature, resolution) {
  // Get the zoom level from the map
  const zoom = map.getView().getZoom();

  // Get the LineString geometry
  const geometry = feature.getGeometry();
  const coordinates = geometry.getCoordinates();

  // Create styles array
  const styles = [];

  // If zoom is greater than or equal to 14, apply the red stroke style
  if (zoom <= 8) {
    styles.push(new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: '#FFA7D3',
        width: 10,
      }),
    }));
  } else {
    // Style for the first point
    styles.push(new ol.style.Style({
      geometry: new ol.geom.Point(coordinates[0]),
      image: new ol.style.RegularShape({
        points: 3,
        rotation: Math.PI * 4 / 3,
        radius: 16, // Adjust the radius based on the zoom level
        fill: new ol.style.Fill({
          color: '#8BC5FF',
        }),
      }),
    }));

    // Style for in-between points
    for (let i = 1; i < coordinates.length - 1; i++) {
      styles.push(new ol.style.Style({
        geometry: new ol.geom.Point(coordinates[i]),
        image: new ol.style.Circle({
          radius: 3, // Adjust the radius based on the zoom level
          fill: new ol.style.Fill({
            color: 'black',
          }),
        }),
      }));
    }

    // Style for the last point
    styles.push(new ol.style.Style({
      geometry: new ol.geom.Point(coordinates[coordinates.length - 1]),
      image: new ol.style.RegularShape({
        points: 3,
        rotation: 0 + Math.PI / 3,
        radius: 16, // Adjust the radius based on the zoom level
        fill: new ol.style.Fill({
          color: '#FFD38B',
        }),
      }),
    }));

    styles.push(new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: '#FFA7D3',
        width: 10,
      }),
    }));
  }
  feature.set('zIndex', 10);
  return styles;
}

proj4.defs('EPSG:2056', '+proj=somerc +lat_0=46.95240555555556 +lon_0=7.439583333333333 +k_0=1 +x_0=2600000 +y_0=1200000 +ellps=bessel +towgs84=674.374,15.056,405.346,0,0,0,0 +units=m +no_defs');
ol.proj.proj4.register(proj4);

const WMS_TILE_SIZE = 512; // px
const TILEGRID_ORIGIN = [2420000, 1350000]; // in EPSG:2056
const TILEGRID_RESOLUTIONS = [
  4000, 3750, 3500, 3250, 3000, 2750, 2500, 2250, 2000, 1750, 1500, 1250,
  1000, 750, 650, 500, 250, 100, 50, 20, 10, 5, 2.5, 2, 1.5, 1, 0.5
];

var extent = [2420000, 1300000, 2900000, 1350000];
var projection = ol.proj.get('EPSG:2056');
projection.setExtent(extent);

var matrixIds = [];
for (var i = 0; i < TILEGRID_RESOLUTIONS.length; i++) {
  matrixIds.push(i);
}

var layerConfig_BackroundMap = {
  "attribution": "swisstopo",
  "format": "jpeg",
  "serverLayerName": "ch.swisstopo.pixelkarte-grau",
  "attributionUrl": "https://www.swisstopo.admin.ch/internet/swisstopo/fr/home.html",
  "label": "SWISSIMAGE",
  // Use 'current', if you are only interested in the latest data.
  "timestamps": [
    "current",
  ]
};

//layers 
/////////////////////////////////////////////////////////////////////

const SelectedFeatureSource = new ol.source.Vector()

const SelectedFeatureLayer = new ol.layer.Vector({
  source : SelectedFeatureSource,
  style : new ol.style.Style({
    image: new ol.style.Circle({
      radius: 3, 
      fill: new ol.style.Fill({
        color: 'orange',
      }),
    }),
    stroke: new ol.style.Stroke({
      color: 'orange',
      width: 10,
    })
  })
})

console.log(SelectedFeatureLayer)

const ActiveObstacle = new ol.layer.Tile({
  opacity: 0.1,
  minZoom : 8,
  source: new ol.source.TileWMS({
    url: `https://wms0.geo.admin.ch/?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=true&LAYERS=ch.bazl.luftfahrthindernis&LANG=en`,
    gutter: 120,
    tileGrid: new ol.tilegrid.TileGrid({
      projection: "EPSG:3857",
      tileSize: WMS_TILE_SIZE,
      origin: TILEGRID_ORIGIN,
      resolutions: TILEGRID_RESOLUTIONS
    })
  })
});


var wmtsSource = function(layerConfig) {
  var resolutions = layerConfig.resolutions || TILEGRID_RESOLUTIONS;
  var tileGrid = new ol.tilegrid.WMTS({
    origin: [extent[0], extent[3]],
    resolutions: resolutions,
    matrixIds: matrixIds
  });
  var extension = layerConfig.format || 'png';
  var timestamp = layerConfig['timestamps'][0];
  return new ol.source.WMTS(({
    url: '//wmts10.geo.admin.ch/1.0.0/{Layer}/default/' + timestamp + '/2056/{TileMatrix}/{TileCol}/{TileRow}.'+ extension,
    tileGrid: tileGrid,
    projection: projection,
    layer: layerConfig.serverLayerName,
    requestEncoding: 'REST'
  }));
};

var BackroundMap = new ol.layer.Tile({
  source: wmtsSource(layerConfig_BackroundMap)
});

const SimplifiedTLMSource = new ol.source.Vector({
  features: new ol.format.GeoJSON().readFeatures(TLMDATA, {
    featureProjection: 'EPSG:2056', // Adjust to your map's projection
  }),
});

const SimplifiedTLMLayer = new ol.layer.Vector({
  style: featuresStyle,
  source: SimplifiedTLMSource,
});

const View = new ol.View({
    // projection: 'EPSG:3857',
    // center: [893463,5943335],
    projection: 'EPSG:2056',
    center: [2600000,1200000],
    zoom: 4,
})

const map = new ol.Map({
    layers: [
      BackroundMap,
      ActiveObstacle,
      SimplifiedTLMLayer,
      SelectedFeatureLayer
    ],
    target: 'map',
    view : View

})

//Interaction
/////////////////////////////////////////////////////////////////////
const container = document.getElementById('popup');
const content = document.getElementById('popup-content');
const closer = document.getElementById('popup-closer');

const popup = new ol.Overlay({
  element: container,
  autoPan: {
    animation: {
      duration: 250,
    },
  },
});

map.addOverlay(popup);

const selectInteraction = new ol.interaction.Select({
  style: selected,
  layers: [SimplifiedTLMLayer], // Specify the layers on which the interaction will work
  multi: true,
  hitTolerance : 5
});

closer.onclick = function () {
  selectInteraction.getFeatures().clear();
  popup.setPosition(undefined);
  closer.blur();
  return false;
};

map.addInteraction(selectInteraction);

selectInteraction.on('select', function (evt) {
  const selectedFeatures = evt.selected;

  if (selectedFeatures.length > 0) {
    const extent = ol.extent.createEmpty();
    
    // Extend the extent with the geometry of each selected feature
    selectedFeatures.forEach(function (feature) {
      ol.extent.extend(extent, feature.getGeometry().getExtent());
    });

    // Calculate the center of the bounding box (extent)
    const center = ol.extent.getCenter(extent);
    var popupContent = '<table>'
    let entry = '<tr><th>ID</th><th>Linked Reg. Num.</th><th>Actions</th></tr>'
    popupContent += entry
    for (let selectedFeature of selectedFeatures){
      let featureId = selectedFeature.get("id") 

      entry =""
      entry += "<tr><td>" 
      entry += featureId
      entry += "</td><td>"
      entry += selectedFeature.get("omsMatches") 
      entry += '</td><td>';
      entry += `<button id="SelectFeature" class="action-button" data-feature-id="${featureId}">+</button>`;
      entry += '</td></tr>';
      popupContent += entry
    }
    popupContent += "</table>"
    content.innerHTML = popupContent

    const actionButtons = document.querySelectorAll('.action-button');
    actionButtons.forEach(button => {
      button.addEventListener('click', function() {
        const featureId = button.dataset.featureId;
        addFeature(featureId, "TLM");
      });
    });

    popup.setPosition(center);}
})

//BackendCall
/////////////////////////////////////////////////////////////////////

// Attach a click event handler to the button
$('#helloButton').click(function() {
  // Send an AJAX request to the server with the CSRF token
  $.ajax({
      type: 'POST',
      url: '/map/log_hello/',
      headers: {
          'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
      },
      success: function(data) {
          console.log('Server log:', data);
      },
      error: function(error) {
          console.error('Error:', error);
      }
  });
});

$('#remFeature').click(function() {
  $.ajax({
    type: 'POST',
    url: '/map/remFeature/',
    headers: {
        'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
    },
    success: function(data) {
      updateSelectedFeaturesTable();
      console.log('remFeature:', data);
    },
    error: function(error) {
        console.error('remFeature Error:', error);
    }
});
});

function getFeature(callback) {
  $.ajax({
    type: 'GET',
    url: '/map/getFeature/', 
    success: function (data) {
      console.log('getFeature:', data);
      callback(data.features);
    },
    error: function (error) {
      console.error('getFeature Error:', error);
      callback(null);
    }
  });
}

function addFeature(featureId,featureType) {
  $.ajax({
    type: 'POST',
    url: '/map/addFeature/',
    headers: {
      'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
    },
    data: {
      featureId: featureId,
      featureType : featureType
    },
    success: function(data) {
      console.log('addFeature:', data);
      updateSelectedFeaturesTable();
    },
    error: function(error) {
      console.error('addFeature Error:', error);
    }
  });
}

// HTML 
/////////////////////////////////////////////////////////////////////
function updateSelectedFeaturesTable() {
  getFeature(function(features) {
    var tableBody = $('#selectedFeatures tbody');
    tableBody.empty();
    SelectedFeatureSource.clear()

    if (features) {
      for (const [key, value] of Object.entries(features)) {
        for (let testFeature of value.coordinates.features) {
          let testFeatureObject = new ol.format.GeoJSON().readFeature(testFeature);
          SelectedFeatureSource.addFeature(testFeatureObject);
        }
    
        var row = $('<tr>')
          .append($('<td>').text(value.type))
          .append($('<td>').text(value.id))
    
        tableBody.append(row);
      }
    }
    

      console.log(tableBody);
  })
}

