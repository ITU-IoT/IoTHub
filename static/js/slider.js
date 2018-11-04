var roomSliderTimeouts = [];
function onSliderChange(value, roomId) {
  clearTimeout(roomSliderTimeouts[roomId]);
  roomSliderTimeouts[roomId] = setTimeout(function() {
	$.ajax({
		type: 'PUT',
		url: "/music/volume/"+roomId+"/"+value
	});
  }, 300);
}

var lightColorTimeouts = [];
function onLightChange(value, lightId) {
  var val = value.replace('#', '')
  clearTimeout(lightColorTimeouts[lightId]);
  lightColorTimeouts[lightId] = setTimeout(function() {
	$.ajax({
		url: "/light/color/"+lightId+"/"+val,
        type: 'PUT'
	});
  }, 300);
}

