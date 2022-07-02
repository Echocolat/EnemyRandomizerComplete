Breath of the Wild Enemy Randomizer v2 by Echocolat 
Big thanks to ArchLeaders for his help and MintLightning for cleaning up the scripts, some help with tweaking, and the arrangement into one file.

What do you need :
	1. BCML (the latest version you have the better)
	2. Python 3.8+ after installing the module oead (pip install oead)
	3. A legally obtained copy of Breath of the Wild v1.5.0 with DLC

How to use :
	If you want to randomize Hyrule enemies:
		1. Go into WhereYourBotWDLCIs\content\0010\Map\MainField and select all the X-Y folders.
		2. Copy-paste them into Enemy Randomizer v2\content\Map\MainField
	If you want to randomize Trials of the Sword enemies:
		1. Go into WhereYourBotWDLCIs\content\0010\Map\AocField and select A-1, B-1, A-2, B-2, A-3 and B-3 folders.
		2. Copy-paste them into Enemy Randomizer v2\aoc\0010\Map\AocField
	If you want to randomize Non-DLC shrines enemies:
		1. Go into WhereYourBaseBotWIs\content\Pack and select all the DungeonXXX packs.
		2. Copy-paste them into Enemy Randomizer v2\content\Pack
	If you want to randomize DLC shrines enemies:
		1. Go into WhereYourBotWDLCIs\content\0010\Pack and select all the DungeonXXX packs.
		2. Copy-paste them into Enemy Randomizer v2\aoc\0010\Pack
	If you want to randomize Divine Beasts enemies:
		1. Go into WhereYourBotWDLCIs\content\0010\Pack and select FinalTrial.pack and all the Remains[element] packs.
		2. Copy-paste them into Enemy Randomizer v2\aoc\0010\Pack
	Then, launch Enemy_Randomizer.py and select your options. 
	If you want the enemies to not respawn each time you load a save, you have to copy WhereYourUpdateBotWIs\content\Pack\Bootup.pack and paste it inside Enemy Randomizer v2\content\Pack, 
	install the package botw_flag_util, and use the command:
		botw_flag_util generate [path to the mod's root] -r 1 1 -b
	Use BCML to install the rules.txt file inside the folder "Enemy Randomizer v2". 
	Finally, take the output (both aoc and content folders) and copy-paste them to a new folder in Cemu/graphicPacks, along with rules.txt.
	Activate the mod (if you're using Chaos mode, it is strongly recommanded to use the Extended Memory community graphic pack) and enjoy !!!
	
If you need any help, because you don't know how to make the mod working for example, don't hesitate to contact me (@Echocolat#9988 on Discord) 
or to put a comment on the GameBanana page of the mod.