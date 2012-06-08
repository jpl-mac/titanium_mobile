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
	color:'green',
	top: 200
});

win1.add(label1);

var mybutton=Ti.UI.createButton
(
	{top: 100,title: 'Push Me'}
);

mybutton.addEventListener
(
	'click',
	function(e)
	{
		e.source.title='Pushed!';
		slider1.backgroundColor='#00F';
		progress1.backgroundColor='#0F0';
	}
);

win1.add(mybutton);

var slider1=Ti.UI.createSlider
(
	{
		top: 200,
		min: 0,
		max: 100,
		value: 50,
	}
);

var sliderListener=function(e)
{
	progress1.value=100-e.value;
	label1.text='Slider value: '+e.value;
	label1.top=e.value;
	mybutton.opacity=e.value/100.0;
};

slider1.addEventListener('change',sliderListener);


win1.add(slider1);

var progress1=Ti.UI.createProgressBar({
	value:0,
	min: 0,
	max: 100,
	top: 300,
});

win1.add(progress1);

// open window
win1.open();
