#updated 12/1/2013
#Time = 128.56
#Time -O3 = 88.779
#Time -Ofast = 85.175

import cPickle as pickle
import difflib
import string
import math
import Image
import ImageGrab
import ImageStat
import colorsys
from OmniscienceTables import *

tryhard=30/100.

def to_multiplicand(x):
    return 1/x-1
def to_fraction(x):
    return 1/(x+1)
herorange=range(23)+range(24,103)+[105,106]

data=pickle.load(open("data_before_wraith_night.p","rb"))

#for hero in sorted(herorange,key=lambda x:data['RD']['synergydivisor'][x][x],reverse=True):
    #print heroes[hero], data['RD']['synergydivisor'][hero][hero]

modes=['CM','RD','AP']
def synergy(id1, id2):
    return float(sum([data[mode]['synergy'][id1][id2] for mode in modes]))/float(sum([data[mode]['synergydivisor'][id1][id2] for mode in modes]))
def advantage(id1, id2):
    if id1==id2: return 1
    return float(sum([data[mode]['advantage'][id1][id2] for mode in modes]))/float(sum([data[mode]['advantagedivisor'][id1][id2] for mode in modes]))

import omnisciencemodule

try:
    signatures=pickle.load(open("signatures.p","rb"))
except:
    print "Resorting to default signatures."
def warning_level(x):
    if x<=1:
        return ""
    if x<=2:
        return "Warning."
    if x<=3:
        return "Warning!"
    return "WARNING"+"!"*int(x-3)
def recognize_image(im):
    signature=[]
    for p in list(im.resize((2,2), Image.ANTIALIAS).getdata()):
        hs = colorsys.rgb_to_hsv(p[0]/255.0,p[1]/255.0,p[2]/255.0)[0:2]
        signature.append(int(round(hs[0]*255)))
        signature.append(int(round(hs[1]*255)))
    bestguess=-1
    bestguessdifference=99999
    for i in herorange:
        difference=sum([(signature[x]-signatures[i][x])**2 for x in range(8)])
        if difference<bestguessdifference:
            bestguess=i
            bestguessdifference=difference
    if bestguessdifference>100:
        print warning_level(math.sqrt(bestguessdifference)/12),"Unsure about",heroes[bestguess]+"."
        print "    Signature:",signature
        print "    Expected: ",signatures[bestguess]
        print "    Difference:",bestguessdifference
        input=raw_input("Correct Hero: ")
        if input!="":
            bestguess=interpret_hero(input)
            print "    Signature:",signature
            print "    Expected: ",signatures[bestguess]
            print "    Difference:",sum([(signature[x]-signatures[bestguess][x])**2 for x in range(8)])
    signatures[bestguess]=[signature[x]*.15+signatures[bestguess][x]*.85 for x in range(8)]
    return bestguess

def interpret_hero(input):
    hero=abbreviations[difflib.get_close_matches(input.lower(),abbreviations.keys(),1,0)[0]]-1
    print heroes[hero],"recognized."
    return hero

def remove_hero(hero):
    if hero in pool:
        del pool[pool.index(hero)]
    if hero in allies:
        del allies[allies.index(hero)]
    if hero in enemies:
        del enemies[enemies.index(hero)]
    
def consider_enemy(hero):
    remove_hero(hero)
    enemies.append(hero)
        
def consider_ally(hero):
    remove_hero(hero)
    allies.append(hero)

