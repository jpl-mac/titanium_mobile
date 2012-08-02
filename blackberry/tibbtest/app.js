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
	font: {fontSize:12},
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
		win1.remove(progress1);
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
		width: '100mm',
	}
);

var sliderListener=function(e)
{
	progress1.value=100-e.value;
	label1.top=e.value;
	mybutton.opacity=e.value/100.0;
	mybutton.left=e.value;
	label1.text='Opacity value: '+mybutton.opacity;
};

slider1.addEventListener('change',sliderListener);
label1.addEventListener('click',function(e)
	{
		label1.text='Label was clicked';
	}
	);


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
