from TT_info import *
from IT_info import *


def create_TT_lite():
    TT = {'dtype':'TT'}
    layer = ['TTaU','TTaX','TTbV','TTbX']
    side = ['RegionA','RegionB','RegionC']
    for l in layer:
        TT[l]={'layer_info':TT_layer_info(l)}
        for si in side:
            TT[l][si]={'side_info': TT_side_info(l,si)}
            for s in TT_reg_len(l,si):
                TT[l][si][str(s)] =  {'Name':l+si+'Sector'+str(s)}
                TT[l][si][str(s)]['div_info'] = TT_div_info(l,si,s)
                    #print a+r+'Sector'+str(s)
    return TT


def create_IT_lite():
    IT = {'dtype':'IT'}
    station = ['IT1','IT2','IT3']
    side = ['ASide','CSide','Bottom','Top']
    layer = ['X1','X2','U','V']
    for st in station:
        IT[st]={'station_info':IT_station_info(st)}
        for s in side:
            IT[st][s]= {'side_info':IT_side_info(st,s)}
            for l in layer:
                IT[st][s][l]={'layer_info':IT_layer_info(st,s,l)}
                for n in range(1,8):
                    IT[st][s][l][str(n)] = {'Name':st+s+l+'Sector'+str(n)}
                    IT[st][s][l][str(n)]['div_info'] = IT_div_info(st,s,l,n)
    return IT