def print_analysis(mode, subset=None):
    if mode[0]=="{": print "Heroes you want to ban [",mode,"]:"
    else: print "Heroes you want to pick [",mode,"]:"
    global allies,enemies,pool
    list=map(to_fraction,omnisciencemodule.analyze([herorange.index(i) for i in pool],[herorange.index(i) for i in allies],[herorange.index(i) for i in enemies],mode))
    order=sorted(filter(lambda x:list[x]!=1 and (not subset or (herorange[x] in subset)),range(len(list))),key=lambda id: list[id],reverse=True)
    printlength=min(20,len(order)-1)
    rankrange=max(.000001,list[order[0]] - list[order[printlength]])
    for i in range(printlength):
        print "{:<4}{:<7.2f}{:<42}{}".format(\
            i+1,\
            100*list[order[i]],\
            '='*int((list[order[i]]-list[order[printlength]])*40/rankrange+.5),\
            heroes[herorange[order[i]]])
    print ""

print "\n====The Omniscience v5===="
print "Prefix allies with !"
print "Remove heroes with -"
print "AP: All pick\nCM: Captain's Mode\nRD: Random Draft\nRCM: Reverse Captains Mode\nCD: Captain's Draft"
mode=string.upper(raw_input("Mode: "))

allies=[]
enemies=[]
pool=list(herorange)

if mode=='CM':
    omnisciencemodule.load_data([[to_multiplicand(synergy(a,b)) for a in herorange] for b in herorange],\
                                [[to_multiplicand(advantage(a,b)) for a in herorange] for b in herorange],\
                                [data['CM']['synergydivisor'][a][a] for a in herorange], tryhard)
    remove_hero(interpret_hero("broodmother"))
    remove_hero(interpret_hero("ember spirit"))
    remove_hero(interpret_hero("earth spirit"))
    if raw_input("Do you have first ban (y/n)? ")=='y':
        print_analysis("{}{}<>>")
        remove_hero(interpret_hero(raw_input("Your first ban: ")))
        print_analysis("{}<>>")
        remove_hero(interpret_hero(raw_input("Their first ban: ")))
        print_analysis("{}<>>")
        remove_hero(interpret_hero(raw_input("Your second ban: ")))
        print_analysis("<>><")
        remove_hero(interpret_hero(raw_input("Their second ban: ")))
        print_analysis("<>><")
        consider_ally(interpret_hero(raw_input("Your first pick: ")))
        print_analysis("<{}{}><>")
        consider_enemy(interpret_hero(raw_input("Their first pick: ")))
        print_analysis("<{}{}><>")
        consider_enemy(interpret_hero(raw_input("Their second pick: ")))
        print_analysis("<{}{}><>")
        consider_ally(interpret_hero(raw_input("Your second pick: ")))
        print_analysis("{}{}><>")
        remove_hero(interpret_hero(raw_input("Your third ban: ")))
        print_analysis("{}><>")
        remove_hero(interpret_hero(raw_input("Their third ban: ")))
        print_analysis("{}><>")
        remove_hero(interpret_hero(raw_input("Your fourth ban: ")))
        print_analysis("<><}{>")
        remove_hero(interpret_hero(raw_input("Their fourth ban: ")))
        print_analysis("<><}{>")
        consider_enemy(interpret_hero(raw_input("Their third pick: ")))
        print_analysis("<><}{>")
        consider_ally(interpret_hero(raw_input("Your third pick: ")))
        print_analysis("<}{><")
        consider_enemy(interpret_hero(raw_input("Their fourth pick: ")))
        print_analysis("<}{><")
        consider_ally(interpret_hero(raw_input("Your fourth pick: ")))
        print_analysis("{><")
        remove_hero(interpret_hero(raw_input("Their fifth ban: ")))
        print_analysis("{><")
        remove_hero(interpret_hero(raw_input("Your fifth ban: ")))
        print_analysis("<")
        consider_enemy(interpret_hero(raw_input("Their fifth pick: ")))
        print_analysis("<")
    else:
        remove_hero(interpret_hero(raw_input("Their first ban: ")))
        print_analysis("{}{><<")
        remove_hero(interpret_hero(raw_input("Your first ban: ")))
        print_analysis("{><<")
        remove_hero(interpret_hero(raw_input("Their second ban: ")))
        print_analysis("{><<")
        remove_hero(interpret_hero(raw_input("Your second ban: ")))
        print_analysis("<<>}{}{<")
        consider_enemy(interpret_hero(raw_input("Their first pick: ")))
        print_analysis("<<>}{}{<")
        consider_ally(interpret_hero(raw_input("Your first pick: ")))
        print_analysis("<>}{}{<>")
        consider_ally(interpret_hero(raw_input("Your second pick: ")))
        print_analysis("{}{<>")
        consider_enemy(interpret_hero(raw_input("Their second pick: ")))
        print_analysis("{}{<>")
        remove_hero(interpret_hero(raw_input("Their third ban: ")))
        print_analysis("{}{<>")
        remove_hero(interpret_hero(raw_input("Your third ban: ")))
        print_analysis("{<><")
        remove_hero(interpret_hero(raw_input("Their fourth ban: ")))
        print_analysis("{<><")
        remove_hero(interpret_hero(raw_input("Your fourth ban: ")))
        print_analysis("<><>")
        consider_ally(interpret_hero(raw_input("Your third pick: ")))
        print_analysis("<>{}<>")
        consider_enemy(interpret_hero(raw_input("Their third pick: ")))
        print_analysis("<>{}<>")
        consider_ally(interpret_hero(raw_input("Your fourth pick: ")))
        print_analysis("{}<>")
        consider_enemy(interpret_hero(raw_input("Their fourth pick: ")))
        print_analysis("{}<>")
        remove_hero(interpret_hero(raw_input("Your fifth ban: ")))
        print_analysis("<>")
        remove_hero(interpret_hero(raw_input("Their fifth ban: ")))
        print_analysis("<>")
