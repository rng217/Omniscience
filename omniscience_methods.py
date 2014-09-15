from omniscience_tables import *
import tkMessageBox
import difflib
import Image
import ImageGrab
import ImageStat

# Odds can be multiplied together easily
def to_odds(x):
    return 1/x-1

# Probabilities are easier for everything else
def to_probability(x):
    return 1/(x+1)

# The winrate for a pair of heroes on the same team. Synergy(X,X) returns the solo winrate for X
def synergy(id1, id2,ranked):
    return data['ranked' if ranked else 'unranked']['synergy'][id1][id2]/data['ranked' if ranked else 'unranked']['synergydivisor'][id1][id2]

# The winrate for id1 when playing against id2. Advantage(X,X) should be empty.
def advantage(id1, id2,ranked):
    return data['ranked' if ranked else 'unranked']['advantage'][id1][id2]/data['ranked' if ranked else 'unranked']['advantagedivisor'][id1][id2]

# Change a hero text string into an ID number. Tolerates abbreviations and misspellings.
def interpret_hero(input):
    hero=abbreviations[difflib.get_close_matches(input.lower(),abbreviations.keys(),1,0)[0]]-1
    return hero

# Determine how far along the picking has progressed based on which entries have been filled out.
def get_next_in_order(order,grid_frame):
    rows=[1,1,None,1,1]
    new_order=""
    first_empty=None
    for char_index in range(len(order)):
        column = "<{?>}".index(order[char_index])
        entry = grid_frame.grid_slaves(rows[column],column)[0]
        rows[column]+=1
        if entry.get()=="":
            new_order+=order[char_index]
            if first_empty==None: first_empty=entry
    return (new_order,first_empty)

# Analyze a Random Draft screenshot
def screenshot_RD():
    pool=[]
    screenshot=ImageGrab.grab()
    rescale=float(screenshot.size[1])/1080
    aspect = 16*screenshot.size[1]/screenshot.size[0]
    if aspect not in hero_group_pixel_offsets_RD:
        tkMessageBox.showerror("Error","Aspect Ratio not supported")
        return
    for group in range(6):
        for hero_number_within_group in range(len(hero_group_table[group])):
            blockX,blockY=hero_group_pixel_offsets_RD[aspect][group]
            offset = 64 if aspect==12 else 73 # The 4:3 icons are smaller
            image=screenshot.crop((int((blockX+offset*(hero_number_within_group%7)+2)*rescale), int((blockY+offset*(hero_number_within_group/7))*rescale),\
                                                      int((blockX+offset*(hero_number_within_group%7)+51)*rescale), int((blockY+offset*(hero_number_within_group/7)+51)*rescale)))
            #image.show()
            brightness=max(ImageStat.Stat(image).mean)
            if heroes[hero_group_table[group][hero_number_within_group]]=="Spectre":
                print brightness
                brightness+=23 #spectre is super dark
            if brightness>46.6:
                pool.append(hero_group_table[group][hero_number_within_group])
    if len(pool)>24 or len(pool)<14: tkMessageBox.showwarning("Warning","Warning! Number of heroes detected ("+str(len(pool))+") is wrong!")
    return pool

# Analyze a Captains Draft screenshot
def screenshot_CD():
    pool=[]
    screenshot=ImageGrab.grab()
    rescale=float(screenshot.size[1])/1080
    aspect = 16*screenshot.size[1]/screenshot.size[0]
    if aspect not in hero_group_pixel_offsets_RD:
        tkMessageBox.showerror("Error","Aspect Ratio not supported")
        return
    for group in range(6):
        for hero_number_within_group in range(len(hero_group_table[group])):
            if hero_group_table[group][hero_number_within_group] not in cmhero_range: continue #phoenix is a black box and is messing up detection
            blockX,blockY=hero_group_pixel_offsets_CD[aspect][group]
            image = screenshot.crop((int((blockX+81*(hero_number_within_group%4)+2)*rescale), int((blockY+46*(hero_number_within_group/4)+2)*rescale),\
                                     int((blockX+81*(hero_number_within_group%4)+78-2)*rescale), int((blockY+46*(hero_number_within_group/4)+44-2)*rescale)))
            #image.show()
            stats=ImageStat.Stat(image)
            if max(stats.mean)>20.5: #puck is brightest at 20.15
                pool.append(hero_group_table[group][hero_number_within_group])
    if len(pool)>27 or len(pool)<11: tkMessageBox.showwarning("Warning","Warning! Number of heroes detected ("+str(len(pool))+") is wrong!")
    return pool