import urllib2
import string
import cPickle as pickle
import time
import msvcrt
import sys
import copy

nHeroes = 112
alpha = 5000. # number of games measured for a probability variable before it starts to "replace" old data

data={
    'next_seq': 1160000000, #6.83c update, end of year beast
    'ranked':{
        'synergy':[], 'advantage':[], 'synergydivisor':[], 'advantagedivisor':[],
        'AP':{'popularity':[0.]*nHeroes, 'popularitydivisor':0},
        'RD':{'popularity':[0.]*nHeroes, 'popularitydivisor':0},
        'CM':{'popularity':[0.]*nHeroes, 'popularitydivisor':0},
        'CD':{'popularity':[0.]*nHeroes, 'popularitydivisor':0}
    },
    'unranked':{
        'synergy':[], 'advantage':[], 'synergydivisor':[], 'advantagedivisor':[],
        'AP':{'popularity':[0.]*nHeroes, 'popularitydivisor':0},
        'RD':{'popularity':[0.]*nHeroes, 'popularitydivisor':0},
        'CM':{'popularity':[0.]*nHeroes, 'popularitydivisor':0},
        'CD':{'popularity':[0.]*nHeroes, 'popularitydivisor':0}
    }
}

try:
    data=pickle.load(open("data.p","rb"))
except:
    for lobbyType in ['ranked','unranked']:
        for j in range(nHeroes):
            data[lobbyType]['synergy'].append([1.]*nHeroes)
            data[lobbyType]['advantage'].append([1.]*nHeroes)
            data[lobbyType]['synergydivisor'].append([2]*nHeroes)
            data[lobbyType]['advantagedivisor'].append([2]*nHeroes)

#normalize data if alpha is lowered
for lobbyType in ['ranked','unranked']:
    for i in range(nHeroes):
        for  j in range(nHeroes):
            if data[lobbyType]['synergydivisor'][i][j]>alpha:
                data[lobbyType]['synergy'][i][j] = alpha * data[lobbyType]['synergy'][i][j] / data[lobbyType]['synergydivisor'][i][j]
                data[lobbyType]['synergydivisor'][i][j] = alpha
            if data[lobbyType]['advantagedivisor'][i][j]>alpha:
                data[lobbyType]['advantage'][i][j] = alpha * data[lobbyType]['advantage'][i][j] / data[lobbyType]['advantagedivisor'][i][j]
                data[lobbyType]['advantagedivisor'][i][j] = alpha
    for mode in ['AP','RD','CM','CD']:
        if data[lobbyType][mode]['popularitydivisor'] > alpha:
            for i in range(nHeroes):
                data[lobbyType][mode]['popularity'][i] = alpha * data[lobbyType][mode]['popularity'][i] / data[lobbyType][mode]['popularitydivisor']
            data[lobbyType][mode]['popularitydivisor'] = alpha

#api_key = raw_input("Enter API key: ")
api_key = open('apikey.txt').read().strip()
if '<' in api_key:
    print "Please enter your API key in the file apikey.txt"
    sys.exit(0)