elif mode=='RD':
    omnisciencemodule.load_data([[to_multiplicand(synergy(a,b)) for a in herorange] for b in herorange],\
                                      [[to_multiplicand(advantage(a,b)) for a in herorange] for b in herorange],\
                                      [data['RD']['synergydivisor'][a][a] for a in herorange], tryhard)
    pool=[]
    screenshot=ImageGrab.grab((0,0,1920,1080))
    for x in [766,868,970,1071]:
        im=screenshot.crop((x,280,x+68,348))
        hero=recognize_image(im)
        print ">"+heroes[hero]
        pool.append(hero)
    for x in [471,583,695,807,919,1031,1143,1255,1367]:
        im=screenshot.crop((x,376,x+76,452))
        hero=recognize_image(im)
        print ">"+heroes[hero]
        pool.append(hero)
    for x in [426,548,671,793,915,1038,1160,1282,1405]:
        im=screenshot.crop((x,483,x+83,566))
        hero=recognize_image(im)
        print ">"+heroes[hero]
        pool.append(hero)
    pickle.dump(signatures,open("signatures.p","wb"))
    if raw_input("Do you have first pick (y/n)").lower()=='y':
        print_analysis("<>><<")
        print_analysis("<>><<>")
        consider_ally(interpret_hero(raw_input("Your first pick: ")))
        print_analysis("<<>><")
        consider_enemy(interpret_hero(raw_input("Their first pick: ")))
        print_analysis("<<>><")
        consider_enemy(interpret_hero(raw_input("Their second pick: ")))
        print_analysis("<<>><")
        consider_ally(interpret_hero(raw_input("Your second pick: ")))
        print_analysis("<>><<")
        print_analysis("<>><<>")
        consider_ally(interpret_hero(raw_input("Your third pick: ")))
        print_analysis("<<>")
        consider_enemy(interpret_hero(raw_input("Their third pick: ")))
        print_analysis("<<>")
        consider_enemy(interpret_hero(raw_input("Their fourth pick: ")))
        print_analysis("<<>")
        consider_ally(interpret_hero(raw_input("Your fourth pick: ")))
        print_analysis("<>")
    else:
        consider_enemy(interpret_hero(raw_input("Their first pick: ")))
        print_analysis("<<>><")
        consider_ally(interpret_hero(raw_input("Your first pick: ")))
        print_analysis("<>><<")
        print_analysis("<>><<>")
        consider_ally(interpret_hero(raw_input("Your second pick: ")))
        print_analysis("<<>><")
        consider_enemy(interpret_hero(raw_input("Their second pick: ")))
        print_analysis("<<>><")
        consider_enemy(interpret_hero(raw_input("Their third pick: ")))
        print_analysis("<<>><")
        consider_ally(interpret_hero(raw_input("Your third pick: ")))
        print_analysis("<>><")
        consider_ally(interpret_hero(raw_input("Your fourth pick: ")))
        print_analysis("<")
        consider_enemy(interpret_hero(raw_input("Their fourth pick: ")))
        print_analysis("<")
        consider_enemy(interpret_hero(raw_input("Their fifth pick: ")))
        print_analysis("<")
