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
