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
	text:'Hello, world!',
	color:'green'
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
		//e.source.label='Pushed!';
		e.source.setVisible(false);
	}
);

win1.add(mybutton);

var slider1=Ti.UI.createSlider
(
	{
		top: 0,
		min: 0,
		max: 100,
		value: 50
	}
);

slider1.addEventListener
(
	'change',
	function(e)
	{
		progress1.value=e.value;
		label1.text='Slider value: '+e.value;
	}
);


win1.add(slider1);

var progress1=Ti.UI.createProgressBar({
	value:0,
	min: 0,
	max: 100
});

win1.add(progress1);

// open window
win1.open();
