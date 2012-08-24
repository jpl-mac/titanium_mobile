// this sets the background color of the master UIView (when there are no windows/tab groups on it)
//Titanium.UI.setBackgroundColor('#000');

//
// create root window
//
var win1 = Titanium.UI.createWindow({  
    backgroundColor:'#F00'
});

var pumpCallback = function(e) {
			if (e.bytesProcessed == -1) {
				Ti.API.info("Can't perform any more operation.");

			} else if (e.errorDescription == null || e.errorDescription == "") {
				var data = e.buffer.toString();
				Ti.API.info("Buffer :" + data);
				Ti.API.info("TotalBytesProcessed :" + e.totalBytesProcessed);
				Ti.API.info("bytesProcessed :" + e.bytesProcessed);
 
			} else {
				Ti.API.info("READ ERROR: " + e.errorDescription);
            }
};
 
var buffer = Ti.createBuffer({ value: "Some long sentence for testing purpose, blah blah blah." });
var stream = Ti.Stream.createStream({ source: buffer });

Ti.Stream.pump(stream, pumpCallback, 7, true);


// open window
win1.open();