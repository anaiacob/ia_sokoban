
def verif(x:int, y:int, targets:list)->bool:
    posy = [l for l, k in targets]
    posx = [k for l, k in targets]
    i=0
    while i<len(targets):
        xt=posx[i]
        yt=posy[i]
        if xt==x and yt==y:
            return False
        i=i+1
    return True

def complet_list_of_wrong_zone(walls:list, height:int, width:int, targets:list) -> list:
    list_of_wrong_zone=[]
    i=0
    posy = [l for l, k in walls]
    posx = [k for l, k in walls]
    while i<len(walls):
        x=posx[i]
        y=posy[i]
        i=i+1
        xinf=x-1
        xsup=x+1
        yinf=y-1
        ysup=y+1
        list_of_wrong_zone.append((y,x))
        if (y == 0 or y == height-1) and verif(x,y,targets)==True and not(x == 0 or x == width-1):
            list_of_wrong_zone.append((y,xinf))
            list_of_wrong_zone.append((y,xsup))
        elif (x == 0 or x == width-1) and verif(x,y,targets)==True and not(y == 0 or y == height-1):
            list_of_wrong_zone.append((yinf,x))            
            list_of_wrong_zone.append((ysup,x))  
        elif x==0 and y==0 and verif(x,y,targets)==True:
            list_of_wrong_zone.append((0,1))
            list_of_wrong_zone.append((1,0))
        elif x==0 and y==height-1 and verif(x,y,targets)==True:
            list_of_wrong_zone.append((yinf,0))
            list_of_wrong_zone.append((y,1))
        elif x==width-1 and y==0 and verif(x,y,targets)==True:
            list_of_wrong_zone.append((0,xinf))
            list_of_wrong_zone.append((1,x))
        elif x==width-1 and y==height-1 and verif(x,y,targets)==True:
            list_of_wrong_zone.append((yinf,x))
            list_of_wrong_zone.append((y,xinf))
    return list_of_wrong_zone