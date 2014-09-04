# Copyright 2014 Daniel Wilson

from OmniscienceTables import *
import difflib

def to_multiplicand(x):
    #return 1/max(x,0.0000001)-1
    return 1/x-1

def to_fraction(x):
    #return 1/(max(x+1,0.0000001))
    return 1/(x+1)

def synergy(id1, id2,ranked):
    return data['ranked' if ranked else 'unranked']['synergy'][id1][id2]/data['ranked' if ranked else 'unranked']['synergydivisor'][id1][id2]

def advantage(id1, id2,ranked):
    return data['ranked' if ranked else 'unranked']['advantage'][id1][id2]/data['ranked' if ranked else 'unranked']['advantagedivisor'][id1][id2]

def interpret_hero(input):
    hero=abbreviations[difflib.get_close_matches(input.lower(),abbreviations.keys(),1,0)[0]]-1
    return hero

def getNextInOrder(order,gridFrame):
    rows=[1,1,None,1,1]
    newOrder=""
    firstEmpty=None
    for charIndex in range(len(order)):
        column = "<{?>}".index(order[charIndex])
        entry = gridFrame.grid_slaves(rows[column],column)[0]
        rows[column]+=1
        if entry.get()=="":
            newOrder+=order[charIndex]
            if firstEmpty==None: firstEmpty=entry
    return (newOrder,firstEmpty)

def screenshot_CD():
    import Image
    import ImageGrab
    import ImageStat
    pool=[]
    screenshot=ImageGrab.grab()
    rescale=float(screenshot.size[0])/1920
    for group in range(6):
        for heroNumberWithinGroup in range(len(heroGroupTable[group])):
            if heroGroupTable[group][heroNumberWithinGroup] not in cmHeroRange: continue #phoenix is a black box and is messing up detection
            blockX,blockY=[(292,267),(630,267),(292,526),(630,526),(292,786),(630,786)][group]
            stats=ImageStat.Stat(screenshot.crop((int((blockX+81*(heroNumberWithinGroup%4)+2)*rescale), int((blockY+46*(heroNumberWithinGroup/4)+2)*rescale),\
                                                      int((blockX+81*(heroNumberWithinGroup%4)+78-2)*rescale), int((blockY+46*(heroNumberWithinGroup/4)+44-2)*rescale))))
            if max(stats.mean)>20.5: #puck is brightest at 20.15
                pool.append(heroGroupTable[group][heroNumberWithinGroup])
    return pool

def screenshot_RD():
    import Image
    import ImageGrab
    import ImageStat
    pool=[]
    screenshot=ImageGrab.grab()
    rescale=float(screenshot.size[0])/1920
    for group in range(6):
        for heroNumberWithinGroup in range(len(heroGroupTable[group])):
            blockX,blockY=[(183,235),(183,469),(710,235),(710,469),(1242,235),(1242,469)][group]
            image=screenshot.crop((int((blockX+73*(heroNumberWithinGroup%7)+2)*rescale), int((blockY+73*(heroNumberWithinGroup/7))*rescale),\
                                                      int((blockX+73*(heroNumberWithinGroup%7)+59)*rescale), int((blockY+73*(heroNumberWithinGroup/7)+59)*rescale)))
            brightness=max(ImageStat.Stat(image).mean)
            if heroes[heroGroupTable[group][heroNumberWithinGroup]]=="Spectre": brightness+=15 #spectre is super dark
            if brightness>46.6:
                pool.append(heroGroupTable[group][heroNumberWithinGroup])
    return pool