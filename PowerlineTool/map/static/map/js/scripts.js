import TLMDATA from './TLMSimpleFeatures.json' assert {type : 'json'}

//Cosnt
/////////////////////////////////////////////////////////////////////

var initialSelectedFeatures = $('#selectedFeatures tbody').html();
let ExportMaterial = {
  name : null,
  dcs : {
    originator : null,
    type : null,
    moving : null,
    group : null,
    points : [],
    jths : [],
    hospitalNearby : null,
    ownerInfo : null, 
    approvalLetterRequired : null, 
    lastModificationReport : null, 
    pending : null,
    authority : null,
    publicationTypes : null, 
    structureStatus : null, 
    legacySymbolCode : null, 
    legacyOwnerAddress : null,
    legacyOmsCMID : null, 
    legacyOmsInvoiceCMID : null, 
    legacyInvoiceAddress : null
  },
  history : null
}

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
        color: 'blue',
        width: 4,
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
      image: new ol.style.Circle({
        radius: 100, // Adjust the radius based on the zoom level
        fill: new ol.style.Fill({
          color: 'black',
        }),
      }),
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
      image: new ol.style.Circle({
        radius: 10, // Adjust the radius based on the zoom level
        fill: new ol.style.Fill({
          color: '#FFA7D3',
        }),
      }),
      stroke: new ol.style.Stroke({
        color: '#FFA7D3',
        width: 10,
      }),
    }));
  }
  feature.set('zIndex', 10);
  return styles;
}

function selectedFeatures (feature, resolution) {
  const zoom = map.getView().getZoom();

  const geometry = feature.getGeometry();
  const coordinates = geometry.getCoordinates();

  const styles = [];

  if (zoom <= 8) {
    styles.push(new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: 'red',
        width: 4,
      }),
    }));
  } else {
    styles.push(new ol.style.Style({
      stroke: new ol.style.Stroke({
        color: 'grey',
        width: 4,
      }),
      image: new ol.style.Circle({
        radius: 6,
        fill: new ol.style.Fill({
          color: 'black',
        }),
      }),
      text: new ol.style.Text({
        // text: (feature.get("elevation") !== undefined ? "elevation: " + feature.get("elevation") + "\n" : "Height:") + feature.get("structureHeight") + " m",
        text: (feature.get("elevation") !== undefined ? "elevation: " + feature.get("elevation") + " m\nStr Height: " + feature.get("structureHeight") + " m"
        :
         "False"),
        font: '12px Calibri,sans-serif',
        textAlign: 'left',
        fill: new ol.style.Fill({
          color: 'black',
        }),
        backgroundFill: new ol.style.Fill({
          color: [255, 255, 255, 0.6],
        }),
        padding: [2, 2, 2, 2],
        offsetX: 10, 
      }),
    }));

    styles.push(new ol.style.Style({
      geometry: new ol.geom.Point(coordinates[0]),
      image: new ol.style.RegularShape({
        points: 3,
        rotation: Math.PI * 4 / 3,
        radius: 10, // Adjust the radius based on the zoom level
        fill: new ol.style.Fill({
          color: 'blue',
        }),
      }),
    }));

    styles.push(new ol.style.Style({
      geometry: new ol.geom.Point(coordinates[coordinates.length -1]),
      image: new ol.style.RegularShape({
        points: 3,
        rotation: Math.PI / 3,
        radius: 10, // Adjust the radius based on the zoom level
        fill: new ol.style.Fill({
          color: 'red',
        }),
      }),
    }));
    
  }
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
  layerId : "Selected",
  source : SelectedFeatureSource,
  style : selectedFeatures,
})

