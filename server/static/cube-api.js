var currentCube = '';
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
  var delay = 1.0 / speed;
  send('delay=' + delay);
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
      updateCubeSelector(JSON.parse(this.response).cubes)
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
}

