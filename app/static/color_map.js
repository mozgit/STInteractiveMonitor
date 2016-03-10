var summary = {{ summary }};
var variable = 'efficiency';
var type = 'mean';
var it_limits;
var tt_limits;

//function to find limits from variable and type
//functions to modify IT and TT lower and upper limits using the input window

function update_colors() {
  //variable in ['width','bias','efficiency']
  //type in ['min','max','mean']
  //limits is two numbers for example [0, 1]
  //summary - output of get_info_lite function
  //{<id>:{variable:<val>, err_variable:<val>}}
  for (var sector in summary)
  {
    //Check if sector is TT or IT and define actual limits
    document.getElementById(sector).style.backgroundColor=calculate_color( actual_limits, summary[sector]['stats'][variable][type]);
  }
}


function calculate_color(limits, value) {
  if (value == "empty")
  {
    return 'black';
  }
  if (value > limits[1])
  {
    return 'black';
  }
  if (value < limits[0])
  {
    return 'black';
  }
  // (value-limits[0])/(limits[1]-limits[0])
  return 'white'
}


