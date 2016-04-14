function set_layout(map, mode){
  var layer = ['TTaU','TTaX','TTbV','TTbX'];
  var side = ['RegionA','RegionB','RegionC'];
  for (var i_layer in layer){
    //console.log(layer[i_layer]);     
    if (['Ilya','Frederic'].indexOf(mode) >=0 ){
      TT_layer_info_2x2(layer[i_layer]);      
    }
    else{
     TT_layer_info_1x4(layer[i_layer]);
    }
    for (var i_side in side){
      if (['Ilya','Frederic'].indexOf(mode) >=0 ){
        TT_side_info_2x2(layer[i_layer], side[i_side]);
      }
      else{
        TT_side_info_1x4(layer[i_layer], side[i_side]);
      }      
    }
  }

  for (var st_id in map){
    if (st_id.indexOf('TT') == 0){
      var sector = parseInt(st_id.split('Sector')[1])
      var region = "Region"+st_id.split('Sector')[0].split("Region")[1]

      if (mode == "Ilya"){
        TT_div_info_Ilya(st_id, region, sector);  
      }
      if (mode == "Mark"){
        TT_div_info_Mark(st_id, region, sector);  
      }
      if (mode == "Frederic"){
        TT_div_info_Frederic(st_id, region, sector);  
      }


      //TTbVRegionBSector1
    }
  }
}

function TT_div_info_Ilya(det, region, sector){
  var nX = 6;
  var nY = 4;
  var sector_iy = sector-1;
  var sector_ix = sector-1;
  if ((det[2]=='a') && (region == 'RegionB')){
    nX = 3;
    nY = 6;
  }
  if ((det[2]=='b') && (region == 'RegionB')){
      nX = 5;
      if ((sector>4) && (sector<23)){
          sector_iy = sector+1;
          sector_ix = sector+1;
          nY = 6;
        }
      if (sector>22){
          sector_iy = sector-7;
          sector_ix = sector-7;
        }
  }
  var width = parseFloat(100*1./nX).toString()+"%";
  var height = parseFloat(100*1./nY).toString()+"%";
  var top = parseFloat((100*1./nY)*(nY-sector_iy%nY-1)).toString()+"%";
  var left = parseFloat((100*1./nX)*(nX-(sector_ix-sector_ix%nY)/nY-1)).toString()+"%";
  document.getElementById(det).style.width = width;
  document.getElementById(det).style.height = height;
  document.getElementById(det).style.top = top;
  document.getElementById(det).style.left = left;
  return true;

}

function TT_div_info_Mark(det, region, sector){
    var nX = 6;
    var nY = 14;
    var nColumns = 4;
    var nsensors = 4;
    var sector_iy = sector-1;
    var sector_ix = sector-1;
    var special = false;
    var top = 0;
    if (['RegionA', 'RegionC'].indexOf(region)>=0){
        if (((sector%2==0) && (sector%4==2)) || ((sector%2==1) && (sector%4==3))){
            nsensors = 3;
          }
        if (sector%4 == 0){
            top =0;
          }
        else if (sector%4 == 1){
            top = 10./14.*100;
          }
        else if (sector%4 == 2){
            top = 7./14.*100
          }
        else if (sector%4 == 3){
            top = 4./14.*100                        
          }
        }
    else if (det[2]=='a'){        
        nColumns = 6;
        nX = 3;
        special = true;
        if ([6, 12, 18].indexOf(sector) >= 0){
            top = 0;
            nsensors = 4;
          }
        else if ([5, 11, 17].indexOf(sector) >= 0){
            top = 4./14.*100;
            nsensors=2;
          }
        else if ([4, 10, 16].indexOf(sector) >= 0){
            top = 6./14.*100;
            nsensors=1;
          }
        else if ([3, 9, 15].indexOf(sector) >= 0){
            top = 50;
            nsensors = 1;
          }
        else if ([2, 8, 14].indexOf(sector) >= 0){
            top = 8./14.*100;
            nsensors = 2;
          }
        else if ([1, 7, 13].indexOf(sector) >= 0){
            top = 10./14.*100;
            nsensors = 4;
          }
        if ([10, 11, 12].indexOf(sector) >= 0){
            top -=2.5;
          }
        if ([7, 8, 9].indexOf(sector) >= 0){
            top +=2.5;
          }
      }
    else if (det[2]=='b'){
        nX = 5
        special = true
        if ([1, 5, 11, 17, 23].indexOf(sector) >= 0){
            top = 10./14.*100;
            nsensors = 4;
          }
        else if ([4, 10, 16, 22, 26].indexOf(sector) >= 0){
            top = 0;
            nsensors = 4;
          }
        else if ([2, 24].indexOf(sector) >= 0){
            top = 50;
            nsensors = 3;
          }
        else if ([3, 25].indexOf(sector) >= 0){
            top = 4./14.*100;
            nsensors = 3;
          }
        else if ([9, 15, 21].indexOf(sector) >= 0){
            top = 4./14.*100;
            nsensors = 2;
          }            
        else if ([8, 14, 20].indexOf(sector) >= 0){
            top = 6./14.*100;
            nsensors = 1;
          }                        
        else if ([7, 13, 19].indexOf(sector) >= 0){
            top = 50;
            nsensors = 1;
          }            
        else if ([6, 12, 18].indexOf(sector) >= 0){
            top = 8./14.*100;
            nsensors = 2;
          }           
        if ((sector>4) && (sector<23)){
            nColumns = 6;
            sector_ix = sector+1;
          }
        if (sector>22){
            sector_ix = sector-7;
          }
        if ([14, 15, 16].indexOf(sector)>=0){
            top-=2.5;
          }
        if ([11, 12, 13].indexOf(sector)>=0){
            top +=2.5;
          }
        }


    width = parseFloat((100*1./nX)-0.5).toString()+"%"
    height = parseFloat((100./nY*nsensors)-0.5).toString()+"%"
    left = parseFloat((100*1./nX)*(nX-(sector_ix-sector_ix%nColumns)/nColumns-1)).toString()+"%"
    document.getElementById(det).style.width = width;
    document.getElementById(det).style.height = height;
    document.getElementById(det).style.top = top.toString()+"%";
    document.getElementById(det).style.left = left;
    return true

}

