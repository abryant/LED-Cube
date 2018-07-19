var currentCube = '';
var currentEventSource = null;
var leds = null;
var audioContext = null;
var audioAnalyser = null;

function sendInput(input) {
  send('input:' + input);
}

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
  if (brightness < 0 || brightness > 100) {
    return;
  }
  document.getElementById('brightnessSlider').value = brightness;
  document.getElementById('brightnessInput').value = brightness;
  send('brightness=' + (brightness / 100.0));
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

function listenToCube() {
  if (currentEventSource != null) {
    currentEventSource.close();
  }
  currentEventSource = new EventSource('/api/listen/' + currentCube);
  currentEventSource.addEventListener('error', function(e) {
    console.log('Error from ' + e.origin);
  });
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
      leds[i].color = new THREE.Color('rgb(' + r + ',' + g + ',' + b + ')');
    }
    requestAnimationFrame(renderScene);
  });
}
function makeCube() {
  var SPACING = 4;
  var SIZE = 8;
  var offset = SPACING * (SIZE - 1) / 2.0;
  var cube = new THREE.Group();
  leds = [];
  for (var i = 0; i < SIZE; i++) {
    var layer = [];
    for (var j = 0; j < SIZE; j++) {
      var line = [];
      for (var k = 0; k < SIZE; k++) {
        var geometry = new THREE.BoxGeometry(1, 1, 1);
        var material = new THREE.MeshBasicMaterial({color: 0x00ff00});
        line.push(material);
        var box = new THREE.Mesh(geometry, material);
        box.position.set(SPACING * i - offset, SPACING * j - offset, SPACING * k - offset);
        cube.add(box);
      }
      if (j % 2 == 0) {
        line.reverse();
      }
      layer = layer.concat(line);
    }
    if (i % 2 == 1) {
      layer.reverse();
    }
    leds = leds.concat(layer);
  }
  // The layers are reversed for 8x8x8 cubes.
  if (SIZE == 8) {
    leds.reverse();
  }
  return cube;
}
var renderScene;
var cube;
var currentPosition;
function init3dScene(scene, camera, renderer) {
  cube = makeCube();
  scene.add(cube);
  currentPosition = new THREE.Spherical(20, Math.PI / 2, 0);

  renderer.domElement.onmousedown = handleCanvasMouseDown;
  renderer.domElement.onmouseup = handleCanvasMouseUp;
  renderer.domElement.onmousemove = handleCanvasMouseMove;
  renderer.domElement.onmousewheel = handleCanvasMouseWheel;
  renderer.domElement.ontouchstart = updateTouchMode;
  renderer.domElement.ontouchend = updateTouchMode;
  renderer.domElement.ontouchmove = handleCanvasTouchMove;
  renderer.setClearColor(new THREE.Color('#ffffff'));
  renderScene = function() {
    cube.setRotationFromEuler(new THREE.Euler(currentPosition.phi - Math.PI / 2, currentPosition.theta, 0));
    camera.position.z = currentPosition.radius;
    renderer.render(scene, camera);
  }
  requestAnimationFrame(renderScene);
}
var rotating = false;
var scaling = false;
var rotateStart = null;
var scaleStart = null;
function handleCanvasMouseDown(event) {
  rotateStart = new THREE.Vector2(event.clientX, event.clientY);
  rotating = true;
}
function handleCanvasMouseUp(event) {
  rotating = false;
}
function handleCanvasMouseMove(event) {
  if (event.buttons == 0) {
    rotating = false;
  }
  if (!rotating) {
    return;
  }
  rotate(new THREE.Vector2(event.clientX, event.clientY));
}
function rotate(rotateEnd) {
  var ROTATE_SPEED = 2;
  var delta = new THREE.Vector2();
  delta.subVectors(rotateEnd, rotateStart).multiplyScalar(ROTATE_SPEED * Math.PI / 180);
  rotateStart.copy(rotateEnd);

  currentPosition.phi += delta.y;
  currentPosition.theta += delta.x;
  if (currentPosition.theta < -Math.PI) {
    currentPosition.theta += 2 * Math.PI;
  }
  if (currentPosition.theta > Math.PI) {
    currentPosition.theta -= 2 * Math.PI;
  }
  currentPosition.makeSafe();
  requestAnimationFrame(renderScene);
}
function handleCanvasMouseWheel(event) {
  var ZOOM_SPEED = 2;
  event.preventDefault();
  if (event.deltaY > 0) {
    currentPosition.radius = Math.min(currentPosition.radius + ZOOM_SPEED, 40);
  } else if (event.deltaY < 0) {
    currentPosition.radius = Math.max(currentPosition.radius - ZOOM_SPEED, 2);
  }
  requestAnimationFrame(renderScene);
}

