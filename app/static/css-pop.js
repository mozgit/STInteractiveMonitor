function resize_charts(){
  var chart_width = $('#container_width').highcharts();
  var chart_bias = $('#container_bias').highcharts();
  var chart_efficiency = $('#container_efficiency').highcharts();
  var chartWidth = document.getElementById('STPlot').clientWidth;
  var chartHeight = document.getElementById('STPlot').clientHeight*0.3;
  console.log(chartWidth.toString()+"px : "+chartHeight.toString()+"px");
  chart_width.setSize(chartWidth, chartHeight);
  chart_bias.setSize(chartWidth, chartHeight);
  chart_efficiency.setSize(chartWidth, chartHeight);
}

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
  el.style.width ='45%';
  el.style.height ='100%';
  el.style.top ='0%';
  if ( el.style.display == 'none' ) { el.style.display = 'block';}
}

function showAsIT_lite(div_id) {
  var el = document.getElementById(div_id);
  if (el.style.width =='90%'){return true;}
  el.style.left ='10%';
  el.style.width ='45%';
  el.style.height ='100%';
  el.style.top ='0%';
  if ( el.style.display == 'none' ) { el.style.display = 'block';}
}

function showAsTT_lite(div_id) {
  var el = document.getElementById(div_id);
  if (el.style.width =='90%'){return true;}
  el.style.left ='55%';
  el.style.width ='45%';
  el.style.height ='100%';
  el.style.top ='0%';
  if ( el.style.display == 'none' ) { el.style.display = 'block';}
}

function expand_lite(div_id) {
  var el = document.getElementById(div_id);
  el.style.left ='10%';
  el.style.width ='90%';
  el.style.height ='100%';
  el.style.top ='0%';
  document.getElementById("container_width").style.width='90%';
  document.getElementById("container_bias").style.width='90%';
  document.getElementById("container_efficiency").style.width='90%';
  resize_charts();
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
           //console.log(xVals);
           //console.log(yVals);
           //console.log(yErrs);
           $('#container_width').highcharts({
            chart: {
            	animation: false,
            },
            title: {
                text: ""
            },
            xAxis: {
              name: 'Run',
              title:{text:null}
                //categories: xVals
            },
            yAxis: [{
                title: {
                    text: 'Resolution [μm]',
                },
                labels: {
                    format: '{value:3.2f}'
                }                
            },
            {
                title: {
                    text: 'Statistics',
                },
                opposite: true                
            }],
            tooltip: {
                formatter: function () {
                    var s = '<b> Run ' + this.x + '</b>';
                    var stat_s = '';
                    var val_s = '';
                    var err_s = '';
                    $.each(this.points, function () {
                        if (this.series.name == 'Number of hits'){
                          stat_s += (Math.round(this.y)).toString();
                        }
                        if (this.series.name == 'Resolution'){
                          val_s += (Math.round(this.y*100)/100).toString();
                        }    
                        if (this.series.name == 'One sigma range'){
                          err_s += (Math.round((this.point.high-this.point.low)/2*100)/100).toString();
                        }                
                    });
                    s+='<br/> Resolution: '+  val_s +' +/- '+err_s+ 'μm<br/> Number of hits: '+stat_s;
                    return s;
                },
                shared: true
            },
            legend:{enabled:false},
            series: [
            {
                name: 'Number of hits',
                data: yVals,
                type: 'area',
                yAxis: 1,
                fillColor: {
                    linearGradient: [0, 0, 0, 300],
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                lineWidth: 0,
                lineColor: '#FFFFFF',
                marker: {
                    enabled: false,
                    fillColor: '#FFFFFF',
                    lineWidth: 2,
                    lineColor: null // inherit from series                    
                }                                
            },

            {
                name: 'Resolution',
                data: yVals,
                type: 'spline'
            },
            {
                name: 'One sigma range',
                data: yErrs,
                type: 'errorbar'
            }
            ]
        });
           $('#container_bias').highcharts({
            chart: {
              animation: false,
            },
            title: {
                text: ""
                },
            xAxis: {
                //categories: xVals
            },
            yAxis: [{
                title: {
                    text: 'Bias [μm]',
                },
                labels: {
                        format: '{value:3.2f}'
                    }
            },
            {
                title: {
                    text: 'Statistics',
                },
                opposite: true                
            }], 
            tooltip: {
                formatter: function () {
                    var s = '<b> Run ' + this.x + '</b>';
                    var stat_s = '';
                    var val_s = '';
                    var err_s = '';
                    $.each(this.points, function () {
                        if (this.series.name == 'Number of hits'){
                          stat_s += (Math.round(this.y)).toString();
                        }
                        if (this.series.name == 'Bias'){
                          val_s += (Math.round(this.y*100)/100).toString();
                        }    
                        if (this.series.name == 'One sigma range'){
                          err_s += (Math.round((this.point.high-this.point.low)/2*100)/100).toString();
                        }                
                    });
                    s+='<br/> Bias: '+  val_s +' +/- '+err_s+ 'μm<br/> Number of hits: '+stat_s;
                    return s;
                },
                shared: true
            },                       
            legend:{enabled:false},
            series: [
            {
                name: 'Number of hits',
                data: yVals,
                type: 'area',
                yAxis: 1,
                fillColor: {
                    linearGradient: [0, 0, 0, 300],
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                lineWidth: 0,
                lineColor: '#FFFFFF',
                marker: {
                    enabled: false,
                    fillColor: '#FFFFFF',
                    lineWidth: 2,
                    lineColor: null // inherit from series                    
                }                                
            },
            {
                name: 'Bias',
                data: yVals,
                type: 'spline'
            },
            {
                name: 'One sigma range',
                data: yErrs,
                type: 'errorbar'
            }]
        });
           $('#container_efficiency').highcharts({
            chart: {
              animation: false,
            },
            title: {
                text: ""
            },
            xAxis: {
              title:{text:null}
                //categories: xVals
            },
            yAxis: [{
                title: {
                    text: 'Efficiency, %',
                },
                labels: {
                        format: '{value:3.2f}'
                    }                
            },
            {
                title: {
                    text: 'Statistics',
                },
                opposite: true                
            }],

            tooltip: {
                formatter: function () {
                    var s = '<b> Run ' + this.x + '</b>';
                    var stat_s = '';
                    var val_s = '';
                    var err_s = '';
                    $.each(this.points, function () {
                        if (this.series.name == 'Number of found hits'){
                          stat_s += (Math.round(this.y)).toString();
                        }
                        if (this.series.name == 'Efficiency'){
                          val_s += (Math.round(this.y*100)/100).toString();
                        }    
                        if (this.series.name == 'One sigma range'){
                          err_s += (Math.round((this.point.high-this.point.low)/2*100)/100).toString();
                        }                
                    });
                    s+='<br/> Efficiency: '+  val_s +' +/- '+err_s+ '%<br/> Number of hits: '+stat_s;
                    return s;
                },
                shared: true
            },              
            legend:{enabled:false},
            series: [
            {
                name: 'Number of found hits',
                data: yVals,
                type: 'area',
                yAxis: 1,
                fillColor: {
                    linearGradient: [0, 0, 0, 300],
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).setOpacity(0).get('rgba')]
                    ]
                },
                lineWidth: 0,
                lineColor: '#FFFFFF',
                marker: {
                    enabled: false,
                    fillColor: '#FFFFFF',
                    lineWidth: 2,
                    lineColor: null // inherit from series                    
                }                                
            },
            {
                name: 'Efficiency',
                data: yVals,
                type: 'spline'
            },
            {
                name: 'One sigma range',
                data: yErrs,
                type: 'errorbar'
            }]
        });                   
};


