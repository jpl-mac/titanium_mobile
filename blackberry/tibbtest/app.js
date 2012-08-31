var win1 = Titanium.UI.createWindow({
backgroundColor:'#F00'
});

var pumpCallback = function(e) {
			if (e.bytesProcessed == -1) { // EOF
				Ti.API.info("<EOF> - Can't perform any more operations on connected socket");

			} else if (e.errorDescription == null || e.errorDescription == "") {
				var data = e.buffer.toString();
				Ti.API.info("DATA!!!: " + data);

			} else {
				Ti.API.info("READ ERROR: " + e.errorDescription);
			}
};

var driverSocket;

var listenSocket = Ti.Network.Socket.createTCP({
    host: '192.168.163.130',
    port: 40404,

    accepted: function(e) {
    Ti.API.info("ACCEPTTED callback.");
    driverSocket = e.inbound;
	var readyMessage = {type: "ready"};
    driverSocket.write(Ti.createBuffer({value: JSON.stringify(readyMessage)}));

    Ti.Stream.pump(driverSocket, pumpCallback, 1024, true);
		},
	error: function(e) {
	Ti.API.info("ERROR callback asdf.");
		//e.socket.close();
	}
});

listenSocket.listen();

listenSocket.accept({

});

var button = Titanium.UI.createButton({
title: 'Stop',
top: 10,
width: 200,
height: 100
});

button.addEventListener('click',function(e)
{
var testMsg = "Message From Server";
driverSocket.write(Ti.createBuffer({value: JSON.stringify(testMsg)}));
});

win1.add(button);

// open window
win1.open();