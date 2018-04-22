var currentCube = '';
var currentEventSource = null;
var leds = null;

function send(command) {
  var url = '/api/send/' + currentCube + '/' + command;
  var request = new XMLHttpRequest();
  request.open('POST', url, true);
  request.send(null);
}
function setSpeed(speed) {
  if (speed <= 0) {
    return;
  }
  document.getElementById('frequencySlider').value = speed;
  document.getElementById('frequencyInput').value = speed;
  var delay = 1.0 / speed;
  send('delay=' + delay);
}
function setBrightness(brightness) {
  if (brightness < 1 || brightness > 255) {
    return;
  }
  document.getElementById('brightnessSlider').value = brightness;
  document.getElementById('brightnessInput').value = brightness;
  send('brightness=' + brightness);
}
function start(visualization) {
  send('start:' + visualization);
}
function stop() {
  send('stop');
}
function disconnect() {
  send('quit');
}
function getCubeNames() {
  var request = new XMLHttpRequest();
  request.open('GET', '/api/list-cubes', true);
  request.onload = function() {
    if (this.status == 200) {
      var cubes = JSON.parse(this.response).cubes;
      updateCubeSelector(cubes);
      if (cubes.length > 0) {
        selectCube(cubes[0]);
      }
    }
  }
  request.send(null);
}
function updateCubeSelector(cubeNames) {
  var selector = document.getElementById('cubeNameSelector');
  // Remove all but the first child.
  while (selector.children.length > 1) {
    selector.removeChild(selector.children[selector.children.length - 1]);
  }
  for (var i = 0; i < cubeNames.length; i++) {
    var option = document.createElement('option');
    option.value = cubeNames[i];
    option.innerText = cubeNames[i];
    selector.appendChild(option);
  }
}
function selectCube(cubeName) {
  if (cubeName == '') {
    return;
  }
  currentCube = cubeName;
  document.getElementById('cubeNameSelector').value = cubeName;
  listenToCube();
}
function initLeds() {
  if (leds != null) {
    return leds;
  }
  leds = [];
  var display = document.getElementById('display-placeholder');
  for (var i = 0; i < 8; ++i) {
    var row = document.createElement('div');
    row.style = 'height: 20px; margin: 5px;';
    display.appendChild(row);
    for (var j = 0; j < 8; ++j) {
      leds[8*i + j] = document.createElement('span');
      leds[8*i + j].style = 'width: 20px; height: 20px; margin: 5px; display: inline-block;';
      row.appendChild(leds[8*i + j]);
    }
  }
}

function listenToCube() {
  if (currentEventSource != null) {
    currentEventSource.close();
  }
  currentEventSource = new EventSource('/api/listen/' + currentCube);
  currentEventSource.addEventListener('error', function(e) {
    console.log('Error from ' + e.origin);
  });
  initLeds();
  currentEventSource.addEventListener('message', function(e) {
    var data = base64js.toByteArray(e.data);
    // check for 'CUBE:' at the start
    if (data[0] != 67 || data[1] != 85 || data[2] != 66 || data[3] != 69 || data[4] != 58) {
      return;
    }
    var len = (data[5] << 8) + data[6];
    if (data.length < (7 + (3 * len))) {
      return;
    }
    for (var i = 0; i < len; ++i) {
      var r = data[7 + (3 * i)];
      var g = data[7 + (3 * i) + 1];
      var b = data[7 + (3 * i) + 2];
      leds[i].style.backgroundColor = 'rgb(' + r + ',' + g + ',' + b + ')';
    }
  });
}
