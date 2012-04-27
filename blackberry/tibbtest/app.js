// this sets the background color of the master UIView (when there are no windows/tab groups on it)
//Titanium.UI.setBackgroundColor('#000');

//
// create root window
//
var win1 = Titanium.UI.createWindow({  
    backgroundColor:'#F00'
});

var label1 = Ti.UI.createLabel({
	textAlign : 'center',
	text:'Hello, world!'
});

label1.text='Test';

win1.add(label1);

var mybutton=Ti.UI.createButton
(
	{label: 'Push Me'}
);

mybutton.addEventListener
(
	'click',
	function(e)
	{
		e.source.label='Pushed!';
	}
);

win1.add(mybutton);

var slider1=Ti.UI.createSlider
(
	{
		value: 50,
		top: 0,
		min: 0,
		max: 100
	}
);

win1.add(slider1);

var progress1=Ti.UI.createProgressBar({
	value:0
});

win1.add(progress1);


/*
label1.text = Titanium.buildDate;

win1.add(label1);
*/


/*
var slider1=Ti.UI.createSlider
(
	{
		value: 50,
		top: 0,
		min: 0,
		max: 100
	}
);

slider1.addEventListener
(
	'change',
	function(e)
	{
		Ti.API.debug('value changed\n');
	}
);
*/

//win1.add(slider1);

// open window
win1.open();
