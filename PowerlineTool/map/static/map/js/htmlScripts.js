//import { addFeature } from "./module.js";

//HTML FUNCTIONS
/////////////////////////////////////////////////////////////////////


function openPopup() {
    // Display the overlay and the popup
    document.getElementById('DCSOverlay').style.display = 'block';
    document.getElementById('DCSPopup').style.display = 'block';
}
  
function closePopup() {
    // Hide the overlay and the popup
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

        console.log(selectedFile.name, "DCS", jsonData)
        addFeature(selectedFile.name, "DCS", jsonData);

        closePopup();
      };
  
      reader.readAsText(selectedFile);
    }
  }

function handleDragOver(event) {
    event.preventDefault();
}

function handleDrop(event) {
    event.preventDefault();
    const files = event.dataTransfer.files;
    handleFile(files[0]);
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

function addFeature(featureId,featureType, featureData = null) {
  console.log(featureData)
  $.ajax({
    type: 'POST',
    url: '/map/addFeature/',
    headers: {
      'X-CSRFToken': $('[name="csrfmiddlewaretoken"]').val(),
    },
    data: JSON.stringify({
      featureId: featureId,
      featureType : featureType,
      featureData : featureData
    }),
    success: function(data) {
      console.log('addFeature:', data);
      updateSelectedFeaturesTable();
    },
    error: function(error) {
      console.error('addFeature Error:', error);
    }
  });
}

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

