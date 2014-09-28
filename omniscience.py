import difflib
import webbrowser
from omniscience_tables import *
from omniscience_methods import * # These are not good, reorganize
from Tkinter import *
import time
import _omniscience # The part written in C

# Setting up the highest level UI elements
master_pool=[]
root = Tk()

## Display amount of data loaded so far
#divisor_total = {'ranked':0,'unranked':0}
#for r in ['ranked','unranked']:
#    for m in ['synergydivisor','advantagedivisor']:
#        for a in hero_range:
#            for b in hero_range:
#                divisor_total[r] += data[r][m][a][b]
#    for m in ['AP','RD','CM','CD']:
#        print r,m,data[r][m]['popularitydivisor']
#print "Adv/Syn completeness ranked: "+str(round(100.*divisor_total['ranked']/len(hero_range)**2/2/5000,2))+"%"
#print "Adv/Syn completeness unranked: "+str(round(100.*divisor_total['unranked']/len(hero_range)**2/2/5000,2))+"%"

root.title("Omniscience v1.10")
root.wm_iconbitmap('Repel.ico')
root.resizable(0, 0)

radio_frame = Frame(root)
radio_frame.pack(fill=X)
scale_frame = Frame(root)
scale_frame.pack(fill=X)
grid_frame = Frame(root)
grid_frame.pack(fill=X)

game_mode = StringVar()
pick_first = BooleanVar()
ranked = BooleanVar()

Radiobutton(radio_frame,text="All Pick",variable=game_mode,value="AP",indicatoron=0).pack(side=LEFT)
Radiobutton(radio_frame,text="Captains Mode",variable=game_mode,value="CM",indicatoron=0).pack(side=LEFT)
Radiobutton(radio_frame,text="Random Draft",variable=game_mode,value="RD",indicatoron=0).pack(side=LEFT)
Radiobutton(radio_frame,text="Captains Draft",variable=game_mode,value="CD",indicatoron=0).pack(side=LEFT)

Checkbutton(radio_frame,text="First Pick",variable=pick_first).pack(side=LEFT)
Checkbutton(radio_frame,text="Ranked",variable=ranked).pack(side=LEFT)

# The Analyze Screenshot button, see OmniscienceMethods.py
def screenshot(*args):
    global master_pool, pick_button
    if game_mode.get()=="CD":
        master_pool=screenshot_CD()
        ban_button.config(state=NORMAL)
    elif game_mode.get()=="RD":
        master_pool=screenshot_RD()
    pick_button.config(state=NORMAL)
screenshot_button=Button(radio_frame,text="Analyze Screenshot",command=screenshot)
screenshot_button.pack(side=RIGHT)

# Goes to the release and information page.
Button(radio_frame,text="About",command=lambda:webbrowser.open("http://negative-energy.github.io/Omniscience/")).pack(side=RIGHT)

Label(scale_frame,text="Situationality of hero selection:").pack(side=LEFT)
situationality_scale = Scale(scale_frame,orient=HORIZONTAL, from_=50)
situationality_scale.set(70)
situationality_scale.pack(side=LEFT)
suggestability_scale = Scale(scale_frame,orient=HORIZONTAL)
suggestability_scale.set(50)
suggestability_scale.pack(side=RIGHT)
Label(scale_frame,text="Chance you will select the recommended hero:").pack(side=RIGHT)

Label(grid_frame,text="Your Picks").grid(row=0,column=0)
Label(grid_frame,text="Your Bans").grid(row=0,column=1)
Label(grid_frame,text="Their Picks").grid(row=0,column=3)
Label(grid_frame,text="Their Bans").grid(row=0,column=4)

# These are called to fix a hero name once a user has finished typing it
def validate_all():
    for row in range(1,6):
        for column in [0,1,3,4]:
            validate_entry(grid_frame.grid_slaves(row,column)[0])
def validate(event):
    validate_entry(event.widget)
def validate_entry(widget):
    if widget.get() == "": return
    hero_id=interpret_hero(widget.get())
    widget.delete(0,END)
    widget.insert(0,heroes[hero_id])

# Make the big grid of entry boxes for heroes
for column in [0,1,3,4]:
    for row in range(1,6):
        entry = Entry(grid_frame)
        entry.bind("<Return>",validate)
        entry.bind("<FocusOut>",validate)
        entry.grid(row=row,column=column)

# Make the big text that displays the recommendations
pick_box = Frame(grid_frame)
pick_text = Text(pick_box)
pick_scroll = Scrollbar(pick_box,command=pick_text.yview)
pick_text.config(yscrollcommand=pick_scroll.set)
pick_box.grid(row=7,column=0,columnspan=5)
pick_text.pack(side=LEFT)
pick_scroll.pack(side=RIGHT, fill=Y)

