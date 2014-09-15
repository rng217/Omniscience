from omniscience_tables import *
import difflib

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

# Analyze a Captains Draft screenshot
def screenshot_CD():
    import Image
    import ImageGrab
    import ImageStat
    pool=[]
    screenshot=ImageGrab.grab()
    rescale=float(screenshot.size[0])/1920
    for group in range(6):
        for hero_number_within_group in range(len(hero_group_table[group])):
            if hero_group_table[group][hero_number_within_group] not in cmhero_range: continue #phoenix is a black box and is messing up detection
            blockX,blockY=[(292,267),(630,267),(292,526),(630,526),(292,786),(630,786)][group]
            stats=ImageStat.Stat(screenshot.crop((int((blockX+81*(hero_number_within_group%4)+2)*rescale), int((blockY+46*(hero_number_within_group/4)+2)*rescale),\
                                                      int((blockX+81*(hero_number_within_group%4)+78-2)*rescale), int((blockY+46*(hero_number_within_group/4)+44-2)*rescale))))
            if max(stats.mean)>20.5: #puck is brightest at 20.15
                pool.append(hero_group_table[group][hero_number_within_group])
    return pool

# Analyze a Random Draft screenshot
def screenshot_RD():
    import Image
    import ImageGrab
    import ImageStat
    pool=[]
    screenshot=ImageGrab.grab()
    rescale=float(screenshot.size[0])/1920
    for group in range(6):
        for hero_number_within_group in range(len(hero_group_table[group])):
            blockX,blockY=[(183,235),(183,469),(710,235),(710,469),(1242,235),(1242,469)][group]
            image=screenshot.crop((int((blockX+73*(hero_number_within_group%7)+2)*rescale), int((blockY+73*(hero_number_within_group/7))*rescale),\
                                                      int((blockX+73*(hero_number_within_group%7)+59)*rescale), int((blockY+73*(hero_number_within_group/7)+59)*rescale)))
            brightness=max(ImageStat.Stat(image).mean)
            if heroes[hero_group_table[group][hero_number_within_group]]=="Spectre": brightness+=15 #spectre is super dark
            if brightness>46.6:
                pool.append(hero_group_table[group][hero_number_within_group])
    return pool