function toggle(div_id) {
	var el = document.getElementById(div_id);
	if ( el.style.display == 'none' ) {	el.style.display = 'block';}
	else {el.style.display = 'none';}
}
function show(div_id) {
	var el = document.getElementById(div_id);
	if ( el.style.display == 'none' ) {	el.style.display = 'block';}
}

function showAsIT(div_id) {
  var el = document.getElementById(div_id);
  el.style.left ='0%';
  if ( el.style.display == 'none' ) { el.style.display = 'block';}
}

function showAsTT(div_id) {
  var el = document.getElementById(div_id);
  el.style.left ='50%';
  if ( el.style.display == 'none' ) { el.style.display = 'block';}
}


function book_plot( existing_runs, name ) { 
           name = typeof name !== 'undefined' ? name : "Just histogram";
           var xVals = [];
           var yVals = [];
           var yErrs = [];

           for (var i in existing_runs) {
              xVals.push(existing_runs[i].toString());
              yVals.push(0);
              yErrs.push(0);
            }
           console.log(xVals);
           console.log(yVals);
           console.log(yErrs);
           $('#container').highcharts({
            chart: {
            	animation: false,
            },
            title: {
                text: name
            },
            xAxis: {
                categories: xVals
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            series: [{
                data: yVals,
                type: 'spline'
            },
            {
                data: yErrs,
                type: 'errorbar'
            }]
        });
};


function make_plot(xVals, yVals, yErrs, name ) { 
           name = typeof name !== 'undefined' ? name : "Just histogram";
           xVals = typeof xVals !== 'undefined' ? xVals : [1, 2, 3];
           yVals = typeof yVals !== 'undefined' ? yVals : [54, 55, 53];
           $('#container').highcharts({
            chart: {
            	animation: false,
            },
            title: {
                text: name
            },
            xAxis: {
                categories: xVals
            },
            yAxis: {
                title: {
                    text: ''
                }
            },
            series: [{
                data: yVals,
                type: 'spline'
            },
            {
                data: yErrs,
                type: 'errorbar'
            }]
        });
};

function update_plot(yVals, yErrs, name) { 
  var chart = $('#container').highcharts();
  chart.setTitle({text: name});
  for (i = 0; i < chart.series[0].data.length; i++) { 
    chart.series[0].data[i].update(yVals[i]);
    chart.series[1].data[i].update(yErrs[i]);
  }
};


function hide(div_id) {
	var el = document.getElementById(div_id);
	el.style.display = 'none';
}


function hideAsIT(div_id) {
  var el = document.getElementById(div_id);
  el.style.display = 'none';
  el.style.left ='50%';
}

function hideAsTT(div_id) {
  var el = document.getElementById(div_id);
  el.style.display = 'none';
  el.style.left ='0%';
}


function blanket_size(popUpDivVar) {
	if (typeof window.innerWidth != 'undefined') {
		viewportheight = window.innerHeight;
	} else {
		viewportheight = document.documentElement.clientHeight;
	}
	if ((viewportheight > document.body.parentNode.scrollHeight) && (viewportheight > document.body.parentNode.clientHeight)) {
		blanket_height = viewportheight;
	} else {
		if (document.body.parentNode.clientHeight > document.body.parentNode.scrollHeight) {
			blanket_height = document.body.parentNode.clientHeight;
		} else {
			blanket_height = document.body.parentNode.scrollHeight;
		}
	}
	var blanket = document.getElementById('blanket');
	blanket.style.height = blanket_height + 'px';
	var popUpDiv = document.getElementById(popUpDivVar);
	popUpDiv_height=blanket_height/2-200;//200 is half popup's height
	popUpDiv.style.top = popUpDiv_height + 'px';
}
function window_pos(popUpDivVar) {
	if (typeof window.innerWidth != 'undefined') {
		viewportwidth = window.innerHeight;
	} else {
		viewportwidth = document.documentElement.clientHeight;
	}
	if ((viewportwidth > document.body.parentNode.scrollWidth) && (viewportwidth > document.body.parentNode.clientWidth)) {
		window_width = viewportwidth;
	} else {
		if (document.body.parentNode.clientWidth > document.body.parentNode.scrollWidth) {
			window_width = document.body.parentNode.clientWidth;
		} else {
			window_width = document.body.parentNode.scrollWidth;
		}
	}
	var popUpDiv = document.getElementById(popUpDivVar);
	window_width=window_width/2-200;//200 is half popup's width
	popUpDiv.style.left = window_width + 'px';
}
function popup(windowname) {
	blanket_size(windowname);
	window_pos(windowname);
	toggle('blanket');
	toggle(windowname);		
}