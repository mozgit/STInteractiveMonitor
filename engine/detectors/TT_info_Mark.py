"""
These functions define position and drawing style of every single element of TT.
"""

def TT_reg_len(det,region):
    top = 25
    if ((det[2]=='a') and (region == 'RegionB')):
        top = 19
    if ((det[2]=='b') and (region == 'RegionB')):
        top = 27
    return range(1, top)


def TT_div_info(det, region, sector):
    nX = 6
    nY = 14
    nColumns = 4
    nsensors = 4
    sector_iy = sector-1
    sector_ix = sector-1
    special = False
    scale = 1.
    if region in ['RegionA', 'RegionC']:
        if ((sector%2==0) and (sector%4==2)) or ((sector%2==1) and (sector%4==3)):
            nsensors = 3
        if (sector%4 == 0):
            top =0
        elif (sector%4 == 1):
            top = 10./14.*100
        elif (sector%4 == 2):
            top = 7./14.*100
        elif (sector%4 == 3):
            top = 4./14.*100                        
    elif (det[2]=='a'):        
    #if ((det[2]=='a') and (region == 'RegionB')):
        nColumns = 6
        nX = 3
        special = True
        if sector in [6, 12, 18]:
            top = 0
            nsensors = 4
        elif sector in [5, 11, 17]:
            top = 4./14.*100
            nsensors=2
        elif sector in [4, 10, 16]:
            top = 6./14.*100
            nsensors=1
        elif sector in [3, 9, 15]:
            top = 50
            nsensors = 1
        elif sector in [2, 8, 14]:
            top = 8./14.*100
            nsensors = 2
        elif sector in [1, 7, 13]:
            top = 10./14.*100
            nsensors = 4
        if sector in [10, 11, 12]:
            top -=2.5
        if sector in [7, 8, 9]:
            top +=2.5

    elif (det[2]=='b'):
    #if ((det[2]=='b') and (region == 'RegionB')):
        nX = 5
        special = True
        if sector in [1, 5, 11, 17, 23]:
            top = 10./14.*100
            nsensors = 4
        elif sector in [4, 10, 16, 22, 26]:
            top = 0
            nsensors = 4
        elif sector in [2, 24]:
            top = 50
            nsensors = 3
        elif sector in [3, 25]:
            top = 4./14.*100
            nsensors = 3            
        elif sector in [9, 15, 21]:
            top = 4./14.*100
            nsensors = 2            
        elif sector in [8, 14, 20]:
            top = 6./14.*100
            nsensors = 1                        
        elif sector in [7, 13, 19]:
            top = 50
            nsensors = 1            
        elif sector in [6, 12, 18]:
            top = 8./14.*100
            nsensors = 2           
        if ((sector>4) and (sector<23)):
            nColumns = 6
            sector_ix = sector+1
        if (sector>22):
            sector_ix = sector-7
        if sector in [14, 15, 16]:
            top-=2.5
        if sector in [11, 12, 13]:
            top +=2.5


    width = str(float(100*1./nX)-0.5)+"%"
    height = str(float(100./nY*nsensors)-0.5)+"%"
    #top = str(float(100*1./nY)*(nY-sector_iy%nY-1))+"%"
    left = str(float(100*1./nX)*(nX-int((sector_ix-sector_ix%nColumns)/nColumns)-1))+"%"
    return {'width':width, 
            'height':height, 
            'top':str(top)+"%", 
            'left':left,
            'position':'absolute',
            'border':' 1px solid #000000',
            'text-align':'center'}


def TT_layer_info(a):
    if a == 'TTbV':
        return {'position':'absolute',
                'top': '25%',
                'left': '0%',
                'width':'100%',
                'height':'25%',
                'border':'1px dashed'}
    if a == 'TTbX':
        return {'position':'absolute',
                'top': '0%',
                'left': '00%',
                'width':'100%',
                'height':'25%',
                'border':'1px dashed'}
    if a == 'TTaX':
        return {'position':'absolute',
                'top': '75%',
                'left': '0%',
                'width':'100%',
                'height':'25%',
                'border':'1px dashed'}
    if a == 'TTaU':
        return {'position':'absolute',
                'top': '50%',
                'left': '0%',
                'width':'100%',
                'height':'25%',
                'border':'1px dashed'}
    return {}


def TT_side_info(a,r):
    #width = '32%'
    if (a[2]=='b'):        
        if (r == 'RegionA'): 
            width = str(6./17*100)+"%"
            left = ' 0%'            
        elif (r == 'RegionB'): 
            width = str(5./17*100)+"%"
            left = str(6./17*100)+"%"
        elif (r == 'RegionC'):            
            width = str(6./17*100)+"%"
            left = str(11./17*100)+"%"
    else:
        if (r == 'RegionA'): 
            left = str(1./17*100)+"%"
            width = str(6./17*100)+"%"          
        elif (r == 'RegionB'):             
            left = str(7./17*100)+"%"
            width = str(3./17*100)+"%"         
        elif (r == 'RegionC'):
            left = str(10./17*100)+"%"
            width = str(6./17*100)+"%"             
    return {'position':'absolute',
            #'border':' 1px solid ',
            'top':' 0%',
            'left': left,
            'width':width,
            'height':'99%'}