function updateTouchMode(event) {
  event.preventDefault();
  rotating = false;
  scaling = false;
  rotateStart = null;
  scaleStart = null;
  if (event.targetTouches.length == 1) {
    rotating = true;
  } else if (event.targetTouches.length == 2) {
    scaling = true;
  }
}
function handleCanvasTouchMove(event) {
  event.preventDefault();
  var ZOOM_SPEED_TOUCH = 0.1;
  if (rotating) {
    if (event.targetTouches.length != 1) {
      rotating = false;
      return;
    }
    var rotateEnd = new THREE.Vector2(event.targetTouches[0].clientX, event.targetTouches[0].clientY);
    if (rotateStart == null) {
      rotateStart = rotateEnd;
    }
    rotate(rotateEnd);
  }
  if (scaling) {
    if (event.targetTouches.length != 2) {
      scaling = false;
      return;
    }
    var scaleEnd = Math.sqrt((event.targetTouches[0].clientX - event.targetTouches[1].clientX)**2 + (event.targetTouches[0].clientY - event.targetTouches[1].clientY)**2);
    if (scaleStart == null) {
      scaleStart = scaleEnd;
    }
    var diff = (scaleStart - scaleEnd) * ZOOM_SPEED_TOUCH;
    scaleStart = scaleEnd;
    currentPosition.radius = Math.max(Math.min(currentPosition.radius + diff, 40), 2);
    requestAnimationFrame(renderScene);
  }
}

function handleKeyPress(event) {
  directionMap = {
    'w': 'back',
    'a': 'left',
    's': 'front',
    'd': 'right',
    'q': 'up',
    'e': 'down',
  };
  if (event.key in directionMap) {
    event.preventDefault();
    sendInput(directionMap[event.key]);
  }
}

function toggleAudio(checkbox) {
  var select = document.getElementById('microphone');
  if (checkbox.checked) {
    select.removeAttribute('disabled');
    populateMicrophoneList(select);
  } else {
    select.setAttribute('disabled', '');
    setMicrophones(select)([]);
    stopAudioProcessing();
  }
}

function populateMicrophoneList(select) {
  navigator.mediaDevices.getUserMedia({audio: true}).then(listAudioDevices).then(setMicrophones(select));
}

function listAudioDevices() {
  return navigator.mediaDevices.enumerateDevices().then((devices) => {
    return devices
      .filter((d) => d.kind === 'audioinput')
      .map((d, i) => ({
        id: d.deviceId, label: d.label || ('microphone ' + (i + 1))
      }));
  });
}

function setMicrophones(select) {
  return (devices) => {
    // Remove all but the first child.
    while (select.children.length > 1) {
      select.removeChild(select.children[select.children.length - 1]);
    }
    devices.forEach((d) => {
      var option = document.createElement('option');
      option.value = d.id;
      option.innerText = d.label;
      select.appendChild(option);
    });
  };
}

function stopAudioProcessing() {
  if (audioContext != null) {
    audioContext.close();
  }
  audioContext = null;
  audioAnalyser = null;
}

function selectMicrophone(id) {
  if (id == null || id == '') {
    stopAudioProcessing();
    return;
  }
  navigator.mediaDevices.getUserMedia({audio: {deviceId: {exact: id}}})
    .then((stream) => {
      stopAudioProcessing();
      audioContext = new AudioContext();
      var source = audioContext.createMediaStreamSource(stream);
      audioAnalyser = audioContext.createAnalyser();
      audioAnalyser.fftSize = 2048;
      source.connect(audioAnalyser);
    });
}