function TT_div_info_Frederic(det, region, sector){
    var nX = 6;
    var nY = 14;
    var nColumns = 4;
    var nsensors = 4;
    var sector_iy = sector-1;
    var sector_ix = sector-1;
    var special = false;
    var top = 0;
    if (['RegionA', 'RegionC'].indexOf(region)>=0){
        if (((sector%2==0) && (sector%4==2)) || ((sector%2==1) && (sector%4==3))){
            nsensors = 3;
          }
        if (sector%4 == 0){
            top =0;
          }
        else if (sector%4 == 1){
            top = 10./14.*100;
          }
        else if (sector%4 == 2){
            top = 7./14.*100
          }
        else if (sector%4 == 3){
            top = 4./14.*100                        
          }
        }
    else if (det[2]=='a'){        
        nColumns = 6;
        nX = 3;
        special = true;
        if ([6, 12, 18].indexOf(sector) >= 0){
            top = 0;
            nsensors = 4;
          }
        else if ([5, 11, 17].indexOf(sector) >= 0){
            top = 4./14.*100;
            nsensors=2;
          }
        else if ([4, 10, 16].indexOf(sector) >= 0){
            top = 6./14.*100;
            nsensors=1;
          }
        else if ([3, 9, 15].indexOf(sector) >= 0){
            top = 50;
            nsensors = 1;
          }
        else if ([2, 8, 14].indexOf(sector) >= 0){
            top = 8./14.*100;
            nsensors = 2;
          }
        else if ([1, 7, 13].indexOf(sector) >= 0){
            top = 10./14.*100;
            nsensors = 4;
          }
      }
    else if (det[2]=='b'){
        nX = 5
        special = true
        if ([1, 5, 11, 17, 23].indexOf(sector) >= 0){
            top = 10./14.*100;
            nsensors = 4;
          }
        else if ([4, 10, 16, 22, 26].indexOf(sector) >= 0){
            top = 0;
            nsensors = 4;
          }
        else if ([2, 24].indexOf(sector) >= 0){
            top = 50;
            nsensors = 3;
          }
        else if ([3, 25].indexOf(sector) >= 0){
            top = 4./14.*100;
            nsensors = 3;
          }
        else if ([9, 15, 21].indexOf(sector) >= 0){
            top = 4./14.*100;
            nsensors = 2;
          }            
        else if ([8, 14, 20].indexOf(sector) >= 0){
            top = 6./14.*100;
            nsensors = 1;
          }                        
        else if ([7, 13, 19].indexOf(sector) >= 0){
            top = 50;
            nsensors = 1;
          }            
        else if ([6, 12, 18].indexOf(sector) >= 0){
            top = 8./14.*100;
            nsensors = 2;
          }           
        if ((sector>4) && (sector<23)){
            nColumns = 6;
            sector_ix = sector+1;
          }
        if (sector>22){
            sector_ix = sector-7;
          }
        }


    width = parseFloat((100*1./nX)-0.5).toString()+"%"
    height = parseFloat((100./nY*nsensors)-0.5).toString()+"%"
    left = parseFloat((100*1./nX)*(nX-(sector_ix-sector_ix%nColumns)/nColumns-1)).toString()+"%"
    document.getElementById(det).style.width = width;
    document.getElementById(det).style.height = height;
    document.getElementById(det).style.top = top.toString()+"%";
    document.getElementById(det).style.left = left;
    return true

}


