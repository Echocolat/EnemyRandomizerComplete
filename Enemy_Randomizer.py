from distutils.command.config import config
from distutils.spawn import spawn
import random
import oead
import os
from pathlib import Path
from random import randint
false = False
true = True

# OPTIONS #
chaos = False
randomWeapons = True
hyrule = True
swordTrial = True
shrines = True
beasts = True
dlcshrines = True
bossProb = 23

if input("    /\\                          /\\\n   /__\\     Welcome to the     /__\\\n  /\\  /\\    Botw Enemizer!    /\\  /\\\n /__\\/__\\                    /__\\/__\\\n\nPLEASE look at the README file before continuing!\n\nTo customize settings, type 'custom'. To use default setting, just press Enter: ") == 'custom':
    print("\nEnter 'y' or 'n' for the following options:\n")
    print("\tDo you want randomized enemies in...")
    hyrule = input('\t\tHyrule (MainField)? ') == 'y'
    shrines = input('\t\tShrines? ') == 'y'
    beasts = input('\t\tDivine Beasts? ') == 'y'
    swordTrial = input('\t\tTrials of the Sword? ') == 'y'
    dlcshrines = input('\t\tDLC shrines? ') == 'y'
    randomWeapons = input('\n\tDo you want to randomize enemy weapons? ') == 'y'
    chaos = input('\n\tIn Chaos Mode, all enemies have an equal chance of spawning (NOT RECOMMENDED)\n\t\tActivate Chaos mode? ') == 'y'
    if not chaos:
        bossProb = input('\n\tChoose probability of mini-bosses (chance = 1/probability)\n\t\tPress Enter to use default value (23), or type an integer: ')

    try:
        bossProb = int(bossProb)
    except:
        bossProb = 23

# OPTIONS #

objectsDetected = {}

hasIchigeki = {
    550632616,
    922489664,
    1045312616,
    1124191658,
    1532782160,
    1609969362,
    1666280366,
    2455133014,
    2464348397,
    2596422984,
    2668152795,
    3220042110,
    3448775721,
    3503668076,
    3602597398,
    3660855167,
    4293673867,
    80844072,
    605669213,
    686607516,
    935714617,
    1289247628,
    1342546971,
    1896830638,
    2175453082,
    2336155376,
    2374098089,
    2985405034,
    3131589968,
    3284731961,
    3492843870,
    3499286924,
    3516037048,
    3667523954,
    3720177370,
    4101766333,
    1318247557,
    1338072565,
    2431854881,
    2787670927,
    2897381425,
    3323374617,
    3362121203,
    3675361416,
    3973316133,
    4201866831,
    392220592,
    570137918,
    706821037,
    855470103,
    899133649,
    980184898,
    1137377869,
    1473719602,
    1812966703,
    1872971899,
    2109811747,
    2245273807,
    2542308349,
    2553054293,
    2699982531,
    2779549592,
    2788519301,
    2959864704,
    3002321673,
    3010425640,
    3077603964,
    3258908224,
    3308273825,
    3350822698,
    3520836035,
    3573940731,
    3742246923,
    3837491176,
    3869978581,
    4046668124,
    4131598004,
    396262437,
    3722716533,
    641591931,
    1057732685,
    1289245973,
    1831034516,
    1854979353,
    2373891178,
    2477880917,
    3176024268,
    3498361990,
    3791177034,
    3884172536,
    4095109193,
    4285959998,
    210614366,
    148282207,
    221775837,
    458827803,
    695342366
}

enemiesGenerated = {
    "Bokoblin": 0,
    "Moriblin": 0,
    "Lizalfos": 0,
    "Lynel": 0,
    "Keese": 0,
    "Chuchu": 0,
    "Golem_Little": 0,
    "Guardian_Mini": 0,
    "Guardian": 0,
    "Octarock": 0,
    "Wizzrobe": 0,
    "Giant": 0,
    "Golem": 0,
    "Sandworm": 0
}

weights = {
    "Enemy_Assassin_Shooter_Azito_Junior": 2, # 3 Yiga
    "Enemy_Assassin_Azito_Middle_DLC2":  1,
    "Enemy_Bokoblin_Bone_Junior_AllDay": 3, # 25 Bokoblin
    "Enemy_Bokoblin_Junior":        7,
    "Enemy_Bokoblin_Middle":        6,
    "Enemy_Bokoblin_Senior":        5,
    "Enemy_Bokoblin_Dark":          4,
    "Enemy_Bokoblin_Gold":          0,
    "Enemy_Chuchu_Electric_Senior": 4, # 12 Chuchu
    "Enemy_Chuchu_Ice_Senior":      4,
    "Enemy_Chuchu_Fire_Senior":     4,
    "Enemy_Chuchu_Senior":          4,
    "Enemy_Golem_Little_Fire":      2, # 8 Stone Boi
    "Enemy_Golem_Little_Ice":       2,
    "Enemy_Golem_Little":           4,
    "Enemy_Guardian_A":             1, # 4 Guardian
    "Enemy_Guardian_B":             1,
    "Enemy_Guardian_C":             1,
    "Enemy_Guardian_A_Fixed_Moss":  1,
    "Enemy_Guardian_Mini_Baby":     3, # 8 Mini-Guardian
    "Enemy_Guardian_Mini_Junior":   2,
    "Enemy_Guardian_Mini_Middle":   2,
    "Enemy_Guardian_Mini_Senior":   1,
    "Enemy_Keese_AllDay":           3, # 13 Keese
    "Enemy_Keese_Electric_AllDay":  3,
    "Enemy_Keese_Fire_AllDay":      3,
    "Enemy_Keese_Ice_AllDay":       3,
    "Enemy_Keese_Swarm_AllDay":     1,
    "Enemy_Lizalfos_Bone_Junior":   3, # 19 Lizalfos
    "Enemy_Lizalfos_Junior":        5,
    "Enemy_Lizalfos_Middle":        4,
    "Enemy_Lizalfos_Senior":        4,
    "Enemy_Lizalfos_Dark":          3,
    "Enemy_Lizalfos_Gold":          0,
    "Enemy_Lizalfos_Electric":      1, # 3 Elemental Lizalfos
    "Enemy_Lizalfos_Fire":          1,
    "Enemy_Lizalfos_Ice":           1,
    "Enemy_Lynel_Junior":           1, # 4 Lynel
    "Enemy_Lynel_Middle":           1,
    "Enemy_Lynel_Senior":           1,
    "Enemy_Lynel_Dark":             1,
    "Enemy_Lynel_Gold":             0,
    "Enemy_Moriblin_Bone_Junior":   3, # 21 Moblin
    "Enemy_Moriblin_Junior":        6,
    "Enemy_Moriblin_Middle":        5,
    "Enemy_Moriblin_Senior":        4,
    "Enemy_Moriblin_Dark":          3,
    "Enemy_Moriblin_Gold":          0,
    "Enemy_Octarock":               2, # 10 Octorock
    "Enemy_Octarock_Desert":        2,
    "Enemy_Octarock_Forest":        2,
    "Enemy_Octarock_Snow":          2,
    "Enemy_Octarock_Stone":         2,
    "Enemy_Wizzrobe_Electric":      1, # 6 Wizrobe
    "Enemy_Wizzrobe_Electric_Senior": 1,
    "Enemy_Wizzrobe_Fire":          1,
    "Enemy_Wizzrobe_Fire_Senior":   1,
    "Enemy_Wizzrobe_Ice":           1,
    "Enemy_Wizzrobe_Ice_Senior":    1}