elif mode=="TEST":
    omnisciencemodule.load_data([[to_multiplicand(synergy(a,b)) for a in herorange] for b in herorange],\
                                      [[to_multiplicand(advantage(a,b)) for a in herorange] for b in herorange],\
                                      [data['AP']['synergydivisor'][a][a] for a in herorange], tryhard)
    import time
    start=time.clock()
    print_analysis("<<<<<")
    end=time.clock()
    print end-start
elif mode=="CD":
    pool=[]
    #blockSizes=[19,15,17,15,18,19]
    screenshot=ImageGrab.grab((0,0,1920,1080))
    heroTable=[[6, 17, 18, 22, 37, 48, 50, 56, 58, 72, 77, 82, 90, 95, 97, 98, 99, 102, 106],
               [1, 13, 15, 27, 28, #41, RIP skeleton king
                                   53, 59, 68, 70, 76, 80, 84, 96, 101],
               [0, 5, 7, 8, 9, 11, 19, 31, 34, 45, 47, 61, 69, 71, 79, 88, 94, 105],
               [3, 10, 14, 39, 40, 43, 46, 55, 60, 62, 66, 81, 87, 92, 93],
               [4, 12, 16, 20, 21, 24, 26, 33, 52, 57, 63, 65, 74, 83, 85, 86, 89, 100],
               [2, 30, 25, 29, 32, 35, 36, 38, 42, 44, 49, 51, 54, 64, 67, 73, 75, 78, 91]]
    omnisciencemodule.load_data([[to_multiplicand(synergy(a,b)) for a in herorange] for b in herorange],\
                                      [[to_multiplicand(advantage(a,b)) for a in herorange] for b in herorange],\
                                      [data['CD']['synergydivisor'][a][a] for a in herorange], tryhard)
    for block in range(6):
        for heroNumberWithinBlock in range(len(heroTable[block])):
            blockX,blockY=[(292,267),(630,267),(292,526),(630,526),(292,786),(630,786)][block]
            stats=ImageStat.Stat(screenshot.crop((blockX+81*(heroNumberWithinBlock%4)+2, blockY+46*(heroNumberWithinBlock/4),\
                                                      blockX+81*(heroNumberWithinBlock%4)+78-2,blockY+46*(heroNumberWithinBlock/4)+44-2)))
            if max(stats.mean)>20:
                pool.append(heroTable[block][heroNumberWithinBlock])
                print heroes[pool[-1]],max(stats.mean)
    if raw_input("Do you have first ban (y/n)? ")=='y':
        print_analysis("{}{}<>><")
        print_analysis("{}{}<>><<")
        remove_hero(interpret_hero(raw_input("Your first ban: ")))
        print_analysis("{}<>><")
        remove_hero(interpret_hero(raw_input("Their first ban: ")))
        print_analysis("{}<>><")
        print_analysis("{}<>><<")
        remove_hero(interpret_hero(raw_input("Your second ban: ")))
        print_analysis("<>><<")
        remove_hero(interpret_hero(raw_input("Their second ban: ")))
        print_analysis("<>><<")
        print_analysis("<>><<>")
        consider_ally(interpret_hero(raw_input("Your first pick: ")))
        print_analysis("<<>><")
        consider_enemy(interpret_hero(raw_input("Their first pick: ")))
        print_analysis("<<>><")
        consider_enemy(interpret_hero(raw_input("Their second pick: ")))
        print_analysis("<<>><")
        print_analysis("<<>><<")
        consider_ally(interpret_hero(raw_input("Your second pick: ")))
        print_analysis("<>><<")
        print_analysis("<>><<>")
        consider_ally(interpret_hero(raw_input("Your third pick: ")))
        print_analysis("<<>")
        consider_enemy(interpret_hero(raw_input("Their third pick: ")))
        print_analysis("<<>")
        consider_enemy(interpret_hero(raw_input("Their fourth pick: ")))
        print_analysis("<<>")
        consider_ally(interpret_hero(raw_input("Your fourth pick: ")))
        print_analysis("<>")
    else:
        print_analysis("{}{><<>")
        remove_hero(interpret_hero(raw_input("Their first ban: ")))
        print_analysis("{}{><<>")
        print_analysis("{}{><<>>")
        remove_hero(interpret_hero(raw_input("Your first ban: ")))
        print_analysis("{><<>")
        remove_hero(interpret_hero(raw_input("Their second ban: ")))
        print_analysis("{><<>")
        print_analysis("{><<>>")
        remove_hero(interpret_hero(raw_input("Your second ban: ")))
        print_analysis("<<>><")
        consider_enemy(interpret_hero(raw_input("Their first pick: ")))
        print_analysis("<<>><")
        print_analysis("<<>><<")
        consider_ally(interpret_hero(raw_input("Your first pick: ")))
        print_analysis("<>><<")
        print_analysis("<>><<>")
        consider_ally(interpret_hero(raw_input("Your second pick: ")))
        print_analysis("<<>><")
        consider_enemy(interpret_hero(raw_input("Their second pick: ")))
        print_analysis("<<>><")
        consider_enemy(interpret_hero(raw_input("Their third pick: ")))
        print_analysis("<<>><")
        consider_ally(interpret_hero(raw_input("Your third pick: ")))
        print_analysis("<>><")
        consider_ally(interpret_hero(raw_input("Your fourth pick: ")))
        print_analysis("<")
        consider_enemy(interpret_hero(raw_input("Their fourth pick: ")))
        print_analysis("<")
        consider_enemy(interpret_hero(raw_input("Their fifth pick: ")))
        print_analysis("<")
else:
    omnisciencemodule.load_data([[to_multiplicand(synergy(a,b)) for a in herorange] for b in herorange],\
                                      [[to_multiplicand(advantage(a,b)) for a in herorange] for b in herorange],\
                                      [data['AP']['synergydivisor'][a][a] for a in herorange], tryhard)
    while True:
        print_analysis("<")
        hero=raw_input("Input: ")
        if hero[0]=='!':
            consider_ally(interpret_hero(hero[1:]))
        elif hero[0]=='-':
            remove_hero(interpret_hero(hero[1:]))
        elif hero[0]=='+':
            hero_id=interpret_hero(hero[1:])
            remove_hero(hero_id)
            pool.append(hero_id)
        elif hero[0]=='#':
            oldpool=pool
            hero=difflib.get_close_matches(hero[1:].lower(),heroTypes.keys()+abbreviations.keys(),1,0)[0]
            if hero in abbreviations:
                print_analysis("<",[abbreviations[hero]-1])
            else:
                print_analysis("<",filter(lambda x: heroes[x] in heroTypes[hero],pool))
            pool=oldpool
        elif hero[0]=='@':
            print_analysis(hero[1:])
        else:
            consider_enemy(interpret_hero(hero))
raw_input("Done.")