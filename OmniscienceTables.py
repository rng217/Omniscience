# Copyright 2014 Daniel Wilson

import zipfile
import cPickle as pickle
data=pickle.load(zipfile.ZipFile("data.zip").open("data.p"))

orders={"AP":"<", "CM":"{}{}<>><{}{}><><}{><", "CD":"{}{}{}<>><<>><<>", "RD":"<>><<>><<>"}
modeSearchDepths={"CM":3,"RD":4,"CD":4}

import string
switchsides_trans = string.maketrans("{}<>","}{><")

heroRange=range(23)+range(24,104)+range(105,107)+range(108,110)
cmHeroRange=range(23)+range(24,60)+range(61,104)+[105]

heroes=["Anti-Mage","Axe","Bane","Bloodseeker","Crystal Maiden","Drow Ranger","Earthshaker","Juggernaut","Mirana",
        "Morphling","Shadow Fiend","Phantom Lancer","Puck","Pudge","Razor","Sand King","Storm Spirit","Sven","Tiny",
        "Vengeful Spirit","Windranger","Zeus","Kunkka","???","Lina","Lion","Shadow Shaman","Slardar","Tidehunter",
        "Witch Doctor","Lich","Riki","Enigma","Tinker","Sniper","Necrophos","Warlock","Beastmaster","Queen of Pain",
        "Venomancer","Faceless Void","Wraith King","Death Prophet","Phantom Assassin","Pugna","Templar Assassin",
        "Viper","Luna","Dragon Knight","Dazzle","Clockwerk","Leshrac","Nature's Prophet","Lifestealer","Dark Seer",
        "Clinkz","Omniknight","Enchantress","Huskar","Night Stalker","Broodmother","Bounty Hunter","Weaver","Jakiro",
        "Batrider","Chen","Spectre","Ancient Apparition","Doom","Ursa","Spirit Breaker","Gyrocopter","Alchemist",
        "Invoker","Silencer","Outworld Devourer","Lycanthrope","Brewmaster","Shadow Demon","Lone Druid","Chaos Knight",
        "Meepo","Treant Protector","Ogre Magi","Undying","Rubick","Disruptor","Nyx Assassin","Naga Siren",
        "Keeper of the Light","Io","Visage","Slark","Medusa","Troll Warlord","Centaur Warrunner","Magnus","Timbersaw",
        "Bristleback","Tusk","Skywrath Mage","Abaddon","Elder Titan","Legion Commander","Techies","Ember Spirit",
        "Earth Spirit","Abyssal Underlord","Terrorblade","Phoenix"]