weightsBoss = {
    "Enemy_Giant_Bone_AllDay":2, # Hinox: 13
    "Enemy_Giant_Junior":5,
    "Enemy_Giant_Middle":4,
    "Enemy_Giant_Senior":2,
    "Enemy_Golem_Fire":2,       # Talus: 14
    "Enemy_Golem_Fire_R":1,
    "Enemy_Golem_Ice":2,
    "Enemy_Golem_Junior":4,
    "Enemy_Golem_Middle":3,
    "Enemy_Golem_Senior":2,
    "Enemy_Sandworm":6,         # Molduga: 7
    "Enemy_SandwormR":1}

weightsArrow = {
    "NormalArrow":3,
    "FireArrow":2,
    "IceArrow":2,
    "ElectricArrow":2,
    "BombArrow":2,
    "AncientArrow":1}

spawnableEnemy=[
    ("Enemy_Assassin_Shooter_Azito_Junior",{'ArrowName': 'NormalArrow', 'DropTable': 'Normal', 'EquipItem1': 'Weapon_Bow_040', 'EquipItem2': 'Default', 'EquipItem3': 'Default', 'EquipItem4': 'Default', 'IsNearCreate': false, 'LevelSensorMode': 1, 'NearCreateAppearID': 0, 'SharpWeaponJudgeType': 1, 'TerritoryArea': 0.0}),
    ("Enemy_Assassin_Azito_Middle_DLC2",{'ArrowName': 'NormalArrow', 'DropTable': 'Normal', 'EquipItem1': 'Weapon_Lsword_074', 'EquipItem2': 'Default', 'EquipItem3': 'Weapon_Sword_043', 'EquipItem4': 'Default', 'IsNearCreate': false, 'IsWatchKeeping': false, 'LevelSensorMode': 1, 'NearCreateAppearID': 0, 'RotAngle': 0.0, 'SharpWeaponJudgeType': 1, 'TerritoryArea': 0.0, 'WaitTime': '1.0'}),
    ("Enemy_Bokoblin_Bone_Junior_AllDay",{'ArrowName': 'NormalArrow', 'DropTable': 'Normal', 'EquipItem1': 'Weapon_Sword_006','EquipItem2': 'Default', 'EquipItem3': 'Default', 'EquipItem4': 'Default', 'FortressEatPer': -1,'IsNearCreate': false, 'IsWatchKeeping': true, 'LevelSensorMode': 1, 'RotAngle': 0.0,'SharpWeaponJudgeType': 1, 'TerritoryArea': 0.0, 'WaitTime': 1.0}),
    ("Enemy_Bokoblin_Junior",{'ArrowName': 'NormalArrow', 'DropTable': 'Normal', 'EquipItem1': 'Weapon_Sword_004','EquipItem2': 'Default', 'EquipItem3': 'Default', 'EquipItem4': 'Default', 'FortressEatPer': -1,'IsNearCreate': false, 'IsWatchKeeping': true, 'LevelSensorMode': 1, 'RotAngle': 0.0,'SharpWeaponJudgeType': 1, 'TerritoryArea': 0.0, 'WaitTime': 1.0}),
    ("Enemy_Bokoblin_Middle",{'ArrowName': 'NormalArrow', 'DropTable': 'Normal', 'EquipItem1': 'Weapon_Sword_005','EquipItem2': 'Default', 'EquipItem3': 'Default', 'EquipItem4': 'Default', 'FortressEatPer': -1,'IsNearCreate': false, 'IsWatchKeeping': true, 'LevelSensorMode': 1, 'RotAngle': 0.0,'SharpWeaponJudgeType': 1, 'TerritoryArea': 0.0, 'WaitTime': 1.0}),
    ("Enemy_Bokoblin_Senior",{'ArrowName': 'NormalArrow', 'DropTable': 'Normal', 'EquipItem1': 'Weapon_Sword_006','EquipItem2': 'Default', 'EquipItem3': 'Default', 'EquipItem4': 'Default', 'FortressEatPer': -1,'IsNearCreate': false, 'IsWatchKeeping': true, 'LevelSensorMode': 1, 'RotAngle': 0.0,'SharpWeaponJudgeType': 1, 'TerritoryArea': 0.0, 'WaitTime': 1.0}),
    ("Enemy_Bokoblin_Dark",{'ArrowName': 'NormalArrow', 'DropTable': 'Normal', 'EquipItem1': 'Weapon_Sword_006','EquipItem2': 'Default', 'EquipItem3': 'Default', 'EquipItem4': 'Default', 'FortressEatPer': -1,'IsNearCreate': false, 'IsWatchKeeping': true, 'LevelSensorMode': 1, 'RotAngle': 0.0,'SharpWeaponJudgeType': 1, 'TerritoryArea': 0.0, 'WaitTime': 1.0}),
    ("Enemy_Bokoblin_Gold",{'ArrowName': 'NormalArrow', 'DropTable': 'Normal', 'EquipItem1': 'Weapon_Sword_006','EquipItem2': 'Default', 'EquipItem3': 'Default', 'EquipItem4': 'Default', 'FortressEatPer': -1,'IsNearCreate': false, 'IsWatchKeeping': true, 'LevelSensorMode': 1, 'RotAngle': 0.0,'SharpWeaponJudgeType': 1, 'TerritoryArea': 0.0, 'WaitTime': 1.0}),
    ("Enemy_Chuchu_Electric_Senior",{'ArrowName': 'NormalArrow', 'DropTable': 'Normal', 'EquipItem1': 'Default', 'EquipItem2': 'Default', 'EquipItem3': 'Default', 'EquipItem4': 'Default', 'IsDrop': false, 'IsNearCreate': false, 'IsWatchKeeping': false, 'LevelSensorMode': 1, 'NearCreateAppearID': 0, 'NearCreateAppearType': 0, 'RotAngle': 0.0, 'SharpWeaponJudgeType': 1, 'TerritoryArea': 0.0, 'WaitTime': 1.0}),
    ("Enemy_Chuchu_Ice_Senior",{'ArrowName': 'NormalArrow', 'DropTable': 'Normal', 'EquipItem1': 'Default', 'EquipItem2': 'Default', 'EquipItem3': 'Default', 'EquipItem4': 'Default', 'IsDrop': false, 'IsNearCreate': false, 'IsWatchKeeping': false, 'LevelSensorMode': 1, 'NearCreateAppearID': 0, 'NearCreateAppearType': 0, 'RotAngle': 0.0, 'SharpWeaponJudgeType': 1, 'TerritoryArea': 0.0, 'WaitTime': 1.0}),
    ("Enemy_Chuchu_Fire_Senior",{'ArrowName': 'NormalArrow', 'DropTable': 'Normal', 'EquipItem1': 'Default', 'EquipItem2': 'Default', 'EquipItem3': 'Default', 'EquipItem4': 'Default', 'IsDrop': false, 'IsNearCreate': false, 'IsWatchKeeping': false, 'LevelSensorMode': 1, 'NearCreateAppearID': 0, 'NearCreateAppearType': 0, 'RotAngle': 0.0, 'SharpWeaponJudgeType': 1, 'TerritoryArea': 0.0, 'WaitTime': 1.0}),
    ("Enemy_Chuchu_Senior",{'ArrowName': 'NormalArrow', 'DropTable': 'Normal', 'EquipItem1': 'Default', 'EquipItem2': 'Default', 'EquipItem3': 'Default', 'EquipItem4': 'Default', 'IsDrop': false, 'IsNearCreate': false, 'IsWatchKeeping': false, 'LevelSensorMode': 1, 'NearCreateAppearID': 0, 'NearCreateAppearType': 0, 'RotAngle': 0.0, 'SharpWeaponJudgeType': 1, 'TerritoryArea': 0.0, 'WaitTime': 1.0}),
    ("Enemy_Golem_Little_Fire",{"ArrowName": "NormalArrow","DropTable": "Normal","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","GolemSleepType": "SleepForward_A","GolemWeakPointLocation": "Point_A","IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Golem_Little_Ice",{"ArrowName": "NormalArrow","DropTable": "Normal","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","GolemSleepType": "SleepForward_A","GolemWeakPointLocation": "Point_A","IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Golem_Little",{"ArrowName": "NormalArrow","DropTable": "Normal","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","GolemSleepType": "SleepForward_A","GolemWeakPointLocation": "Point_A","IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Guardian_A",{"ChaseRange": 200,"DropTable": "Normal","GuardianLegType0": "Guardian_A_Leg","GuardianLegType1": "Guardian_A_Leg","GuardianLegType2": "Guardian_A_Leg","GuardianLegType3": "Guardian_A_Leg","GuardianLegType4": "Guardian_A_Leg","GuardianLegType5": "Guardian_A_Leg","IsSuspended": true,"SharpWeaponJudgeType": 1}),
    ("Enemy_Guardian_B",{"ChaseRange": 200,"DropTable": "Normal","GuardianLegType0": "Guardian_A_Leg","GuardianLegType1": "Guardian_A_Leg","GuardianLegType2": "Guardian_A_Leg","GuardianLegType3": "Guardian_A_Leg","GuardianLegType4": "Guardian_A_Leg","GuardianLegType5": "Guardian_A_Leg","IsSuspended": false,"SharpWeaponJudgeType": 0}),
    ("Enemy_Guardian_C",{"ChaseRange": 200,"DropTable": "Normal","GuardianLegType0": "Guardian_A_Leg","GuardianLegType1": "Guardian_A_Leg","GuardianLegType2": "Guardian_A_Leg","GuardianLegType3": "Guardian_A_Leg","GuardianLegType4": "Guardian_A_Leg","GuardianLegType5": "Guardian_A_Leg","IsSuspended": false,"SharpWeaponJudgeType": 1}),
    ("Enemy_Guardian_A_Fixed_Moss",{"ChaseRange": 200,"DropTable": "Normal","GuardianLegType0": "Guardian_A_Leg","GuardianLegType1": "Guardian_A_Leg","GuardianLegType2": "Guardian_A_Leg","GuardianLegType3": "Guardian_A_Leg","GuardianLegType4": "Guardian_A_Leg","GuardianLegType5": "Guardian_A_Leg","IsSuspended": false,"SharpWeaponJudgeType": 0}),
    ("Enemy_Guardian_Mini_Baby",{"ArrowName": "NormalArrow","BeamRange": 0,"DropTable": "Normal","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","IsAnnihilateDungeonEnemy": false,"IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Guardian_Mini_Junior",{"ArrowName": "NormalArrow","BeamRange": 0,"DropTable": "Normal","EquipItem1": "Weapon_Lsword_013","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","IsAnnihilateDungeonEnemy": false,"IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Guardian_Mini_Middle",{"ArrowName": "NormalArrow","BeamRange": 0,"DropTable": "Normal","EquipItem1": "Weapon_Sword_014","EquipItem2": "Weapon_Lsword_014","EquipItem3": "Default","EquipItem4": "Default","IsAnnihilateDungeonEnemy": false,"IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 1,"TerritoryArea": 0}),
    ("Enemy_Guardian_Mini_Senior",{"ArrowName": "NormalArrow","BeamRange": 0,"DropTable": "Normal","EquipItem1": "Weapon_Sword_015","EquipItem2": "Weapon_Lsword_015","EquipItem3": "Weapon_Spear_015","EquipItem4": "Default","IsAnnihilateDungeonEnemy": false,"IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 1,"TerritoryArea": 0}),
    ("Enemy_Keese_AllDay",{"ArrowName": "NormalArrow","DropTable": "Normal","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","IsCreateOnFace": true,"IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 1,"TerritoryArea": 0}),
    ("Enemy_Keese_Electric_AllDay",{"ArrowName": "NormalArrow","DropTable": "Normal","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","IsCreateOnFace": true,"IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Keese_Fire_AllDay",{"ArrowName": "NormalArrow","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","IsCreateOnFace": false,"IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 1,"TerritoryArea": 0}),
    ("Enemy_Keese_Ice_AllDay",{"ArrowName": "NormalArrow","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","IsCreateOnFace": true,"IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 1,"TerritoryArea": 0}),
    ("Enemy_Keese_Swarm_AllDay",{"ArrowName": "NormalArrow","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","IsNearCreate": false,"LevelSensorMode": 1,"PatternID": -1,"SharpWeaponJudgeType": 1,"SubUnitNum": 0,"TerritoryArea": 0}),
    ("Enemy_Lizalfos_Bone_Junior",{"ArrowName": "NormalArrow","EquipItem1": "Weapon_Spear_034","EquipItem3": "LizalfosPipe","FortressEatPer": -1,"IsMimicry": false,"IsNearCreate": false,"IsWatchKeeping": true,"LevelSensorMode": 1,"RotAngle": 60,"SharpWeaponJudgeType": 0,"TerritoryArea": 0,"WaitTime": 150}),
    ("Enemy_Lizalfos_Junior",{"ArrowName": "NormalArrow","EquipItem1": "Weapon_Spear_034","EquipItem3": "LizalfosPipe","FortressEatPer": -1,"IsMimicry": false,"IsNearCreate": false,"IsWatchKeeping": true,"LevelSensorMode": 1,"RotAngle": 60,"SharpWeaponJudgeType": 0,"TerritoryArea": 0,"WaitTime": 150}),
    ("Enemy_Lizalfos_Middle",{"ArrowName": "NormalArrow","EquipItem1": "Weapon_Sword_008","FortressEatPer": -1,"IsMimicry": false,"IsNearCreate": false,"IsWatchKeeping": false,"LevelSensorMode": 1,"RotAngle": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0,"WaitTime": 1}),
    ("Enemy_Lizalfos_Senior",{"ArrowName": "NormalArrow","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","FortressEatPer": -1,"IsMimicry": false,"IsNearCreate": false,"IsWatchKeeping": true,"LevelSensorMode": 1,"RotAngle": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0,"WaitTime": 1}), 
    ("Enemy_Lizalfos_Dark",{"ArrowName": "NormalArrow","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","FortressEatPer": -1,"IsIchigekiActor": true,"IsMimicry": false,"IsNearCreate": false,"IsWatchKeeping": true,"LevelSensorMode": 1,"RotAngle": 0,"SharpWeaponJudgeType": 1,"TerritoryArea": 0,"WaitTime": 1}),
    ("Enemy_Lizalfos_Gold",{"ArrowName": "NormalArrow","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","FortressEatPer": -1,"IsMimicry": false,"IsNearCreate": false,"IsWatchKeeping": true,"LevelSensorMode": 1,"RotAngle": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0,"WaitTime": 1}),
    ("Enemy_Lizalfos_Electric",{"EquipItem1": "Weapon_Sword_029","EquipItem2": "Weapon_Shield_026","FortressEatPer": -1,"IsMimicry": false,"IsNearCreate": false,"IsWatchKeeping": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"RotAngle": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0,"WaitTime": 1}),
    ("Enemy_Lizalfos_Fire",{"ArrowName": "NormalArrow","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","FortressEatPer": -1,"IsMimicry": true,"IsNearCreate": false,"IsWatchKeeping": false,"LevelSensorMode": 1,"RotAngle": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0,"WaitTime": 1}),
    ("Enemy_Lizalfos_Ice",{"ArrowName: ":"NormalArrow","EquipItem1": "Weapon_Spear_034","FortressEatPer": -1,"IsMimicry": false,"IsNearCreate": false,"IsWatchKeeping": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"RotAngle": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0,"WaitTime": 1}),
    ("Enemy_Lynel_Junior",{"ArrowName": "ElectricArrow","EquipItem1": "Weapon_Lsword_016","EquipItem3": "Weapon_Bow_009","IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Lynel_Middle",{"ArrowName": "IceArrow","EquipItem1": "Weapon_Lsword_017","EquipItem3": "Weapon_Bow_026","IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Lynel_Senior",{"ArrowName": "IceArrow","EquipItem1": "Weapon_Lsword_018","EquipItem3": "Weapon_Bow_032","IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Lynel_Dark",{"ArrowName": "ElectricArrow","EquipItem1": "Weapon_Sword_018","EquipItem3": "Weapon_Bow_032","EquipItem4": "Default","IsLazyTraverse": true,"IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Lynel_Gold",{"ArrowName": "ElectricArrow","EquipItem1": "Weapon_Sword_018","EquipItem3": "Weapon_Bow_032","EquipItem4": "Default","IsLazyTraverse": true,"IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Moriblin_Bone_Junior",{"EquipItem1": "Weapon_Lsword_010","FortressEatPer": -1,"IsNearCreate": false,"IsWatchKeeping": true,"LevelSensorMode": 1,"RotAngle": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0,"WaitTime": 1}),
    ("Enemy_Moriblin_Junior",{"EquipItem1": "Weapon_Lsword_010","FortressEatPer": -1,"IsNearCreate": false,"IsWatchKeeping": true,"LevelSensorMode": 1,"RotAngle": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0,"WaitTime": 1}),
    ("Enemy_Moriblin_Middle",{"EquipItem1": "Weapon_Spear_002","FortressEatPer": -1,"IsNearCreate": false,"IsWatchKeeping": false,"LevelSensorMode": 1,"RotAngle": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0,"WaitTime": 1}),
    ("Enemy_Moriblin_Senior",{"EquipItem1": "Weapon_Sword_009","EquipItem2": "Weapon_Shield_009","FortressEatPer": -1,"IsNearCreate": false,"IsWatchKeeping": true,"LevelSensorMode": 1,"RotAngle": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0,"WaitTime": 1}),
    ("Enemy_Moriblin_Dark",{"ArrowName": "IceArrow","DropTable": "Normal","EquipItem1": "Weapon_Bow_001","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","FortressEatPer": -1,"IsNearCreate": false,"IsWatchKeeping": true,"LevelSensorMode": 1,"RotAngle": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0,"WaitTime": 1}),
    ("Enemy_Moriblin_Gold",{"ArrowName": "IceArrow","DropTable": "Normal","EquipItem1": "Weapon_Bow_001","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","FortressEatPer": -1,"IsNearCreate": false,"IsWatchKeeping": true,"LevelSensorMode": 1,"RotAngle": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0,"WaitTime": 1}),
    ("Enemy_Octarock",{"ArrowName": "NormalArrow","CarryActorName": "OctObj_Grass_08","DropTable": "Normal","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 1,"TerritoryArea": 0}),
    ("Enemy_Octarock_Desert",{"ArrowName": "NormalArrow","DropTable": "Normal","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","IsMimicry": false,"IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 1,"TerritoryArea": 0}),
    ("Enemy_Octarock_Forest",{"ArrowName": "NormalArrow","CarryActorName": "OctObj_Grass_05","DropTable": "Normal","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 1,"TerritoryArea": 0}),
    ("Enemy_Octarock_Snow",{"ArrowName": "NormalArrow","DropTable": "Normal","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Octarock_Stone",{"ArrowName": "NormalArrow","DropTable": "Normal","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 1,"TerritoryArea": 0}),
    ("Enemy_Wizzrobe_Electric",{"ArrowName": "NormalArrow","DropTable": "Normal","EquipItem1": "Weapon_Sword_062","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 1,"TerritoryArea": 0}),
    ("Enemy_Wizzrobe_Electric_Senior",{"EquipItem1": "Weapon_Sword_050","IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Wizzrobe_Fire",{"EquipItem1": "Weapon_Sword_060","IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Wizzrobe_Fire_Senior",{"EquipItem1": "Weapon_Sword_048","IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Wizzrobe_Ice",{"EquipItem1": "Weapon_Sword_061","IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Wizzrobe_Ice_Senior",{"EquipItem1": "Weapon_Sword_049","IsNearCreate": false,"LevelSensorMode": 1,"NearCreateAppearID": 0,"SharpWeaponJudgeType": 0,"TerritoryArea": 0})]

spawnableBoss=[
    ("Enemy_Giant_Bone_AllDay",{"EquipItem3": "Weapon_Sword_001","EquipItem4": "Weapon_Bow_001","EquipItem5": "Weapon_Lsword_002","GiantRoamType": 0,"IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Giant_Junior",{"EquipItem3": "Weapon_Sword_001","EquipItem4": "Weapon_Bow_001","EquipItem5": "Weapon_Lsword_002","GiantRoamType": 0,"IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Giant_Middle",{"EquipItem3": "Weapon_Sword_001","EquipItem4": "Weapon_Bow_001","EquipItem5": "Weapon_Spear_002","GiantArmor2": "GiantGreave_Wood_L","GiantRoamType": 0,"IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Giant_Senior",{"EquipItem3": "Weapon_Sword_024","EquipItem4": "Weapon_Bow_036","EquipItem5": "Weapon_Lsword_002","GiantArmor2": "GiantGreave_Iron_L","GiantRoamType": 0,"IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Golem_Fire",{"GolemSleepType": "SleepForward_B","GolemWeakPointLocation": "Point_B","IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Golem_Fire_R",{"ArrowName": "NormalArrow","DropTable": "Normal","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","GolemSleepType": "SleepBack_A","GolemWeakPointLocation": "Point_B","IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Golem_Ice", {"GolemSleepType": "SleepForward_B","GolemWeakPointLocation": "Point_B","IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Golem_Junior",{"GolemSleepType": "SleepForward_B","GolemWeakPointLocation": "Point_C","IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Golem_Middle",{"GolemSleepType": "SleepForward_B","GolemWeakPointLocation": "Point_B","IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Golem_Senior",{"GolemSleepType": "SleepForward_B","GolemWeakPointLocation": "Point_A","IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 0,"TerritoryArea": 0}),
    ("Enemy_Sandworm",{"ArrowName": "NormalArrow","DropTable": "Normal","EquipItem1": "Default","EquipItem2": "Default","EquipItem3": "Default","EquipItem4": "Default","IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 1,"TerritoryArea": 0}),
    ("Enemy_SandwormR",{"ArrowName": "NormalArrow","DropTable": "Normal","EquipItem1": "Default","EquipItem2": "Weapon_Spear_021","EquipItem3": "Weapon_Lsword_029","EquipItem4": "Weapon_Spear_029","EquipItem5": "Weapon_Sword_021","EquipItem6": "Weapon_Spear_030","IsNearCreate": false,"LevelSensorMode": 1,"SharpWeaponJudgeType": 1,"TerritoryArea": 0})]

blacklistFlags = ['Enemy_Dragon','Enemy_Ganon','SiteBoss','Enemy_Assassin_Senior','Enemy_Air','Quest','Item']
blacklistZones = ['E-4','D-6','D-7','E-6','E-7']

tableBow = ["Weapon_Bow_"+i for i in [
            "001","002","003","004","006","009","011","013","014","015","016","017","023","026","027","028","029",
            "030","032","033","035","036","038","040"]]
tableLsword = ["Weapon_Lsword_"+i for i in [
            "001","002","003","004","005","006","010","011","012","013","014","015","016","017","018","019","020",
            "023","024","027","029","030","031","032","033","034","035","036","037","038","041","045","047","051",
            "054","055","056","074"]]
tableShield = ["Weapon_Shield_"+i for i in [
            "001","002","003","004","005","006","007","008","009","013","014","015","016","017","018","021","022",
            "023","025","026","030","031","032","033","034","035","036","037","038","040","041","042"]]
tableSpear = ["Weapon_Spear_"+i for i in [
            "001","002","003","004","005","006","007","008","009","010","011","012","013","014","015","016","017",
            "018","021","022","023","024","025","027","028","029","030","031","032","033","034","035","036","037",
            "038","047","049","050"]]
tableSword = ["Weapon_Sword_"+i for i in [
            "001","002","003","004","005","006","007","008","009","013","014","015","016","017","018","019","020",
            "021","022","023","024","025","027","029","030","031","033","034","035","040","041","042","043","044",
            "047","048","049","050","051","052","053","060","061","062","073"]]

tableArrow = ["NormalArrow","FireArrow","IceArrow","ElectricArrow","BombArrow","AncientArrow"]

tableWeapon = tableBow + tableLsword + tableShield + tableSpear + tableSword

hasTableOther = ["Enemy_Bokoblin_Dark","Enemy_Bokoblin_Junior","Enemy_Bokoblin_Middle","Enemy_Bokoblin_Senior","Enemy_Bokoblin_Gold", "Enemy_Bokoblin_Bone_Junior_AllDay",
                 "Enemy_Lizalfos_Dark","Enemy_Lizalfos_Electric","Enemy_Lizalfos_Fire","Enemy_Lizalfos_Ice","Enemy_Lizalfos_Junior","Enemy_Lizalfos_Middle", "Enemy_Lizalfos_Bone_Junior", "Enemy_Lizalfos_Senior", "Enemy_Lizalfos_Gold",
                 "Enemy_Moriblin_Junior","Enemy_Moriblin_Middle","Enemy_Moriblin_Senior","Enemy_Moriblin_Dark","Enemy_Moriblin_Gold", "Enemy_Moriblin_Bone_Junior"]

isInGround = ["Enemy_Guardian_C", "Enemy_Keese_AllDay","Enemy_Keese_Electric_AllDay","Enemy_Keese_Fire_AllDay","Enemy_Keese_Ice_AllDay"]

isMiniGuardian = ["Enemy_Guardian_Mini_Baby","Enemy_Guardian_Mini_Junior","Enemy_Guardian_Mini_Middle","Enemy_Guardian_Mini_Senior"]

isLynel = ["Enemy_Lynel_Junior","Enemy_Lynel_Middle","Enemy_Lynel_Senior","Enemy_Lynel_Dark","Enemy_Lynel_Gold"]

hasBowOnly = ["Enemy_Assassin_Shooter_Azito_Junior"]

hasLswordOnly = ["Enemy_Assassin_Azito_Middle_DLC2"]

sandwormAllowed = True


def weighting(list, weightNums):
    weighting = []
    for i in range(len(list)):
        entry = list[i][0]
        for j in range(weightNums[entry]):
            weighting.append(list[i])
    return weighting

def altWeighting(list, weightNums):
    weighting = []
    for i in range(len(list)):
        entry = list[i]
        for j in range(weightNums[entry]):
            weighting.append(list[i])
    return weighting

def spawnableFix(list):
    for i in range(len(list)):
        for k in list[i][1]:
            if type(list[i][1][k]) == int:
                list[i][1][k] = oead.S32(list[i][1][k])
            elif type(list[i][1][k]) == float:
                list[i][1][k] = oead.F32(list[i][1][k])
    return list
    
def randomizeEnemies(fileSubpath,indexLetters,indexNumbers):
    counter = 0
    for let in indexLetters:
        for chi in indexNumbers:
            dyn = '_Dynamic.smubin'
            sta = '_Static.smubin'
            for i in [dyn,sta]:
                file = fileSubpath+let+chi+'\\'+let+chi+i
                with open(file, 'rb') as f:
                    data = oead.byml.from_binary(oead.yaz0.decompress(f.read()))
                for j in range(len(data['Objs'])):
                    configName = data['Objs'][j]['UnitConfigName']

                    # if configName not in objectsDetected:
                    #     objectsDetected[configName] = 0
                    # objectsDetected[configName] += 1

                    if checkBlacklist(configName):
                        continue

                    newEnemy = randomEnemyPick(let+chi)

                    for index in enemiesGenerated:
                        if index in newEnemy[0]:
                            enemiesGenerated[index] += 1
                            break

                    copyValues(newEnemy, data, j)
                    counter += 1
                    
                    if int(data['Objs'][j]['HashId']) in hasIchigeki:
                        data['Objs'][j]['!Parameters']['IsIchigekiActor'] = true

                    if randomWeapons:
                        randomizeWeapon(newEnemy,data,j)
                    
                    # Move Up
                    if newEnemy[0] in isInGround:
                        if 'Guardian_C' in newEnemy[0]:
                            data['Objs'][j]['Translate'][1] = oead.F32(float(data['Objs'][j]['Translate'][1]) + 7.0)
                        data['Objs'][j]['Translate'][1] = oead.F32(float(data['Objs'][j]['Translate'][1]) + 2.0)

                with open(file, 'wb') as f:
                    f.write(oead.yaz0.compress(oead.byml.to_binary(data,True)))
                # print('Processed',file)
    print("\t" + str(counter) + " enemies randomized\n")

def randomizeEnemiesPack(subPath, subPath2, packNames):
    counter = 0
    for pack in packNames:
        isThereEnemy = False
        if not Path(subPath+pack+'.pack').exists():
            continue
        data: bytes = Path(subPath+pack+'.pack').read_bytes()
        sarc = oead.Sarc(data)
        sarc_writer = oead.SarcWriter(endian=oead.Endianness.Big)
        for file in sarc.get_files():
            # print(file.data.tobytes())
            sarc_writer.files[file.name] = file.data.tobytes()
        for file in sarc.get_files():
            nom = file.name
            if nom in [subPath2+pack+'/'+pack+'_Static.smubin',subPath2+pack+'/'+pack+'_Dynamic.smubin']:
                data: bytes = file.data
                data = oead.byml.from_binary(oead.yaz0.decompress(data))
                for j in range(len(data['Objs'])):
                    configName = data['Objs'][j]['UnitConfigName']
                    
                    if checkBlacklist(configName):
                        continue
                    
                    newEnemy = randomEnemyPick('A-0')

                    for index in enemiesGenerated:
                        if index in newEnemy[0]:
                            enemiesGenerated[index] += 1
                            break
                    
                    isThereEnemy = True
                    copyValues(newEnemy, data, j)
                    counter += 1

                    if randomWeapons:
                        randomizeWeapon(newEnemy,data,j)

                sarc_writer.files[nom] = oead.yaz0.compress(oead.byml.to_binary(data,True))
        if not isThereEnemy:
            os.remove(subPath+pack+'.pack')
        else:
            _, sarc_bytes = sarc_writer.write()
            with open(subPath+pack+'.pack','wb') as f:
                f.write(sarc_bytes)
    print("\t" + str(counter) + " enemies randomized\n")

def checkBlacklist(enemyName):
    cont = enemyName[0:6] != "Enemy_"
    for blacklisted in blacklistFlags:
        if blacklisted in enemyName:
            cont = True
    return cont

def randomEnemyPick(zone):
    if randint(0,bossProb) == 0 and not chaos:
        newEnemy = random.choice(spawnableBoss)
    else:
        newEnemy = random.choice(spawnableEnemy)

    if zone in blacklistZones:
        # while newEnemy in spawnableBoss:
        #     newEnemy = random.choice(spawnableEnemy)
        # Less bosses, but not no bosses
        if newEnemy in spawnableBoss:
            if randint(0,10) == 0:
                newEnemy = random.choice(spawnableBoss)
            else:
                newEnemy = random.choice(spawnableEnemy)
    
    if 'Sandworm' in newEnemy[0] and not sandwormAllowed:
        while 'Sandworm' in newEnemy[0]:
            newEnemy = random.choice(spawnableBoss)
    
    return newEnemy

def copyValues(enemy, mapData, index):
    if "Guardian_A_Fixed" in mapData['Objs'][index]['UnitConfigName']:
        mapData['Objs'][index]['Translate'][1] = oead.F32(float(mapData['Objs'][index]['Translate'][1]) + 2.5)
    if "Golem" in enemy[0] and "Little" not in enemy[0] and enemy[0] !="Enemy_Golem_Fire_R":
        enemy[1]["GolemSleepType"] = random.choice(["SleepForward_B","SleepForward_A"])
        enemy[1]["GolemWeakPointLocation"] = random.choice(["Point_A","Point_B","Point_C"])
    elif "Giant" in enemy[0]:
        enemy[1]["EquipItem3"] = random.choice(tableWeapon)
        enemy[1]["EquipItem4"] = random.choice(tableWeapon)
        enemy[1]["EquipItem5"] = random.choice(tableWeapon)
        if "GiantArmor1" in enemy[1]:
            del enemy[1]["GiantArmor1"]
        if "GiantArmor2" in enemy[1]:
            del enemy[1]["GiantArmor2"]
        if random.randint(0,2) != 0:
            enemy[1]["GiantArmor1"] = random.choice(["GiantGreave_Wood_R","GiantGreave_Iron_R"])
        if random.randint(0,2) != 0:
            enemy[1]["GiantArmor2"] = random.choice(["GiantGreave_Wood_L","GiantGreave_Iron_L"])
    mapData['Objs'][index]['UnitConfigName'] = enemy[0]
    mapData['Objs'][index]['!Parameters'] = enemy[1]
    if 'LinksToRail' in mapData['Objs'][index]:
        del mapData['Objs'][index]['LinksToRail']
    if 'OnlyOne' in mapData['Objs'][index]:
        del mapData['Objs'][index]['OnlyOne']
    if 'Scale' in mapData['Objs'][index]:
        del mapData['Objs'][index]['Scale']
    if 'Guardian_C' in mapData['Objs'][index]['UnitConfigName']:
        mapData['Objs'][index]['Translate'][1] = oead.F32(float(mapData['Objs'][index]['Translate'][1]) + 30.0)
    if 'Keese' in mapData['Objs'][index]['UnitConfigName']:
        mapData['Objs'][index]['Translate'][1] = oead.F32(float(mapData['Objs'][index]['Translate'][1]) + 2.5)

def randomizeWeapon(enemy, mapData, index):
    # Mini-Guardian
    if enemy[0] in isMiniGuardian:
        weaponChoices = [tableLsword, tableShield, tableSpear, tableSword]
        if enemy[0] == "Enemy_Guardian_Mini_Senior":
            mapData['Objs'][index]['!Parameters']['EquipItem1'] = random.choice(weaponChoices.pop(randint(0,len(weaponChoices)-1)))
            mapData['Objs'][index]['!Parameters']['EquipItem2'] = random.choice(weaponChoices.pop(randint(0,len(weaponChoices)-1)))
            mapData['Objs'][index]['!Parameters']['EquipItem3'] = random.choice(weaponChoices.pop(randint(0,len(weaponChoices)-1)))
        elif enemy[0] == "Enemy_Guardian_Mini_Middle":
            mapData['Objs'][index]['!Parameters']['EquipItem1'] = random.choice(weaponChoices.pop(randint(0,len(weaponChoices)-1)))
            mapData['Objs'][index]['!Parameters']['EquipItem2'] = random.choice(weaponChoices.pop(randint(0,len(weaponChoices)-1)))
        elif enemy[0] == "Enemy_Guardian_Mini_Junior":
            mapData['Objs'][index]['!Parameters']['EquipItem1'] = random.choice(weaponChoices.pop(randint(0,len(weaponChoices)-1)))

    # Greatsword Only
    elif enemy[0] in hasLswordOnly:
        mapData['Objs'][index]['!Parameters']['EquipItem1'] = random.choice(tableLsword)

    # Bow Only
    elif enemy[0] in hasBowOnly:
        mapData['Objs'][index]['!Parameters']['EquipItem1'] = random.choice(tableBow)
        mapData['Objs'][index]['!Parameters']['ArrowName'] = random.choice(tableArrow)

    # Lynel
    elif enemy[0] in isLynel:
        # Add Bow
        mapData['Objs'][index]['!Parameters']['EquipItem3'] = random.choice(tableBow)
        # Add Arrow
        mapData['Objs'][index]['!Parameters']['ArrowName'] = random.choice(tableArrow)
        # Roll Type
        alea=randint(0,2)
        # Sword & Shield
        if alea == 0:
            mapData['Objs'][index]['!Parameters']['EquipItem1'] = random.choice(tableSword)
            mapData['Objs'][index]['!Parameters']['EquipItem4'] = random.choice(tableShield)
        # Spear
        elif alea == 1:
            mapData['Objs'][index]['!Parameters']['EquipItem1'] = random.choice(tableSpear)
        # Greatsword
        else:
            mapData['Objs'][index]['!Parameters']['EquipItem1'] = random.choice(tableLsword)

    # Any Weapon
    elif enemy[0] in hasTableOther:
        alea=randint(0,3)
        if 'EquipItem1' in mapData['Objs'][index]['!Parameters']:
            mapData['Objs'][index]['!Parameters']['EquipItem1'] = "Default"
        if 'EquipItem2' in mapData['Objs'][index]['!Parameters']:
            mapData['Objs'][index]['!Parameters']['EquipItem2'] = "Default"
        if 'EquipItem3' in mapData['Objs'][index]['!Parameters']:
            mapData['Objs'][index]['!Parameters']['EquipItem3'] = "Default"
        if 'EquipItem4' in mapData['Objs'][index]['!Parameters']:
            mapData['Objs'][index]['!Parameters']['EquipItem4'] = "Default"
        if alea == 0:
            mapData['Objs'][index]['!Parameters']['EquipItem1'] = random.choice(tableSword)
            mapData['Objs'][index]['!Parameters']['EquipItem2'] = random.choice(tableShield)
        elif alea == 1:
            mapData['Objs'][index]['!Parameters']['EquipItem1'] = random.choice(tableSpear)
        elif alea == 2:
            mapData['Objs'][index]['!Parameters']['EquipItem1'] = random.choice(tableBow)
            mapData['Objs'][index]['!Parameters']['ArrowName'] = random.choice(tableArrow)
        else:
            mapData['Objs'][index]['!Parameters']['EquipItem1'] = random.choice(tableLsword)

spawnableEnemy = spawnableFix(spawnableEnemy)
spawnableBoss = spawnableFix(spawnableBoss)

if not chaos:
    spawnableEnemy = weighting(spawnableEnemy, weights)
    spawnableBoss = weighting(spawnableBoss, weightsBoss)
    tableArrow = altWeighting(tableArrow, weightsArrow)
else:
    spawnableEnemy += spawnableBoss
print()
if hyrule:
    print("Randomizing Hyrule enemies...")
    randomizeEnemies('Enemy Randomizer v2\\content\\Map\\MainField\\',["A-","B-","C-","D-","E-","F-","G-","H-","I-","J-"],["1","2","3","4","5","6","7","8"])
sandwormAllowed = False

if swordTrial:
    print("Randomizing Trial of the Sword enemies...")
    randomizeEnemies('Enemy Randomizer v2\\aoc\\0010\\Map\\AocField\\',["A-","B-"],["1","2","3"])

if shrines:
    print("Randomizing Shrine enemies...")
    randomizeEnemiesPack('Enemy Randomizer v2\\content\\Pack\\','Map/CDungeon/',['Dungeon'+str(i)[1:4] for i in range(1000,1120)])

if dlcshrines:
  print("Randomizing DLC Shrines enemies...")
  randomizeEnemiesPack('Enemy Randomizer v2\\aoc\\0010\\Pack\\','Map/CDungeon/',['Dungeon'+str(i)[1:4] for i in range(1120,1136)])

if beasts:
    print("Randomizing Divine Beast enemies...")
    randomizeEnemiesPack('Enemy Randomizer v2\\aoc\\0010\\Pack\\','Map/MainFieldDungeon/',['RemainsWater','RemainsFire','RemainsElectric','RemainsWind','FinalTrial'])

# for i in sorted(objectsDetected):
#     print(i, objectsDetected[i])

print("Total enemies generated:")
print(enemiesGenerated)
input('Press Enter to exit...')