function update_plot(yVals, yErrs, name) { 
  var chart = $('#container').highcharts();
  chart.setTitle({text: name.toString()});
  for (i = 0; i < chart.series[0].data.length; i++) { 
    chart.series[0].data[i].update(yVals[i]);
    chart.series[1].data[i].update(yErrs[i]);
  }
};

function update_plot_lite(name) { 
  var chart_width = $('#container_width').highcharts();
  var chart_bias = $('#container_bias').highcharts();
  var chart_efficiency = $('#container_efficiency').highcharts();
  //chart_width.setTitle({text: name.id});
  chart_width.xAxis[0].setCategories(existing_runs);
  chart_width.series[1].setData(map[name.id]["width"]);
  chart_width.series[2].setData(map[name.id]["err_width"]);
  chart_width.series[0].setData(map[name.id]["n_res"]);

  //chart_bias.setTitle({text: name.id});
  chart_bias.xAxis[0].setCategories(existing_runs);
  chart_bias.series[1].setData(map[name.id]["bias"]);
  chart_bias.series[2].setData(map[name.id]["err_bias"]);
  //I'm not sure why is this line is needed, 
  //but without it statistics is not updated
  chart_bias.series[0].setData(map[name.id]["n_eff"]);
  chart_bias.series[0].setData(map[name.id]["n_res"]);  

  //chart_efficiency.setTitle({text: name.id});
  chart_efficiency.xAxis[0].setCategories(existing_runs);
  chart_efficiency.series[1].setData(map[name.id]["efficiency"]);
  chart_efficiency.series[2].setData(map[name.id]["err_efficiency"]);  
  chart_efficiency.series[0].setData(map[name.id]["n_eff"]);

  //for (i = 0; i < chart.series[0].data.length; i++) { 
  //  chart.series[0].data[i].update(map[name.id][hist][i]);
  //  chart.series[1].data[i].update(map[name.id]["err_"+hist][i]);
  //}
};


function hide(div_id) {
	var el = document.getElementById(div_id);
	el.style.display = 'none';
}

function hideBig_lite(div_id) {
  var el = document.getElementById(div_id);
  el.style.left ='10%';
  el.style.width ='45%';
  el.style.height ='100%';
  el.style.top ='0%';
  document.getElementById("container_width").style.width='45%';
  document.getElementById("container_bias").style.width='45%';
  document.getElementById("container_efficiency").style.width='45%';
  resize_charts();
  el.style.display = 'none';
}


function hideAsIT_lite(div_id) {
  var el = document.getElementById(div_id);
  if (el.style.width =='90%'){return true;}
  el.style.display = 'none';
  el.style.left ='55%';
}

function hideAsTT_lite(div_id) {
  var el = document.getElementById(div_id);
  if (el.style.width =='90%'){return true;}
  el.style.display = 'none';
  el.style.left ='10%';
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