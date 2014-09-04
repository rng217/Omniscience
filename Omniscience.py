# Copyright 2014 Daniel Wilson
#updated 7/27/2014

from OmniscienceMethods import *
import difflib
from Tkinter import *
import omnisciencemodule

masterPool=[]
root = Tk()
root.title("Omniscience")
root.wm_iconbitmap('Repel.ico')
root.resizable(0, 0)

radioFrame = Frame(root)
radioFrame.pack(fill=X)
scaleFrame = Frame(root)
scaleFrame.pack(fill=X)
gridFrame = Frame(root)
gridFrame.pack(fill=X)

gamemode = StringVar()
pickfirst = BooleanVar()
ranked = BooleanVar()

Radiobutton(radioFrame,text="All Pick",variable=gamemode,value="AP",indicatoron=0).pack(side=LEFT)
Radiobutton(radioFrame,text="Captains Mode",variable=gamemode,value="CM",indicatoron=0).pack(side=LEFT)
Radiobutton(radioFrame,text="Random Draft",variable=gamemode,value="RD",indicatoron=0).pack(side=LEFT)
Radiobutton(radioFrame,text="Captains Draft",variable=gamemode,value="CD",indicatoron=0).pack(side=LEFT)

Checkbutton(radioFrame,text="First Pick",variable=pickfirst).pack(side=LEFT)
Checkbutton(radioFrame,text="Ranked",variable=ranked).pack(side=LEFT)

def screenshot(*args):
    global masterPool, pickButton
    if gamemode.get()=="CD":
        masterPool=screenshot_CD()
        banButton.config(state=NORMAL)
    elif gamemode.get()=="RD":
        masterPool=screenshot_RD()
    pickButton.config(state=NORMAL)

screenshotButton=Button(radioFrame,text="Analyze Screenshot",command=screenshot)
screenshotButton.pack(side=RIGHT)

import webbrowser

def about(*args):
    about=Toplevel()
    about.title("Help / About")
    about.resizable(0, 0)
    txt=Text(about, font="Times", wrap=WORD)
    txt.pack()
    txt.insert(END,
    "Data completeness: "+str(sum([sum([data['unranked']['advantagedivisor'][a][b] for a in heroRange]) for b in heroRange])/len(heroRange)**2/100)+"%\n\n"+\
    "The Omniscience is a program that assists with hero selection in the game Dota 2. It uses statistics and a large database of games played previously to suggest heroes that work well with or against the heroes already selected.\n\n"+\
    "The Omniscience is aware of the order in which the picks occur in the various modes. After pressing the Picks button or the Bans button, the entry box that you are expected to fill out next will be selected.\n\n"+\
    "A screenshot can be analyzed to figure out the available hero pool in the Captain's Draft or Random Draft modes. Simply make sure the Omniscience window is not covering any of the hero boxes (suggested locations are the bottom of the screen or on a second monitor) and press the Analyze Screenshot button. Make sure your game is set to Borderless Window in video options to avoid having the game minimize while you do this. In Random Draft you must first press Grid View on the right and then check the Show All Heroes checkbox at the top. Only the default hero grid and 16:9 widescreen resolutions are supported.\n\n"+\
    "Remember that while the Omniscience can take into account the relationships among the heroes in play, the pool available, and the winrate and popularity of the heroes, it does not account for team/lane composition or what heroes each person is good at playing. These factors are at least as important as the hero picks themselves, so you must still use your judgement when picking.\n\n"+\
    "Copyright 2014 Daniel Wilson")
    version_frame = Frame(about)
    version_frame.pack(fill=X)
    Label(version_frame,text="Version 1.00").pack(side=LEFT)
    Button(version_frame,text="Check web page for updates",command=lambda:webbrowser.open("https://dl.dropboxusercontent.com/u/16143985/data.zip")).pack(side=RIGHT)

Button(radioFrame,text="About",command=about).pack(side=RIGHT)

Label(scaleFrame,text="Situationality of hero selection:").pack(side=LEFT)
situationalityScale = Scale(scaleFrame,orient=HORIZONTAL, from_=50)
situationalityScale.set(70)
situationalityScale.pack(side=LEFT)
suggestabilityScale = Scale(scaleFrame,orient=HORIZONTAL)
suggestabilityScale.set(50)
suggestabilityScale.pack(side=RIGHT)
Label(scaleFrame,text="Chance you will select the recommended hero:").pack(side=RIGHT)

Label(gridFrame,text="Your Picks").grid(row=0,column=0)
Label(gridFrame,text="Your Bans").grid(row=0,column=1)
Label(gridFrame,text="Their Picks").grid(row=0,column=3)
Label(gridFrame,text="Their Bans").grid(row=0,column=4)

