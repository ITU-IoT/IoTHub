var roomSliderTimeouts = [];
function onSliderChange(value, roomId) {
  clearTimeout(roomSliderTimeouts[roomId]);
  roomSliderTimeouts[roomId] = setTimeout(function() {
  	console.log(value, roomId, $);
	$.ajax({
		type: 'PUT',
		url: "/music/volume/"+roomId+"/"+value
	});
  }, 300);
}
