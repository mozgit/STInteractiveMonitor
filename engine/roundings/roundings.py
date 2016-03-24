def split_number(number):
    if number == 0:
        return{'sing':1,'power':0,'digits':'0'}
    sign = 1
    integers = ""
    decimals = ""
    power = 0
    if number<0:
        sign = -1
    integers = str(abs(number)).split(".")[0]
    try:#
        decimals = str(abs(number)).split(".")[1]
    except:
        decimals = ""
    power = len(integers)-1
    if abs(number)<1:
        while (int(number)==0):
            number *=10
            power -=1
    simplified = integers+decimals
    while simplified[len(simplified)-1]=='0':
        simplified = simplified[:-1]
    while simplified[0]=='0':
        simplified=simplified[1:]
    return {'sing':sign,'power':power,'digits':simplified}


def round_up(number, ndigit):
    if number<0:
        return -round_down(-number,ndigit)
    if ndigit < 1:
        #print "Warning in smart schema rounding! (Round Up) ndigit = "+str(ndigit)+", returning original number"
        return number
    simplified = split_number(number)['digits']
    power = split_number(number)['power']
    temp = ""
    if len(simplified)<ndigit:
        #simplified=str(int(simplified)+1)
        while len(simplified)<ndigit:
            simplified+='0'
        for i in range(0, ndigit):
            temp+=simplified[i]
        rn = int(temp)+1
        return float(rn)/10**(len(str(temp))-1)*10**(power)
    for i in range(0, ndigit):
        temp+=simplified[i]
    rn = int(temp)+1
    return float(rn)/10**(len(str(temp))-1)*10**(power)

def round_down(number, ndigit):
    if number<0:
        return -round_down(-number,ndigit)
    if ndigit < 1:
        #print "Warning in smart schema rounding! (Round Down) ndigit = "+str(ndigit)+", returning 0"
        return 0
    simplified = split_number(number)['digits']
    power = split_number(number)['power']
    temp = ""
    if len(simplified)<ndigit:
        simplified=str(int(simplified)+1)
        while len(simplified)<ndigit:
            simplified+='0'
        for i in range(0, ndigit):
            temp+=simplified[i]
        rn = int(temp)-1
        return float(rn)/10**(len(str(temp))-1)*10**(power)
    for i in range(0, ndigit):
        temp+=simplified[i]
    rn = int(temp)-1
    return float(rn)/10**(len(str(temp))-1)*10**(power)



def smart_interval(min_l, max_l, ndigit):
    if min_l == max_l:
        return [min_l, max_l]

    if (min_l<0) and (max_l<0):
        return [-smart_interval(-max_l,-min_l,ndigit)[1],-smart_interval(-max_l,-min_l,ndigit)[0]]
    d_min = split_number(min_l)['digits']
    d_max = split_number(max_l)['digits']
    p_min = split_number(min_l)['power']
    p_max = split_number(max_l)['power']
    if (min_l<0) and (max_l>0):
        return [-round_up(max(max_l,-min_l),2),round_up(max(max_l,-min_l),2)]

    d_pow = p_max-p_min
    if d_pow!=0:
        for i in range(0, d_pow):
            d_min = '0'+d_min


    if len(d_max)<ndigit:
        if len(d_min)<ndigit:
            return [min_l,max_l]
        return [round_down(min_l,ndigit),max_l]
    if len(d_min)<ndigit:
        return [min_l,round_up(max_l,ndigit)]

    counter = 0
    i = 0
    while counter<ndigit:
        #print str(i) + "<"+str(ndigit)+" "+d_max+" "+d_min
        try:
            if d_max[i]!=d_min[i]:
                counter+=1
        except:
            break
        i+=1
    #print "("+str(min_l)+", "+str(max_l)+") ="+str(i)+"=> ("+str(round_down(min_l,i-d_pow))+", "+str(round_up(max_l,i))+")"
    return [round_down(min_l,i-d_pow),round_up(max_l,i)]