for column in [0,1,3,4]:
    for row in range(1,6):
        Entry(gridFrame).grid(row=row,column=column)

def validate_all():
    for row in range(1,6):
        for column in [0,1,3,4]:
            validate_entry(gridFrame.grid_slaves(row,column)[0])
def validate(event):
    validate_entry(event.widget)
def validate_entry(widget):
    if widget.get() == "": return
    hero_id=interpret_hero(widget.get())
    widget.delete(0,END)
    widget.insert(0,heroes[hero_id])
for column in [0,1,3,4]:
    for row in range(1,6):
        entry = gridFrame.grid_slaves(row,column)[0]
        entry.bind("<Return>",validate)
        entry.bind("<FocusOut>",validate)

pickBox = Frame(gridFrame)
pickText = Text(pickBox)
pickScroll = Scrollbar(pickBox,command=pickText.yview)
pickText.config(yscrollcommand=pickScroll.set)

pickBox.grid(row=7,column=0,columnspan=5)
pickText.pack(side=LEFT)
pickScroll.pack(side=RIGHT, fill=Y)

def refresh_picks():
    refresh("<")
def refresh_bans():
    refresh("{")
def refresh(firstChar):
    omnisciencemodule.load_settings(1-situationalityScale.get()/100.,1-suggestabilityScale.get()/100.)
    order=orders[gamemode.get()]
    if gamemode.get()!="AP":
        if not pickfirst.get(): order=order.translate(switchsides_trans)
        (order,nextBox)=getNextInOrder(order,gridFrame)
        order=order[order.index(firstChar):]
        while order.count("<",1)+order.count(">",1) > modeSearchDepths[gamemode.get()] or order.endswith("{") or order.endswith("}"):
            order=order[:-1]
        nextBox.focus_set()

    validate_all()

    allies=[]
    enemies=[]
    pool=list(masterPool)
    
    for row in range(1,6):
        hero=gridFrame.grid_slaves(row,0)[0].get()
        if hero:
            hero = heroes.index(hero)
            allies.append(hero)
            if hero in pool: pool.remove(hero)

        hero=gridFrame.grid_slaves(row,1)[0].get()
        if hero:
            hero = heroes.index(hero)
            if hero in pool: pool.remove(hero)

        hero=gridFrame.grid_slaves(row,3)[0].get()
        if hero:
            hero = heroes.index(hero)
            enemies.append(hero)
            if hero in pool: pool.remove(hero)

        hero=gridFrame.grid_slaves(row,4)[0].get()
        if hero:
            hero = heroes.index(hero)
            if hero in pool: pool.remove(hero)
    heroQuality=map(to_fraction,omnisciencemodule.analyze([heroRange.index(i) for i in pool],
                                                          [heroRange.index(i) for i in allies],
                                                          [heroRange.index(i) for i in enemies],order))
    heroQuality=[0 if i not in pool else heroQuality[heroRange.index(i)] for i in range(len(heroes))]
    order=sorted(pool,key=lambda id: heroQuality[id],reverse=True)
    pickText.delete("0.0",END)
    rankrange=max(.000001,float(heroQuality[order[0]]-heroQuality[order[-1]]))
    width=55
    for i in range(len(order)):
        normalized=int((heroQuality[order[i]]-heroQuality[order[-1]])*2*width/rankrange-width)
        pickText.insert(END,"{:<3} {:<20} {}\n".format(\
            i+1,\
            heroes[order[i]],\
            "="*normalized+" "*min(width-normalized,width+normalized)+"="*-normalized))

pickButton=Button(gridFrame,text="Picks",command=refresh_picks)
pickButton.grid(row=6,column=0)
banButton=Button(gridFrame,text="Bans", command=refresh_bans)
banButton.grid(row=6,column=1)

def gamemode_changed(*args):
    global masterPool
    masterPool=list(cmHeroRange if gamemode.get().startswith("C") else heroRange)
    omnisciencemodule.load_data([[to_multiplicand(synergy(a,b,ranked.get())) for a in heroRange] for b in heroRange],\
                                [[to_multiplicand(advantage(a,b,ranked.get())) for a in heroRange] for b in heroRange],\
                                [data['ranked' if ranked.get() and not gamemode.get()=="RD" else 'unranked'][gamemode.get()]['popularity'][a] for a in heroRange])
    banButton.config(state=NORMAL if gamemode.get()=="CM" else DISABLED)
    if gamemode.get()=="AP" or gamemode.get()=="CM":
        screenshotButton.config(state=DISABLED)
        pickButton.config(state=NORMAL)
    else:
        screenshotButton.config(state=NORMAL)
        pickButton.config(state=DISABLED)
        
gamemode.trace("w",gamemode_changed)
ranked.trace("w",gamemode_changed)
gamemode.set("AP")

root.mainloop()