abbreviations={
'ab':102,'abaddon':102,
'al':73,'alch':73,'alchemist':73,
'aa':68,'ancient apparition':68,
'am':1,'anti-mage':1,
'axe':2,
'bane':3,
'bat':65,'br':65,'batrider':65,
'bb':99,'bristleback':99,
'bm':38,'beast':38,'beastmaster':38,
'bs':4,'bloodseeker':4,
'bh':62,'bounty':62,'bounty hunter':62,
'brew':78,'brewmaster':78,
'brood':61,'broodmother':61,
'cw':96,'centaur':96,'warrunner':96,'centaur warrunner':96,'centaur warchief':96,'warchief':96,
'ck':81,'chaos':81,'chaos knight':81,
'ch':66,'chen':66,
'clinkz':56,
'clock':51,'clockwerk':51,
'cm':5,'crystal maiden':5,
'ds':55,'seer':55,'dark seer':55,
'daz':50,'dazzle':50,
'dp':43,'death prophet':43,
'dis':87,'disruptor':87,
'doom':69,'db':69,'doom bringer':69,
'dk':49,'dragon':49,'dragon knight':49,
'drow':6,'dr':6,'drow ranger':6,
'es':7,'shaker':7,'earthshaker':7,
'ench':58,'enchantress':58,
'?':33,'nig':33,'enigma':33,
'fv':41,'void':41,'faceless void':41,
'gc':72,'gyro':72,'gyrocopter':72,
'husk':59,'huskar':59,
'inv':74,'invoker':74,
'jak':64,'jakiro':64,
'jug':8,'juggs':8,'juggernaut':8,
'kotl':90,'keeper':90,'keeper of the light':90,
'kunkka':23,
'lesh':52,'leshrac':52,
'ls':54,'lifestealer':54,
'ld':80,'lone druid':80,
'lycan':77,'lycanthrope':77,
'lina':25,
'lich':31,
'lion':26,
'luna':48,
'mag':97,'magnataur':97,'magnus':97,
'mirana':9,
'morph':10,'morphling':10,
'meepo':82,
'ns':60,'night stalker':60,'stalker':60,'night':60,
'naga':89,'naga siren':89,'siren':89,
'np':53,'nature\'s prophet':53,'profit':53,
'necro':36,'nl':36,'necrolyte':36,'necrophos':36,
'nyx':88,'na':88,'nyx assassin':88,
'ogre':84,'om':84,'magi':84,'ogre magi':84,
'omni':57,'ok':57,'omniknight':57,
'od':76,'outworld destroyer':76,'outworld demolisher':76,'outworld devourer':76,'obsidian destroyer':76,
'pa':44,'phantom assassin':44,
'pl':12,'lancer':12,'phantom lancer':12,
'pudge':14,
'puck':13,
'pugna':45,
'qop':39,'queen':39,'queen of pain':39,
'razor':15,
'rubick':86,
'riki':32,
'sk':16,'sand':16,'sand king':16,
'sd':79,'shadow demon':79,'demon':79,
'sf':11,'fiend':11,'shadow fiend':11,'fiend':11,
'ss':27,'shaman':27,'shadow shaman':27,
'shh':75,'silencer':75,
'wk':42,'wraith':42,'wraith king':42,'skeleton':42,'skeleton king':42,
'sm':101,'swm':101,'skywrath':101,'sky':101,'skywrath mage':101,
'sb':71,'spirit breaker':71,
'slar':28,'slardar':28,
'storm':17,'storm spirit':17,
'sven':18,
'sniper':35,
'spectre':67,
'slark':93,
'ta':46,'templar':46,'templar assassin':46,
'tide':29,'tidehunter':29,
'ts':98,'timber':98,'timbersaw':98,
'tp':83,'treant':83,'treant protector':83,'protector':83,
'tiny':19,
'tinker':34,
'ud':85,'dirge':85,'undying':85,
'ursa':70,
'vs':20,'venge':20,'vengeful spirit':20,
'veno':40,'vm':40,'venomancer':40,
'vis':92,'visage':92,
'viper':47,
'wl':37,'warlock':37,
'weaver':63,
'wr':21,'wind':21,'windrunner':21,'windranger':21,
'wd':30,'witch':30,'doctor':30,'witch doctor':30,
'io':91,'wisp':91,
'zeus':22,
'med':94,'medusa':94,
'tw':95,'troll':95,'warlord':95,'troll warlord':95,
'tusk':100,'tuskarr':100,
'et':103,'elder titan':103,'titan':103,'elder':103,
'xin':106,'ember':106,'ember spirit':106,
'kaolin':107,'earth':107,'earth spirit':107,
'tresdin':104,'lc':104,'legion':104,'commander':104,'legion commander':104,
'tb':109,'terrorblade':109,'terror':109,
'phoenix':110}

heroGroupTable=[[6, 17, 18, 22, 37, 48, 50, 56, 58, 72, 77, 82, 90, 95, 97, 98, 99, 102, 103, 106, 109],
                [1, 13, 15, 27, 28, 41, 53, 59, 68, 70, 76, 80, 84, 96, 101],
                [0, 5, 7, 8, 9, 11, 19, 31, 34, 45, 47, 61, 69, 71, 79, 88, 94, 105],
                [3, 10, 14, 39, 40, 43, 46, 55, 60, 62, 66, 81, 87, 92, 93, 108],
                [4, 12, 16, 20, 21, 24, 26, 33, 52, 57, 63, 65, 74, 83, 85, 86, 89, 100],
                [2, 30, 25, 29, 32, 35, 36, 38, 42, 44, 49, 51, 54, 64, 67, 73, 75, 78, 91]]