apiurl='http://api.steampowered.com/IDOTA2Match_570/GetMatchHistoryBySequenceNum/v1?key='+api_key+'&matches_requested=100&start_at_match_seq_num='
page=None
stop=False
last_match_start_time=9999999999
radiant=range(5)
dire=range(5,10)
while not stop:
    if last_match_start_time < time.time()-86400:
        data['next_seq']+=50000
    start_get_time=time.clock()
    while not stop:
        print "Downloading "+str(data['next_seq'])+": "+time.strftime('%x %I:%M:%S %p',time.localtime(last_match_start_time))
        try:
            stop=msvcrt.kbhit()
            page=urllib2.urlopen(urllib2.Request(apiurl+str(data['next_seq'])))
        except:
            print "Error retrieving page: "+str(sys.exc_info()[0])
            pickle.dump(data,open("data.p","wb"))
            time.sleep(19) # found by trial and error
        else:
            break
    if stop:
        break

    hero_ids=[]
    radiant_win=True
    good_game=True
    backup=copy.deepcopy(data)
    lobbyType=0
    #print "Analyzing..."
    #try:
    for line in page:
        if line[4:-1]=='"radiant_win": true,':
            radiant_win=True
        elif line[4:-1]=='"radiant_win": false,':
            radiant_win=False
        elif line[4:21]=='"match_seq_num": ':
            data['next_seq']=int(line[21:-2])
        elif line[4:18]=='"lobby_type": ':
            lobbyType={'7':'ranked','0':'unranked'}.get(line[18:-2],'unknown')
        elif line[4:18]=='"start_time": ':
            last_match_start_time=int(line[18:-2])
        elif line[4:21]=='"human_players": ':
            if line[-4:-1]!='10,':
                good_game=False
        elif line[6:23]=='"leaver_status": ':
            if line[-4:-1]!=' 0,':
                good_game=False
        elif line[6:17]=='"hero_id": ':
            hero_ids.append(int(line[17:-2])-1)
        elif line[2:18]=='"statusDetail": ':
            print line[19:-2]
        elif line[4:17]=='"game_mode": ':
            mode={1:'AP', 2:'CM', 3:'RD', 16:'CD', 22:'AP'}.get(int(line[17:].rstrip(", \n")),None)
            if mode and good_game and lobbyType in data:
                if data[lobbyType][mode]['popularitydivisor']<alpha:
                    data[lobbyType][mode]['popularitydivisor']+=1
                else:
                    for i in range(nHeroes):
                        data[lobbyType][mode]['popularity'][i]*=1-1/alpha
                for i in range(10):
                    data[lobbyType][mode]['popularity'][hero_ids[i]]+=1
                for i in radiant:
                    for j in radiant:
                        if data[lobbyType]['synergydivisor'][hero_ids[i]][hero_ids[j]]<alpha:
                            data[lobbyType]['synergydivisor'][hero_ids[i]][hero_ids[j]]+=1
                        else:
                            data[lobbyType]['synergy'][hero_ids[i]][hero_ids[j]]*=1-1/alpha
                        if radiant_win:
                            data[lobbyType]['synergy'][hero_ids[i]][hero_ids[j]]+=1
                    for j in dire:
                        if data[lobbyType]['advantagedivisor'][hero_ids[i]][hero_ids[j]]<alpha:
                            data[lobbyType]['advantagedivisor'][hero_ids[i]][hero_ids[j]]+=1
                            data[lobbyType]['advantagedivisor'][hero_ids[j]][hero_ids[i]]+=1
                        else:
                            data[lobbyType]['advantage'][hero_ids[i]][hero_ids[j]]*=1-1/alpha
                            data[lobbyType]['advantage'][hero_ids[j]][hero_ids[i]]*=1-1/alpha
                        if radiant_win:
                            data[lobbyType]['advantage'][hero_ids[i]][hero_ids[j]]+=1
                        else:
                            data[lobbyType]['advantage'][hero_ids[j]][hero_ids[i]]+=1
                for i in dire:
                    for j in dire:
                        if data[lobbyType]['synergydivisor'][hero_ids[i]][hero_ids[j]]<alpha:
                            data[lobbyType]['synergydivisor'][hero_ids[i]][hero_ids[j]]+=1
                        else:
                            data[lobbyType]['synergy'][hero_ids[i]][hero_ids[j]]*=1-1/alpha
                        if not radiant_win:
                            data[lobbyType]['synergy'][hero_ids[i]][hero_ids[j]]+=1
            good_game=True
            hero_ids=[]
    #except:
    #    print "Error while reading: "+str(sys.exc_info()[0])
    #    data=backup
    time.sleep(max(0,1 + start_get_time - time.clock()))
    stop=msvcrt.kbhit()

pickle.dump(data,open("data.p","wb"))

#raw_input()