console.log(SelectedFeatureLayer)
const ActiveObstacle = new ol.layer.Tile({
  opacity: 1,
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


// const SimplifiedTLMSource = new ol.source.Vector({
//   features: new ol.format.GeoJSON().readFeatures(TLMDATA, {
//     featureProjection: 'EPSG:2056', // Adjust to your map's projection
//   }),
// });

const SimplifiedTLMSource = new ol.source.Vector({
  features: [], // Initialize with empty features array
});

// Loads the TLM Simple features
getTLMSimpleFeatures()

const SimplifiedTLMLayer = new ol.layer.Vector({
  style: featuresStyle,
  source: SimplifiedTLMSource,
  layerId : "TLM",
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
//Populates the table
updateSelectedFeaturesTable();

//When a feature is selcted
const popupContainer = document.getElementById('popup');
const popupTitle = document.getElementById('popup-title');
const popupContent = document.getElementById('popup-content');
const popupCloser = document.getElementById('popup-closer');

const popup = new ol.Overlay({
  element: popupContainer,
  autoPan: {
    animation: {
      duration: 250,
    },
  },
});

map.addOverlay(popup);


const selectInteraction = new ol.interaction.Select({
  style: selected,
  layers: [SimplifiedTLMLayer,SelectedFeatureLayer], // Specify the layers on which the interaction will work
  multi: false,
  hitTolerance : 5
});

popupCloser.onclick = function() {
  selectInteraction.getFeatures().clear();
  popup.setPosition(undefined);
  popupCloser.blur();
  return false;
};

map.addInteraction(selectInteraction);

selectInteraction.on('select', function (evt) {
  const selectedFeatures = evt.selected;
  const selectedLayerName = selectInteraction.getLayer(selectedFeatures[0]).get("layerId")

  if (selectedFeatures.length > 0) {
    if (selectedLayerName =="Selected"){
      const extent = selectedFeatures[0].getGeometry().getExtent()
      const center = ol.extent.getCenter(extent);

      popupTitle.innerHTML = "Feature";
      var newPopupContent = '<pre id="json">'
      let entry
      for (let selectedFeature of selectedFeatures){
        const selectedFeatureProperties = selectedFeature.getProperties();
        console.log(selectedFeature)
        delete selectedFeatureProperties.geometry;
        entry = JSON.stringify(selectedFeatureProperties, undefined, 2);
        newPopupContent += entry
      }
      newPopupContent += "</pre>"
      popupContent.innerHTML = newPopupContent
      popup.setPosition(center);
    } 
    else if (selectedLayerName =="TLM"){
      const extent = ol.extent.createEmpty();
      selectedFeatures.forEach(function (feature) {
        ol.extent.extend(extent, feature.getGeometry().getExtent());
      });
      const center = ol.extent.getCenter(extent);

      popupTitle.innerHTML = "Line String";

      var newPopupContent = '<table>'
      let entry = '<tr><th>Source</th><th>Linked Reg. Num.</th><th>Actions</th></tr>'
      newPopupContent += entry
      for (let selectedFeature of selectedFeatures){
        let featureId = selectedFeature.get("id") 
        entry = ""
        entry += "<tr><td>" 
        entry += featureId
        entry += "</td><td>"
        entry += selectedFeature.get("omsMatches") 
        entry += '</td><td>';
        entry += `<button id="SelectFeature" class="action-button" data-feature-id="${featureId}"> + </button>`;
        entry += '</td></tr>';
        newPopupContent += entry
      }
      newPopupContent += "</table>"
      popupContent.innerHTML = newPopupContent

      const actionButtons = document.querySelectorAll('.action-button');
      actionButtons.forEach(button => {
        button.addEventListener('click', function() {
          const featureId = button.dataset.featureId;
          addFeature(featureId, "TLM");

        });
      });

      popup.setPosition(center);
    }
  }
})

let isContextMenuVisible = false;

function showContextMenu(x, y) {
  if (isContextMenuVisible) return; // Check if the context menu is already visible
  isContextMenuVisible = true; // Set the flag to true when showing the menu
  var contextMenu = document.getElementById('context-menu');
  var contextMenuContent1 = document.getElementById('context-menu-content-1');
  var contextMenuContent2 = document.getElementById('context-menu-content-2');
  var contextMenuContent1pts = document.getElementById('context-menu-1points');
  var contextMenuContent2pts = document.getElementById('context-menu-2points');
  var featuresAtCoordinates = map.getFeaturesAtPixel([x, y]);
  var fuseButton = contextMenuContent2pts.querySelector('.fuse-button');
  var divideButton = contextMenuContent1pts.querySelector('.divide-button');
  var points = []
  var linestrings = []
  for (var feature of featuresAtCoordinates){
    if (feature.getGeometry().getType() === "Point"){
      points.push({id: feature.get('id'),source :  feature.get('source')})
    }
  }

  for (var feature of featuresAtCoordinates){
    if (feature.getGeometry().getType() === "linestring"){
      linestrings.push(feature.get('source'))
    }
  }

  const fuseClickListener = () => {
    console.log("fuseClickListener")
    fusePoints(points);
    hideContextMenu();
  };
  
  const divideClickListener = () => {
    console.log("divideClickListener")
    dividePoint(points);
    hideContextMenu();
  };

  // Hide all submenus
  contextMenuContent1pts.style.display = 'none';
  contextMenuContent2pts.style.display = 'none';

  if (points.length === 2){
    contextMenuContent1.innerHTML = 'Source: ' + points[0].source  + ' / ' + points[1].source;
    contextMenuContent2.innerHTML = 'Point ID: ' + points[0].id + ' / ' + points[1].id ;
    contextMenuContent2pts.style.display = 'block';
    fuseButton.removeEventListener('click', fuseClickListener);
    fuseButton.addEventListener('click', fuseClickListener, { once: true });
  
  } else if (points.length === 1 ){
    contextMenuContent1.innerHTML = 'Source: ' + points[0].source;
    contextMenuContent2.innerHTML = 'Point ID: ' + points[0].id;
    contextMenuContent1pts.style.display = 'block';
    divideButton.removeEventListener('click', divideClickListener);
    divideButton.addEventListener('click', divideClickListener, { once: true });
  }  else {
    return;
  }
  // Set the position of the context menu
  contextMenu.style.display = 'block';
  contextMenu.style.left = x + 'px';
  contextMenu.style.top = y + 'px';
}

function hideContextMenu() {
  var contextMenu = document.getElementById('context-menu');
  contextMenu.style.display = 'none';
  isContextMenuVisible = false; 
}

function removeAllListeners(element) {
  var clonedElement = element.cloneNode(true);
  element.parentNode.replaceChild(clonedElement, element);
}

//BackendCall
/////////////////////////////////////////////////////////////////////

function getTLMSimpleFeatures() {
  $.ajax({
    type: 'GET',
    url: '/map/getTLMSimpleFeatures/',
    headers: {
      'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
    },
    success: function(response) {
      console.log('getTLMSimpleFeatures:', response);
      if (response.success){
        SimplifiedTLMSource.clear(); 
        const newFeatures = new ol.format.GeoJSON().readFeatures(response.features, {
          featureProjection: 'EPSG:2056',
        });
        SimplifiedTLMSource.addFeatures(newFeatures); // Add new features
      } else {
        // Handle failure if needed 
      }
    },
    error: function(error) {
      console.error('getTLMSimpleFeatures Error:', error);
    } 
  })
}

function remFeature(featureId = "null") {
  $.ajax({
    type: 'POST',
    url: '/map/remFeature/',
    headers: {
      'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
    },
    data: JSON.stringify({
      featureId: featureId,
    }),
    success: function(response) {
      updateSelectedFeaturesTable();
      console.log('remFeature:', response);
    },
    error: function(error) {
      console.error('remFeature Error:', error);
    }
  });
}

function getFeature(callback) {
  $.ajax({
    type: 'GET',
    url: '/map/getFeature/', 
    success: function (response) {
      console.log('getFeature:', response);
      callback(response.features);
    },
    error: function (error) {
      console.error('getFeature Error:', error);
      callback(null);
    }
  });
}

function addFeature(featureId,featureType, featureData = null) {
  $.ajax({
    type: 'POST',
    url: '/map/addFeature/',
    headers: {
      'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
    },
    data: JSON.stringify({
      featureId: featureId,
      featureType : featureType,
      featureData : featureData,
    }),
    success: function(response) {
      console.log('addFeature:', response);
      updateSelectedFeaturesTable();
    },
    error: function(error) {
      console.error('addFeature Error:', error);
    }
  });
}

function updateSelectedFeaturesTable() {
  getFeature(function(features) {
    var tableBody = $('#selectedFeatures tbody');
    tableBody.empty();
    SelectedFeatureSource.clear()

    if (features) {
      console.log(features)
      for (const [key, value] of Object.entries(features)) {
        for (let testFeature of value.coordinates.features) {
          let testFeatureObject = new ol.format.GeoJSON().readFeature(testFeature);
          SelectedFeatureSource.addFeature(testFeatureObject);
        }
    
        var row = $('<tr>')
          .append($('<td>').text(value.type))
          .append($('<td>').text(value.id))
          .append($('<td>').html(`<button class="remFeatureButton" data-id="${value.id}"> - </button>`));
    
        tableBody.append(row);
      }
      $('.remFeatureButton').click(function() {
        var featureId = $(this).data('id');
        remFeature(featureId);
      });
    }
  })
}

function validation(){
  $.ajax({
    type: 'POST',
    url: '/map/validation/',
    headers: {
      'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
    },
    success: function(response) {
      console.log('validation:', response);
      if (response.success) {
        updateSelectedFeaturesTable();
        map.removeLayer(SimplifiedTLMLayer)
        document.getElementById('step1').style.display = 'none';
        document.getElementById('step2').style.display = 'block';
      } else {
        alert('Validation failed: ' + response.message);
      }
    },
    error: function(error) {
      console.error('validation Error:', error);
    }
  })
}

const fusePoints = (points) => {  
  $.ajax({
    type: 'POST', 
    url: '/map/fuse/', 
    headers: {
      'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
    },
    data: JSON.stringify({
      points: points
    }),
    contentType: 'application/json',  
    success: function(response) {
      if (response.success){
        updateSelectedFeaturesTable();
      } else {
        alert('Fuse failed: ' + response.message);
      }
    },
    error: (xhr, status, error) => {
      console.error('Fuse Error:', error);
    }
  });
};

const dividePoint = (points) => {
  $.ajax({
    type: 'POST', 
    url: '/map/divide/', 
    headers: {
      'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
    },
    data: JSON.stringify({
      points: points
    }),
    contentType: 'application/json',
    success: (response) => {
      console.log('dividePoints', response);
      if (response.success){
        updateSelectedFeaturesTable();
      } else {
        alert('Divide failed: ' + response.message);
      }

    },
    error: (xhr, status, error) => {
      console.error('Divide points error:', status, error);
    }
  });
};

function exportfeature(){
  $.ajax({
    type: 'POST',
    url: '/map/export/',
    headers: {
      'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
    },
    success: function(response) {
      console.log('exportFeature:', response);
      if (response.success) {
        ExportMaterial.history = response.history
        ExportMaterial.dcs.points = response.dcs.points
        ExportMaterial.dcs.jths = response.dcs.jths
        openDCSAttributesPopup()
        const filePreview = document.getElementById('DCSAttributesfilePreview');
        const formattedJSON = JSON.stringify(ExportMaterial, null, 2);
        filePreview.innerHTML = '<pre>' + formattedJSON + '</pre>';
      } else {
        alert('exportFeature failed: ' + response.message);
      }
    },
    error: function(error) {
      console.error('exportfeature Error:', error);
    }
  })
};

// POPUP
/////////////////////////////////////////////////////////////////////
function openPopup() {
  document.getElementById('DCSOverlay').style.display = 'block';
  document.getElementById('DCSPopup').style.display = 'block';
}

function closePopup() {
  document.getElementById('DCSOverlay').style.display = 'none';
  document.getElementById('DCSPopup').style.display = 'none';
}

function saveAction() { 
  const fileInput = document.getElementById('fileInput');
  const selectedFile = fileInput.files[0];

  if (selectedFile && selectedFile.type === 'application/json') {
    const reader = new FileReader();

    reader.onload = function (e) {
      const jsonData = JSON.parse(e.target.result);
      addFeature(selectedFile.name, "DCS", jsonData);
      closePopup();
    };
    reader.readAsText(selectedFile);
  }
}

function handleFileSelect(event) {
  const files = event.target.files;
  handleFile(files[0]);
}

function handleFile(file) {
  const filePreview = document.getElementById('filePreview');

  if (file && file.type === 'application/json') {
    const reader = new FileReader();

    reader.onload = function (e) {
      const jsonData = JSON.parse(e.target.result);

      const preview = document.createElement('pre');
      preview.textContent = JSON.stringify(jsonData, null, 2);
      filePreview.innerHTML = ''; // Clear previous preview
      filePreview.appendChild(preview);
    };

    reader.readAsText(file);
  }
}
////
function openDCSAttributesPopup() {
  document.getElementById('DCSOverlay').style.display = 'block';
  document.getElementById('DCSAttributesPopup').style.display = 'block';
}

function closeDCSAttributesPopup() {
  document.getElementById('DCSOverlay').style.display = 'none';
  document.getElementById('DCSAttributesPopup').style.display = 'none';
}

function handleDCSAttributesFileSelect(event) {
  const file = event.target.files[0];
  const fileName = file.name;
  handleDCSAttributesFile(file,fileName);
}

function handleDCSAttributesFile(file, name) {
  const filePreview = document.getElementById('DCSAttributesfilePreview');

  if (file && file.type === 'application/json') {
    const reader = new FileReader();

    reader.onload = function (e) {
      const jsonData = JSON.parse(e.target.result);
      ExportMaterial.name = name

      ExportMaterial.dcs.originator = jsonData.originator
      ExportMaterial.dcs.type = jsonData.type
      ExportMaterial.dcs.moving = jsonData.moving
      ExportMaterial.dcs.group = jsonData.group
      ExportMaterial.dcs.hospitalNearby = jsonData.hospitalNearby
      ExportMaterial.dcs.ownerInfo = jsonData.ownerInfo
      ExportMaterial.dcs.approvalLetterRequired = jsonData.approvalLetterRequired
      ExportMaterial.dcs.lastModificationReport = jsonData.lastModificationReport
      ExportMaterial.dcs.pending = jsonData.pending
      ExportMaterial.dcs.authority = jsonData.authority
      ExportMaterial.dcs.publicationTypes = jsonData.publicationTypes
      ExportMaterial.dcs.structureStatus = jsonData.structureStatus
      ExportMaterial.dcs.legacySymbolCode = jsonData.legacySymbolCode
      ExportMaterial.dcs.legacyOwnerAddress = jsonData.legacyOwnerAddress
      ExportMaterial.dcs.legacyOmsCMID = jsonData.legacyOmsCMID
      ExportMaterial.dcs.legacyOmsInvoiceCMID = jsonData.legacyOmsInvoiceCMID
      ExportMaterial.dcs.legacyInvoiceAddress = jsonData.legacyInvoiceAddress

      ExportMaterial.history.push({
        timestamp: new Date().toISOString(),
        operation: 'Metadata completion',
        parameter: {
            Source : name
          }
      })

      const formattedJSON = JSON.stringify(ExportMaterial, null, 2);
      filePreview.innerHTML = '<pre>' + formattedJSON + '</pre>';
    };

    reader.readAsText(file);
  }
}

function exportDCSAttributesAction(file) {
  //DCS data generation
  const dcsData = JSON.stringify(file.dcs, null, 2);
  const dcsBlob = new Blob([dcsData], { type: 'application/json' });
  const dcsA = document.createElement('a');
  const dcsUrl = window.URL.createObjectURL(dcsBlob);
  dcsA.href = dcsUrl;
  dcsA.download = 'MOD-' + file.name ;
  document.body.appendChild(dcsA);
  dcsA.click();
  document.body.removeChild(dcsA);
  window.URL.revokeObjectURL(dcsUrl);

  //History 
  const historyData = JSON.stringify(file.history, null, 2);
  const historyBlob = new Blob([historyData], { type: 'application/json' });
  const historyA = document.createElement('a');
  const historyUrl = window.URL.createObjectURL(historyBlob);
  historyA.href = historyUrl;
  historyA.download = 'History-' + file.name ;
  document.body.appendChild(historyA);
  historyA.click();
  document.body.removeChild(historyA);
  window.URL.revokeObjectURL(historyUrl);
}

// HTML 
/////////////////////////////////////////////////////////////////////


$(document).ready(function() {
  $('#remFeature').click(function() {
    remFeature();
  });
  $('#openPopupBtn').click(function() {
    openPopup();
  });

  $('#closeBtn').click(function() {
    closePopup();
  });

  $('#saveDCSFeature').click(function() {
    saveAction();
  });
  $('#fileInput').on('change', function(event) {
    handleFileSelect(event);
  });

  $('#validation').click(function() {
    validation();
  });

  $('#exportfeature').click(function() {
    exportfeature();
  });
  
  $('#DCSAttributescloseBtn').click(function() {
    closeDCSAttributesPopup();
  });

  $('#DCSAttributesfileInput').on('change', function(event) {
    handleDCSAttributesFileSelect(event);
  });

  $('#exportDcsFeature').click(function() {
    exportDCSAttributesAction(ExportMaterial);
  });
});

document.addEventListener('contextmenu', function(event) {
  event.preventDefault();
  showContextMenu(event.clientX, event.clientY);
});

document.addEventListener('click', function() {
  hideContextMenu();
  var contextMenuContent1pts = document.getElementById('context-menu-1points');
  var contextMenuContent2pts = document.getElementById('context-menu-2points');
  var fuseButton = contextMenuContent2pts.querySelector('.fuse-button');
  var divideButton = contextMenuContent1pts.querySelector('.divide-button');
  removeAllListeners(fuseButton);
  removeAllListeners(divideButton);
});