heroTypes={ #unused and out of date
"lane support":
["Crystal Maiden","Dazzle","Earthshaker","Io","Jakiro","Lich","Lion","Omniknight",
"Treant Protector","Vengeful Spirit","Warlock"],

"carry":
["Alchemist","Anti-Mage","Bloodseeker","Bounty Hunter","Brewmaster","Broodmother","Chaos Knight",
"Clinkz","Doom","Dragon Knight","Drow Ranger","Faceless Void","Huskar","Invoker","Juggernaut",
"Kunkka","Lifestealer","Lone Druid","Luna","Lycanthrope","Magnus","Medusa","Meepo","Mirana",
"Morphling","Naga Siren","Nature's Prophet","Necrolyte","Outworld Devourer","Phantom Assassin",
"Phantom Lancer","Queen of Pain","Razor","Riki","Shadow Fiend","Silencer","Wraith King",
"Slardar","Sniper","Spectre","Spirit Breaker","Storm Spirit","Sven","Templar Assassin",
"Troll Warlord","Ursa","Viper","Weaver","Ember Spirit"],

"disabler":
["Alchemist","Ancient Apparition","Axe","Bane","Batrider","Beastmaster","Bristleback",
"Centaur Warrunner","Chaos Knight","Crystal Maiden","Disruptor","Dragon Knight","Earthshaker",
"Enigma","Faceless Void","Gyrocopter","Jakiro","Kunkka","Leshrac","Lina","Lion","Magnus","Meepo",
"Mirana","Naga Siren","Nyx Assassin","Ogre Magi","Puck","Pudge","Rubick","Sand King",
"Shadow Demon","Shadow Shaman","Wraith King","Slardar","Spirit Breaker","Storm Spirit","Sven",
"Tidehunter","Tiny","Treant Protector","Undying","Vengeful Spirit","Visage","Warlock","Windrunner",
"Witch Doctor","Ember Spirit"],

"ganker":
["Alchemist","Batrider","Beastmaster","Bloodseeker","Bounty Hunter","Chaos Knight","Clinkz",
"Enchantress","Gyrocopter","Kunkka","Lycanthrope","Mirana","Nature's Prophet","Night Stalker",
"Nyx Assassin","Ogre Magi","Phantom Assassin","Pudge","Queen of Pain","Riki","Shadow Demon",
"Spirit Breaker","Storm Spirit","Timbersaw","Tinker","Tiny","Viper","Slark"],

"nuker":
["Bane","Batrider","Bounty Hunter","Crystal Maiden","Dark Seer","Death Prophet","Disruptor","Doom",
"Gyrocopter","Invoker","Io","Jakiro","Leshrac","Lich","Lina","Lion","Luna","Magnus","Mirana",
"Morphling","Nyx Assassin","Ogre Magi","Puck","Pugna","Queen of Pain","Razor","Sand King",
"Shadow Demon","Shadow Fiend","Shadow Shaman","Skywrath Mage","Tinker","Tiny","Venomancer",
"Visage","Windrunner","Zeus","Ember Spirit"],

"initiator":
["Axe","Batrider","Beastmaster","Brewmaster","Bristleback","Centaur Warrunner","Clockwerk",
"Dark Seer","Disruptor","Earthshaker","Elder Titan","Enigma","Faceless Void","Gyrocopter",
"Huskar","Invoker","Kunkka","Magnus","Meepo","Morphling","Night Stalker","Puck","Sand King",
"Silencer","Slardar","Spirit Breaker","Storm Spirit","Sven","Tidehunter","Timbersaw","Tiny",
"Treant Protector","Tusk","Undying","Vengeful Spirit","Venomancer","Warlock","Earth Spirit"],

"Jungler":
["Axe","Bloodseeker","Chen","Enchantress","Enigma","Lifestealer","Lone Druid","Lycanthrope",
"Nature's Prophet","Ursa"],

"pusher":
["Brewmaster","Broodmother","Chaos Knight","Chen","Death Prophet","Dragon Knight","Enchantress",
"Enigma","Jakiro","Juggernaut","Keeper of the Light","Leshrac","Lone Druid","Lycanthrope",
"Naga Siren","Nature's Prophet","Phantom Lancer","Pugna","Rubick","Shadow Shaman","Tinker",
"Undying","Venomancer"],

"roamer":
["Ancient Apparition","Bane","Clockwerk","Crystal Maiden","Dark Seer","Disruptor","Earthshaker",
"Jakiro","Leshrac","Lich","Lina","Lion","Puck","Sand King","Shadow Shaman","Slardar","Sven",
"Tidehunter","Vengeful Spirit","Venomancer","Windrunner","Witch Doctor","Zeus"],

"durable":
["Alchemist","Axe","Beastmaster","Brewmaster","Bristleback","Centaur Warrunner","Chaos Knight",
"Clockwerk","Death Prophet","Doom","Dragon Knight","Elder Titan","Enchantress","Huskar","Kunkka",
"Lifestealer","Lone Druid","Lycanthrope","Necrolyte","Night Stalker","Ogre Magi","Omniknight",
"Pudge","Razor","Wraith King","Slardar","Spectre","Spirit Breaker","Tidehunter","Timbersaw",
"Tiny","Treant Protector","Tusk","Undying","Ursa","Viper","Visage","Ember Spirit"],

"escape":
["Anti-Mage","Batrider","Bounty Hunter","Broodmother","Clinkz","Dark Seer","Faceless Void",
"Invoker","Lifestealer","Mirana","Morphling","Naga Siren","Nature's Prophet","Phantom Assassin",
"Phantom Lancer","Puck","Queen of Pain","Riki","Slark","Storm Spirit","Templar Assassin","Weaver",
"Windrunner"],

#Semi-Carry: See Ganker

"support":
["Ancient Apparition","Bane","Chen","Crystal Maiden","Dazzle","Disruptor","Earthshaker",
"Enchantress","Io","Leshrac","Lich","Lina","Lion","Necrolyte","Omniknight","Pugna","Shadow Demon",
"Shadow Shaman","Silencer","Skywrath Mage","Sven","Tidehunter","Vengeful Spirit","Venomancer",
"Warlock","Windrunner","Witch Doctor","Zeus"]
}