function TT_layer_info_2x2(det){
    document.getElementById("name_"+det).style.width = "100%";
    document.getElementById("name_"+det).style.height = "15%";
    document.getElementById("name_"+det).style.top = "0%";
    document.getElementById("name_"+det).style.left = "0%";
    document.getElementById("position_"+det).style.width = "90%";
    document.getElementById("position_"+det).style.height = "80%";
    document.getElementById("position_"+det).style.top = "15%";
    document.getElementById("position_"+det).style.left = "5%";      
    if (det == 'TTbV'){
        document.getElementById(det).style.top = '0%';
        document.getElementById(det).style.left = '0%';
        document.getElementById(det).style.width ='50%';
        document.getElementById(det).style.height ='50%';
        return true
      }
    if (det == 'TTbX'){
        document.getElementById(det).style.top = '0%';
        document.getElementById(det).style.left = '50%';
        document.getElementById(det).style.width ='50%';
        document.getElementById(det).style.height ='50%';
        return true
      }
    if (det == 'TTaX'){
        document.getElementById(det).style.top = '50%';
        document.getElementById(det).style.left = '0%';
        document.getElementById(det).style.width ='50%';
        document.getElementById(det).style.height ='50%';
        return true
      }
    if (det == 'TTaU'){
        document.getElementById(det).style.top = '50%';
        document.getElementById(det).style.left = '50%';
        document.getElementById(det).style.width ='50%';
        document.getElementById(det).style.height ='50%';
        return true
      }
    return true
  }


function TT_layer_info_1x4(det){
    document.getElementById("name_"+det).style.width = "10%";
    document.getElementById("name_"+det).style.height = "100%";
    document.getElementById("name_"+det).style.top = "0%";
    document.getElementById("name_"+det).style.left = "0%";
    document.getElementById("position_"+det).style.width = "80%";
    document.getElementById("position_"+det).style.height = "90%";
    document.getElementById("position_"+det).style.top = "5%";
    document.getElementById("position_"+det).style.left = "15%";    
    if (det == 'TTbV'){
      document.getElementById(det).style.top= '25%';
      document.getElementById(det).style.left= '0%';
      document.getElementById(det).style.width='100%';
      document.getElementById(det).style.height='25%';
      return true
      }
    if (det == 'TTbX'){
      document.getElementById(det).style.top= '0%';
      document.getElementById(det).style.left= '00%';
      document.getElementById(det).style.width='100%';
      document.getElementById(det).style.height='25%';
      return true
      }
    if (det == 'TTaX'){
      document.getElementById(det).style.top= '75%';
      document.getElementById(det).style.left= '0%';
      document.getElementById(det).style.width='100%';
      document.getElementById(det).style.height='25%';
      return true
      }
    if (det == 'TTaU'){
      document.getElementById(det).style.top= '50%';
      document.getElementById(det).style.left= '0%';
      document.getElementById(det).style.width='100%';
      document.getElementById(det).style.height='25%';
      return true
      }
    return true
  }


function TT_side_info_2x2(a,r){
    if (a[2]=='b'){
        if (r == 'RegionA'){
            var width = parseFloat(6./17*100).toString()+"%";
            var left = ' 0%';
            }        
        else if (r == 'RegionB'){
            var width = parseFloat(5./17*100).toString()+"%";
            var left = parseFloat(6./17*100).toString()+"%";
          }
        else if (r == 'RegionC'){            
            var width = parseFloat(6./17*100).toString()+"%";
            var left = parseFloat(11./17*100).toString()+"%";
          }
    }
    else{
        if (r == 'RegionA'){
            var left = parseFloat(1./17*100).toString()+"%";
            var width = parseFloat(6./17*100).toString()+"%";
          }
        else if (r == 'RegionB'){             
            var left = parseFloat(7./17*100).toString()+"%";
            var width = parseFloat(3./17*100).toString()+"%";
          }
        else if (r == 'RegionC'){
            var left = parseFloat(10./17*100).toString()+"%";
            var width = parseFloat(6./17*100).toString()+"%";      
          }
    }  

    //console.log(a.toString()+r.toString());     
    document.getElementById(a+r).style.top= ' 0%';
    document.getElementById(a+r).style.left= left;
    document.getElementById(a+r).style.width= width;
    document.getElementById(a+r).style.height= '99%';
    return true;
  }


function TT_side_info_1x4(a,r){
    if (a[2]=='b'){
        if (r == 'RegionA'){
            var width = parseFloat(6./17*100-1).toString()+"%";
            var left = ' 0%';
            }        
        else if (r == 'RegionB'){
            var width = parseFloat(5./17*100-1).toString()+"%";
            var left = parseFloat(6./17*100).toString()+"%";
          }
        else if (r == 'RegionC'){            
            var width = parseFloat(6./17*100-1).toString()+"%";
            var left = parseFloat(11./17*100).toString()+"%";
          }
    }
    else{
        if (r == 'RegionA'){
            var left = parseFloat(1./17*100).toString()+"%";
            var width = parseFloat(6./17*100-1).toString()+"%";
          }
        else if (r == 'RegionB'){             
            var left = parseFloat(7./17*100).toString()+"%";
            var width = parseFloat(3./17*100-1).toString()+"%";
          }
        else if (r == 'RegionC'){
            var left = parseFloat(10./17*100).toString()+"%";
            var width = parseFloat(6./17*100-1).toString()+"%";      
          }
    }
    
    //console.log(a.toString()+r.toString());
    document.getElementById(a+r).style.top= ' 0%';
    document.getElementById(a+r).style.left= left;
    document.getElementById(a+r).style.width= width;
    document.getElementById(a+r).style.height= '99%';
    return true;
  }  