# The code behind the Picks and Bans buttons
# This generates and displays the list of hero recommendations
def refresh_picks():
    refresh("<")
def refresh_bans():
    refresh("{")
# The user sometimes want preliminary recommendations before the opponent has finished selecting.
# It will skip ahead to the first instance of first_char in the picking order string to get recommendations for the future.
def refresh(first_char):
    #feed settings data to the C code
    _omniscience.load_settings(1-situationality_scale.get()/100.,1-suggestability_scale.get()/100.)
    order=orders[game_mode.get()]
    # Unranked AP has no order. When suggestability is 0 minimax is not very useful, so skip it.

    # The FocusOut event fires *after* clicking the button for some reason.
    # We have to check the hero entry boxes here too.
    validate_all()

    allies=[]
    enemies=[]
    pool=list(master_pool)
    
    # Read in all the the hero entry boxes
    for row in range(1,6):
        for column in [0,1,3,4]:
            hero=grid_frame.grid_slaves(row,column)[0].get()
            if hero:
                hero = heroes.index(hero)
                if column==0: allies.append(hero)
                if column==3: enemies.append(hero)
                if hero in pool: pool.remove(hero)

    if (not ranked.get() and game_mode.get()=='AP') or suggestability_scale.get()==0:
        order="<"
    else:
        if not pick_first.get(): order=order.translate(switchsides_trans)
        (order,next_box)=get_next_in_order(order,grid_frame)
        order=order[order.index(first_char):]
        next_box.focus_set()

    # Iteratively increase the search depth until it starts taking too long
    length = 0
    start_time = time.clock()
    hero_quality = None
    while time.clock() < start_time+mode_search_min_times[game_mode.get()] and length < len(order):
        length += 1
        while length < len(order) and (order[length-1] == '{' or order[length-1]=='{'):
            length += 1
        # Pass the info to the C code and let it do the heavy lifting.
        # The C code uses a different numbering system so we have to translate it here.
        hero_quality=map(to_probability,_omniscience.analyze([hero_range.index(i) for i in pool],
                                                              [hero_range.index(i) for i in allies],
                                                              [hero_range.index(i) for i in enemies],order[:length]))
    hero_quality=[0 if i not in pool else hero_quality[hero_range.index(i)] for i in range(len(heroes))]

    # Format the data and display it
    order=sorted(pool,key=lambda id: hero_quality[id],reverse=True)
    pick_text.delete("0.0",END)
    rankrange=max(.000001,float(hero_quality[order[0]]-hero_quality[order[-1]]))
    width=55
    for i in range(len(order)):
        normalized=int((hero_quality[order[i]]-hero_quality[order[-1]])*2*width/rankrange-width)
        pick_text.insert(END,"{:<3} {:<20} {}\n".format(\
            i+1,\
            heroes[order[i]],\
            "="*normalized+" "*min(width-normalized,width+normalized)+"="*-normalized))

pick_button=Button(grid_frame,text="Picks",command=refresh_picks)
pick_button.grid(row=6,column=0)
ban_button=Button(grid_frame,text="Bans", command=refresh_bans)
ban_button.grid(row=6,column=1)

def clear_entries():
    for row in range(1,6):
        for column in [0,1,3,4]:
            grid_frame.grid_slaves(row,column)[0].delete(0,END)
Button(grid_frame,text="Clear All", command=clear_entries).grid(row=6,column=4)

# Reload data and send it to the C code whenever the mode is changed.
def game_mode_changed(*args):
    global master_pool
    master_pool=list(cmhero_range if game_mode.get().startswith("C") else hero_range)
    _omniscience.load_data([[to_odds(synergy(a,b,ranked.get())) for a in hero_range] for b in hero_range],\
                                [[to_odds(advantage(a,b,ranked.get())) for a in hero_range] for b in hero_range],\
                                [data['ranked' if ranked.get() and not game_mode.get()=="RD" else 'unranked'][game_mode.get()]['popularity'][a] for a in hero_range])
    ban_button.config(state=NORMAL if game_mode.get()=="CM" else DISABLED)
    if game_mode.get()=="AP" or game_mode.get()=="CM":
        screenshot_button.config(state=DISABLED)
        pick_button.config(state=NORMAL)
    else:
        screenshot_button.config(state=NORMAL)
        pick_button.config(state=DISABLED)
        
game_mode.trace("w",game_mode_changed)
ranked.trace("w",game_mode_changed)
game_mode.set("AP")

root.mainloop()