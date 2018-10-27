var roomSliderTimeouts = [];
function onSliderChange(value, roomId) {
  clearTimeout(roomSliderTimeouts[roomId]);
  roomSliderTimeouts[roomId] = setTimeout(function() {
  	console.log(value, roomId, $);
	$.ajax({
		type: 'POST',
		url: "/music/volume/"+roomId+"/"+value,
		success: function() {console.log("posted successfully")}
	})
  }, 500);
}
