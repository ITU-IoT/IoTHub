var roomSliderTimeouts = [];
function onSliderChange(value, roomId) {
  clearTimeout(roomSliderTimeouts[roomId]);
  roomSliderTimeouts[roomId] = setTimeout(function() {
  	console.log(value, roomId, $);
	$.post("/music/volume/"+roomId+"/"+value);
  }, 500);
}
