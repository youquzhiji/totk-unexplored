import json
import regex as re
import os
import argparse
import numpy as np

BOSSES_REMATCH = [
    [-1154.3687744140625, -529.5303344726562, 3626.1552734375],
    # 11392603486633175579 - Enemy_DungeonBoss_Rito_Underground
    [1607.1004638671875, -354.0353088378906, 62.11279296875],
    # 13478036497897348683 - Enemy_DungeonBoss_Goron_Underground
    [949.4633178710938, -364.2261962890625, 461.0583190917969],
    # 13679657688670718412 - Enemy_DungeonBoss_Gerudo_Underground
    [-2720.704833984375, -546.7757568359375, 76.66574096679688],
    # 16102269431729981480 - Enemy_DungeonBoss_Gerudo_Underground
    [2145.2978515625, -489.21875, 627.767822265625],  # 268066833160582041 - Enemy_DungeonBoss_Goron_Underground
    [-4370.8974609375, -530.1677856445312, -3046.453125],  # 2913438567168641393 - Enemy_DungeonBoss_Rito_Underground
    [-1243.7784423828125, -443.6505126953125, -2014.3238525390625],
    # 4047783038021099072 - Enemy_DungeonBoss_Zora_Underground
    [2837.0, -685.8195190429688, -610.0],  # 5069068021545237469 - Enemy_DungeonBoss_Zora_Underground
    [3671.0791015625, -434.81951904296875, -1680.5042724609375],
    # 5210398793000277741 - Enemy_DungeonBoss_Zora_Underground
    [-3635.715576171875, -926.6304931640625, 837.6383666992188],
    # 6031128008877239078 - Enemy_DungeonBoss_Gerudo_Underground
    [-2266.555419921875, -710.8698120117188, -3266.33154296875],
    # 7058364791334812681 - Enemy_DungeonBoss_Rito_Underground
    [-2792.8583984375, -440.26953125, 759.00732421875]  # 8899164221420779612 - Enemy_DungeonBoss_Goron_Underground
]

BOSSES_REMATCH_DEFEATED = [

    0xab170b3c,  # 11392603486633175579 - Enemy_DungeonBoss_Rito_Underground
    0xa0b5253d,  # 13478036497897348683 - Enemy_DungeonBoss_Goron_Underground
    0xa6e5f8f9,  # 13679657688670718412 - Enemy_DungeonBoss_Gerudo_Underground
    0x0069a6fe,  # 16102269431729981480 - Enemy_DungeonBoss_Gerudo_Underground
    0xf2b13c3f,  # 268066833160582041 - Enemy_DungeonBoss_Goron_Underground
    0x0f86acd0,  # 2913438567168641393 - Enemy_DungeonBoss_Rito_Underground
    0x8fd913f8,  # 4047783038021099072 - Enemy_DungeonBoss_Zora_Underground
    0xbc9fde5a,  # 5069068021545237469 - Enemy_DungeonBoss_Zora_Underground
    0x2730997d,  # 5210398793000277741 - Enemy_DungeonBoss_Zora_Underground
    0xe72eb42e,  # 6031128008877239078 - Enemy_DungeonBoss_Gerudo_Underground
    0xe18248e8,  # 7058364791334812681 - Enemy_DungeonBoss_Rito_Underground
    0xffb3f46b  # 8899164221420779612 - Enemy_DungeonBoss_Goron_Underground
]

WELL_STATUS = [
    # seems to be needed in order for the icon to appear in map and also to count towards 100%
    # IsVisitLocationArea_CaveEntrance.
    0x45b30297,  # 13194262444821253016 - Well_0001
    0xed8c6c70,  # 17178703360531207997 - Well_0002
    0xb91f743d,  # 7062249617308613387 - Well_0003
    0xd81c08d6,  # 11933224307091230694 - Well_0004
    0x0ef1efca,  # 17490979021949379359 - Well_0005
    0xbad036bf,  # 3812226219033581199 - Well_0006
    0xcf474c86,  # 11200109829905050648 - Well_0007
    0xc50cdfb7,  # 9877532556918825502 - Well_0008
    0x73d3b6a1,  # 17331489093918561059 - Well_0009
    0x0a623984,  # 5433239543305108333 - Well_0010
    0xbe134c79,  # 18374843825268348839 - Well_0011
    0x321a53c1,  # 5573801400564842698 - Well_0012
    0x52fc93c7,  # 8464135276822714214 - Well_0013
    0x10d31a20,  # 8343852468912327656 - Well_0014
    0x50b7ff7c,  # 6244318697190485736 - Well_0015
    0xf2369d24,  # 14008184576550557030 - Well_0016
    0x7b698cff,  # 2682661287366618580 - Well_0017
    0x9d8c9e37,  # 18292467756691799253 - Well_0018
    0x8d94eccf,  # 15263783675053925142 - Well_0019
    0x8aec454c,  # 14294001447745603636 - Well_0020
    0x4362cf69,  # 483243831094194862 - Well_0021
    0x84260607,  # 16136047310243677537 - Well_0022
    0xaa692d8f,  # 14203679129553496960 - Well_0023
    0x097d69f4,  # 15539656917565867470 - Well_0024
    0xd65c76bd,  # 3409760176723313861 - Well_0025
    0xcaa22279,  # 7162466888885758692 - Well_0026
    0x6efd054e,  # 4504342832330418540 - Well_0027
    0x1a1d2dc4,  # 3624902666293548976 - Well_0028
    0x33c242cf,  # 8973258028144868802 - Well_0029
    0xfc42a6b8,  # 1154334463393842455 - Well_0030
    0xd97f0bf2,  # 11738989003295390645 - Well_0031
    0xaff27cb8,  # 2155917192954298383 - Well_0032
    0x8433b864,  # 5334751970332889797 - Well_0033
    0x9c102b50,  # 8216510434135260539 - Well_0034
    0x2dba628c,  # 5631944481270506220 - Well_0041
    0x307478a2,  # 1774279682527688702 - Well_0042
    0xaf2751bc,  # 6433184824016975873 - Well_0043
    0xf281fcdf,  # 5021182011261805087 - Well_0044
    0xf790f14c,  # 16477279299337157907 - Well_0045
    0x146228ba,  # 9000359301995578366 - Well_0046
    0xd0e99318,  # 16802610989801911938 - Well_0047
    0xdb05738a,  # 13473655612253629489 - Well_0047B
    0x324e7abe,  # 11679239074233164527 - Well_0048
    0xcc574d89,  # 12969905487474250827 - Well_0049
    0x51ca4ba7,  # 13777722591245673954 - Well_0049B
    0x91c7b29b,  # 17171302321035659098 - Well_0049C
    0xbe2e98c8,  # 9327423028890108170 - Well_0049D
    0xbdb49eca,  # 5906427813420395857 - Well_0049E
    0x96a89582,  # 10040443261155710972 - Well_0050
    0x91d5dbc4,  # 9559166076253669217 - Well_0051
    0x933ef2da,  # 1662241179931426393 - Well_0052
    0xde9778a1,  # 18270657436817135448 - Well_0053
    0xca3759a0,  # 5515697063015506333 - Well_0054
    0xd2e03aab,  # 3244074412902120610 - Well_0055
    0x9b585a39,  # 10430103283884318777 - Well_0056
    0x657ad3df,  # 7517110108375739855 - Well_0057
    0x295a5e07,  # 15893213395873888747 - Well_0058
    0x580b10e3  # 9748532938243040102 - Well_0059
]
CAVE_STATUS = [
    # IsGetCaveMasterMedal.Cave_
    0x3a4892fd,  # Akkala_0000
    0xb3ce2279,  # Akkala_0003
    0x5c12f666,  # Akkala_0005
    0xd9e04dd4,  # Akkala_0007
    0x0c144ba9,  # Akkala_0010
    0x4b352a68,  # Akkala_0011
    0x9c3bc68e,  # Akkala_0014
    0xe23763f3,  # Akkala_0017
    0x9c154963,  # CentralHyrule_0008
    0x36966a7b,  # CentralHyrule_0009
    0x8aedd1dc,  # CentralHyrule_0011
    0x05db09b4,  # CentralHyrule_0013
    0x3a8438f6,  # CentralHyrule_0017
    0x694d3922,  # CentralHyrule_0018
    0x057aae24,  # CentralHyrule_0019
    0x91b93260,  # CentralHyrule_0020
    0xa9425920,  # CentralHyrule_0021
    0xb377534f,  # CentralHyrule_0022
    0xc51c271c,  # CentralHyrule_0023
    0x9ec19a00,  # CentralHyrule_0030
    0xee968d65,  # Eldin_0020
    0xefe12df2,  # Eldin_0021
    0x0b90d147,  # Eldin_0022
    0xe168d362,  # Eldin_0023
    0x97a8995f,  # Eldin_0025
    0x6ec69925,  # Eldin_0026
    0x921f2755,  # Eldin_0027
    0x74ad5d43,  # Eldin_0028
    0x109acbe3,  # Eldin_0029
    0x9462567e,  # Eldin_0030
    0x98a1676d,  # Eldin_0031
    0x093281e3,  # Eldin_0033
    0xe7bc5beb,  # Eldin_0034
    0xfed5cd46,  # Eldin_0035
    0x89e6d2e9,  # Eldin_0037
    0xe65ffe1d,  # Eldin_0038
    0xcf7e6457,  # Eldin_0039
    0xcd316527,  # Firone_0002
    0xaecb682e,  # Firone_0008
    0x4349c90d,  # Firone_0009
    0x785fd37d,  # Firone_0016
    0x7419780f,  # Firone_0020
    0x91a70897,  # Firone_0022
    0xfd1576bf,  # Firone_0023
    0xeb336b37,  # Firone_0024
    0x9a70291f,  # Firone_0029
    0x75796c16,  # FirstPlateau_0001
    0x47d4dc0f,  # FirstPlateau_0002
    0x7f61cdfd,  # GerudoDesert_0007
    0x6510f426,  # GerudoDesert_0008
    0x4ca1fdd2,  # GerudoDesert_0015
    0x3c499ceb,  # GerudoDesert_0022
    0x58028ec0,  # GerudoDesert_0030
    0xffe03687,  # GerudoDesert_0031
    0x7be30826,  # GerudoDesert_0032
    0x20a60062,  # GerudoDesert_0035
    0x3d235262,  # GerudoDesert_0036
    0x06750ea3,  # GerudoDesert_0037
    0x542a183e,  # GerudoDesert_0039
    0x173aaee7,  # GerudoDesert_0040
    0x6728247e,  # GerudoDesert_0041
    0xa8c973a3,  # GerudoDesert_0044
    0xb8f1f3c1,  # GerudoDesert_0045
    0x393e032c,  # GerudoDesert_0046
    0x3d59ac0e,  # GerudoDesert_0049
    0x12cdc1f2,  # GerudoDesert_0050
    0xa7a7d61d,  # GerudoDesert_0051
    0xe7b3e8fd,  # GerudoHighlands_0002
    0x4d4df44a,  # GerudoHighlands_0008
    0x48b72033,  # GerudoHighlands_0014
    0xe6e7de47,  # GerudoHighlands_0017
    0x28ea1102,  # HateruEast_0000
    0xb1c7be06,  # HateruEast_0002
    0x1abd365f,  # HateruEast_0006
    0x46d1603b,  # HateruEast_0007
    0x5d305283,  # HateruEast_0008
    0xa913a912,  # HateruEast_0009
    0x5ff05676,  # HateruEast_0013
    0xd1a3108a,  # HateruEast_0014
    0x6d406e0f,  # HateruEast_0016
    0x65f30245,  # HateruWest_0002
    0x9155a62e,  # HateruWest_0005
    0x86cda846,  # HateruWest_0006
    0xc52025ad,  # HateruWest_0008
    0x2affeb89,  # HateruWest_0011
    0xd40717b8,  # HateruWest_0012
    0x9c02adf9,  # Hebra_0000
    0xee23a63d,  # Hebra_0013
    0xaea53961,  # Hebra_0015
    0x3bffd5b7,  # Hebra_0016
    0x4087bd4e,  # Hebra_0019
    0xde0f7c34,  # Hebra_0021
    0x72fbb2c6,  # Hebra_0022
    0xa6ede8f8,  # Hebra_0023
    0xb3dba045,  # Hebra_0025
    0xf764bed9,  # Hebra_0026
    0x91522a83,  # Hebra_0030
    0x4e3ab0d4,  # Hebra_0035
    0xed1deb3b,  # Hebra_0036
    0xaf73d942,  # Hebra_0037
    0xd884bf98,  # Hebra_0039
    0x9a9260d0,  # Hebra_0040
    0xec56a695,  # Hebra_0041
    0x8ae4b8fb,  # HyruleForest_0001
    0x02829324,  # HyruleForest_0006
    0x95dd6439,  # HyruleForest_0007
    0x965bb738,  # HyruleForest_0008
    0x0c4fa74c,  # HyruleRidge_0000
    0x52b7f157,  # HyruleRidge_0002
    0x67acbeb9,  # HyruleRidge_0003
    0xe6e5f556,  # HyruleRidge_0005
    0xc7aa5ca0,  # HyruleRidge_0006
    0x1f24ce09,  # HyruleRidge_0007
    0x20ea3880,  # HyruleRidge_0008
    0xdcd9a527,  # Lanayru_0006
    0xcd578915,  # Lanayru_0008
    0x46bbf652,  # Lanayru_0014
    0x09bf0c1d,  # Lanayru_0019
    0x0d21fe8f,  # Lanayru_0024
    0x52ba8073,  # Lanayru_0032
    0x070b77a4,  # Lanayru_0033
    0x09007d0e,  # Lanayru_0035
    0xbf93c5f7,  # Lanayru_0036
    0xfbe18fd6,  # Lanayru_0048
    0x0aadbad2,  # Lanayru_0049
    0x61cabc09,  # Lanayru_0052
    0xe6a0230a,  # Lanayru_0053
    0x8d797c20,  # Lanayru_0055
    0xe349a05c,  # Lanayru_0057
    0xa05c2ee9,  # Lanayru_0060
    0x6df6538a,  # Lanayru_0061
    0xae1f8688,  # LanayruMountain_0002
    0xe9fd11b0,  # LanayruMountain_0006
    0xd99ae420,  # LanayruMountain_0008
    0x5a87eef9,  # LanayruMountain_0010
    0x6ea55e80,  # LanayruMountain_0014
    0xaf6d0f65,  # LanayruMountain_0016
    0xbf5b8586,  # LanayruMountain_0022
    0x18602fad,  # LanayruMountain_0024
    0xc2e43cc6,  # LanayruMountain_0025
    0x57acfa65,  # LanayruMountain_0026
    0x801e08e3,  # Tabantha_0001
    0x891f9219,  # Tabantha_0002
    0xf8017f51,  # Tabantha_0003
    0x1f859e86,  # Well_0043B
    0x825b96c0,  # Zora_Imperial_Palace
    0x5b4fdd02,  # ZoraZonauTerminal
]

WELL = [
    [-3831.584, 230.703, -2105.445],  # 13194262444821253016 - Well_0001
    [-2358.595, 367.4547, -1871.801],  # 17178703360531207997 - Well_0002
    [-1810.858, 196.3615, -1623.456],  # 7062249617308613387 - Well_0003
    [-1069.444, 203.7078, -2325.903],  # 11933224307091230694 - Well_0004
    [-911.3, 195.5639, -1616.2],  # 17490979021949379359 - Well_0005
    [-670.9031, 177.8872, -1351.729],  # 3812226219033581199 - Well_0006
    [-1039.614, 124.1464, -415.3119],  # 11200109829905050648 - Well_0007
    [-912.8082, 109.3519, -331.207],  # 9877532556918825502 - Well_0008
    [-1313.988, 99.37948, 622.6918],  # 17331489093918561059 - Well_0009
    [-879.179, 111.336, 1101.615],  # 5433239543305108333 - Well_0010
    [-1460.715, 122.0619, 1296.74],  # 18374843825268348839 - Well_0011
    [-1680.918, 211.5355, 1349.228],  # 5573801400564842698 - Well_0012
    [-1720.26, 125.6991, 2238.07],  # 8464135276822714214 - Well_0013
    [662, 129.684, -1266.5],  # 8343852468912327656 - Well_0014
    [62.63467, 117.6656, -547.6163],  # 6244318697190485736 - Well_0015
    [-68.06168, 114.6147, 163.0891],  # 14008184576550557030 - Well_0016
    [786.9977, 120.705, -7.592865],  # 2682661287366618580 - Well_0017
    [686.1927, 107.3817, 766.4301],  # 18292467756691799253 - Well_0018
    [782.5, 126, 1496.9],  # 15263783675053925142 - Well_0019
    [316.5151, 99.1031, 1856.799],  # 14294001447745603636 - Well_0020
    [322.3558, 100.5785, 1927.037],  # 483243831094194862 - Well_0021
    [423.4993, 99.49803, 2042.955],  # 16136047310243677537 - Well_0022
    [339.629, 117.7631, 2098.56],  # 14203679129553496960 - Well_0023
    [316.0589, 135.0148, 2127.813],  # 15539656917565867470 - Well_0024
    [594.4839, 183.014, 2100.442],  # 3409760176723313861 - Well_0025
    [606.1266, 140.7945, 2261.083],  # 7162466888885758692 - Well_0026
    [1544.127, 98.71378, -169.9368],  # 4504342832330418540 - Well_0027
    [1435.5, 99.67163, 136.4959],  # 3624902666293548976 - Well_0028
    [1529.16, 99.65267, 326.8987],  # 8973258028144868802 - Well_0029
    [1219.596, 100.1902, 397.1848],  # 1154334463393842455 - Well_0030
    [1716.448, 113.5011, 650.8704],  # 11738989003295390645 - Well_0031
    [2746.387, 220.0299, -175.5236],  # 2155917192954298383 - Well_0032
    [3057.234, 423.9277, -2310.919],  # 5334751970332889797 - Well_0033
    [-3235.338, 113.4215, 2606.406],  # 8216510434135260539 - Well_0034
    [2940.59, 101.111, 3378.44],  # 5631944481270506220 - Well_0041
    [1535.121, 151.8213, 3553.629],  # 1774279682527688702 - Well_0042
    [537.629, 138.9138, 3426.698],  # 6433184824016975873 - Well_0043
    [-1679.566, 326, -2586],  # 5021182011261805087 - Well_0044
    [-2820, 120.964, 2233],  # 16477279299337157907 - Well_0045
    [365.4017, 101.3057, 1126.331],  # 9000359301995578366 - Well_0046
    [884.597, 117.3564, 195.319],  # 16802610989801911938 - Well_0047
    [858.0345, 117.3564, 262.7126],  # 13473655612253629489 - Well_0047B
    [1794.704, 101.8641, 1949.73],  # 11679239074233164527 - Well_0048
    [3421.88, 229.4044, 2029.529],  # 12969905487474250827 - Well_0049
    [3356.756, 209.4572, 2050.473],  # 13777722591245673954 - Well_0049B
    [3514.478, 220.4324, 2152.45],  # 17171302321035659098 - Well_0049C
    [3384.515, 227.3835, 2211.729],  # 9327423028890108170 - Well_0049D
    [3301.478, 221.9783, 2300.911],  # 5906427813420395857 - Well_0049E
    [-1357.184, 167.0685, -700.063],  # 10040443261155710972 - Well_0050
    [1875.014, 215.0161, 1043.556],  # 9559166076253669217 - Well_0051
    [1092.674, 113.5, -1154.046],  # 1662241179931426393 - Well_0052
    [-212.0227, 109.9849, -134.9251],  # 18270657436817135448 - Well_0053
    [2617.932, 239.5, -1169.059],  # 5515697063015506333 - Well_0054
    [3719.832, 182.6035, -1587.556],  # 3244074412902120610 - Well_0055
    [3195, 292.768, -1715.5],  # 10430103283884318777 - Well_0056
    [4232.868, 217.473, -2780.07],  # 7517110108375739855 - Well_0057
    [394.5, 138, 3387],  # 15893213395873888747 - Well_0058
    [-2958.587, 260.9558, -531.9565]  # 9748532938243040102 - Well_0059
]
CAVE = [
    [4122.229, 293.179, -662.295],  # Cave_Akkala_0000
    # [4122.229, 293.179, -662.295],

    [4505.99, 201.8511, -705.3162],  # Cave_Akkala_0003
    # [4505, 209.9406, -705.1617],

    [3925.927, 212.3195, -1576.423],  # Cave_Akkala_0005
    # [3925.927, 212.5605, -1576.423],

    [3678.723, 179.5108, -1538.252],  # Cave_Akkala_0007
    # [3678.723, 179.5108, -1538.252],
    # [3735.437, 190.3167, -1534.085],
    # [3735.437, 186.3167, -1534.085],

    [3243.716, 399.535, -1456.824],  # Cave_Akkala_0010
    # [3243.716, 399.535, -1456.824],

    [3321.5, 276.5, -3424],  # Cave_Akkala_0011
    # [3321.5, 276.5, -3424],

    [4650.503, 54.9944, -3584.834],  # Cave_Akkala_0014
    # [4645.503, 111.9944, -3206.834],
    # [4650.67, 104.5, -3584.908],
    # [4650.67, 54.5, -3584.908],

    [3292.5, 500.0642, -1492],  # Cave_Akkala_0017
    # [3292.5, 500.0642, -1492],

    # [37.30195, 128.1821, 198.8625], #Cave_CentralHyrule_0008
    # [6.009788, 141.0668, 157.9319],
    [37.30195, 124.1821, 198.8625],
    # [6.009788, 136.0668, 157.9319],

    # [-832.3462, 137.4909, 1488.377], #Cave_CentralHyrule_0009
    [-832.3462, 132.4909, 1488.377],

    #[711.5814, 1596.062, 1449.099],  # Cave_CentralHyrule_0011
    # [739.0957, 1652.759, 1358.025],
    [711.5814, 1591.062, 1449.099],
    # [739.0957, 1647.759, 1358.025],

    #[587.4191, 1553.043, 1624.505],  # Cave_CentralHyrule_0013
    # [632.1589, 1593.918, 1638.774],
    [632.2798, 1588.919, 1638.811],
    # [587.4191, 1548.043, 1624.505],

    #[170.5166, 1487.815, 1633.773],  # Cave_CentralHyrule_0017
    # [260.1547, 1471.727, 1557.838],
     [170.5166, 1482.815, 1633.773],
    # [260.1547, 1466.727, 1557.838],

    # [-253.8396, 120.3645, -98], #Cave_CentralHyrule_0018
    # [-253.8998, 212.6871, -749.0048],
    # [-318.5, 182.7972, -782.5],
    [-325.6665, 159.5706, -802.5264],
    # [-254.0375, 113.5017, -129],
    # [-253.9667, 132.8978, -767.084],

    #[380.06, 1521.65, 1631.647],  # Cave_CentralHyrule_0019
    # [489.6634, 1483.25, 1625.622],
    [380.06, 1516.65, 1631.647],
    # [489.6634, 1473.25, 1625.622],

    # [-1111.5, 148.2, 432.0626], #Cave_CentralHyrule_0020
    [-1111.5, 128.2, 432.0626],

    # [-72.10925, 125.9356, 1045.974], #Cave_CentralHyrule_0021
    [-72.10925, 122.9356, 1045.974],

    # [-512.3591, 130.869, -127.5918], #Cave_CentralHyrule_0022
    [-512.3591, 125.869, -127.5918],

    # [-1167.155, 137.7493, 1310.977], #Cave_CentralHyrule_0023
    [-1167.155, 127.7493, 1310.977],

    # [-1404.5, 108.66, 256.5], #Cave_CentralHyrule_0030
    [-1404.5, 101.56, 256.5],

    # [2767.812, 634.8295, -2778.185], #Cave_Eldin_0020
    [2767.812, 626.8295, -2778.185],

    # 2238.605, 636.0185, -2682.376], #Cave_Eldin_0021
    [2238.605, 626.0185, -2682.376],

    # [2373.343, 561.8396, -3051.703], #Cave_Eldin_0022
    [2373.343, 550.8396, -3051.703],

    # [1554.559, 506.4309, -3102.513], #Cave_Eldin_0023
    [1554.559, 498.4309, -3102.513],

    # [1423.078, 394.9322, -2102.729], #Cave_Eldin_0025
    [1423.078, 389.9322, -2102.729],

    # [1746.19, 450.72, -1926.52], #Cave_Eldin_0026
    [1800.955, 425.9151, -1983.352],

    # [2016, 531.2755, -2038.984], #Cave_Eldin_0027
    [2016, 526.2755, -2038.984],

    # [1642.848, 389.5436, -1729.563], #Cave_Eldin_0028
    [1642.848, 384.5436, -1729.563],

    # [1853.956, 406.4446, -1719.953], #Cave_Eldin_0029
    [1853.956, 397.4446, -1719.953],

    # [2206.314, 514.6932, -3075.319], #Cave_Eldin_0030
    [2206.314, 510.9432, -3075.319],

    # [2485.386, 268.3781, -1792.983], #Cave_Eldin_0031
    [2485.386, 263.3781, -1792.983],

    # [1764.653, 511.2603, -2837.404], #Cave_Eldin_0033
    [1764.653, 505.2603, -2837.404],

    # [1713.881, 511.1068, -2718.587], #Cave_Eldin_0034
    [1713.881, 506.1068, -2718.587],

    # [1949.909, 537.4574, -2687.209], #Cave_Eldin_0035
    [1949.909, 531.4574, -2687.209],

    # [1929.11, 238.2568, -1278.69], #Cave_Eldin_0037
    # [1931.949, 283.4043, -1312.395],
    [1929.5, 227.2706, -1271.645],
    # [1931.949, 273.6543, -1304.573],

    # [2593.647, 261.4519, -1330.448], #Cave_Eldin_0038
    [2593.647, 256.4519, -1330.448],

    # [2275.316, 267.5, -1520.099], #Cave_Eldin_0039
    [2275.316, 262.5, -1520.099],

    # [809.8935, 121.2152, 2971.707], #Cave_Firone_0002
    [809.8935, 116.2152, 2971.707],

    # [671.8048, 134.3863, 3109.481], #Cave_Firone_0008
    [671.8048, 129.3863, 3109.481],

    # [1169.23, 283.2793, 2443.27], #Cave_Firone_0009
    [1169.635, 282.5722, 2443.85],

    # [-176.3386, 126.6612, 3062.832], #Cave_Firone_0016
    # [-256.1517, 101.9714, 2940.198],
    [-256.1517, 86.97139, 2940.198],
    # [-171.1738, 92.30429, 3067.066],

    # [568.6034, 123.2259, 2981.877], #Cave_Firone_0020
    [568.6034, 118.2259, 2981.877],

    # [1203.094, 135.9193, 3170.906], #Cave_Firone_0022
    [1203.094, 130.9193, 3170.906],

    # [126.18, 68.16491, 2501.39], #Cave_Firone_0023
    [125.7477, 15.91255, 2501.451],

    # [608.9023, 161.3276, 2210.08], #Cave_Firone_0024
    [608.9023, 156.3276, 2210.08],

    # [280.2788, 135.6949, 3875.137], #Cave_Firone_0029
    [283.978, 138.5791, 3851.469],

    # [-1111.638, 254.71, 2148.178], #Cave_FirstPlateau_0001
    [-1092.381, 249.1899, 2162.711],

    # [-1061.875, 252.6713, 1829.554], #Cave_FirstPlateau_0002
    [-1061.875, 247.6713, 1829.554],

    # [-3763.073, 140.5631, 2698], #Cave_GerudoDesert_0007
    # [-3763.275, 130.3909, 2420.758],
    [-3763.275, 120.3909, 2698.519],
    # [-3763.275, 120.3909, 2420.758],

    # [-3827.19, 145.7133, 2650.319], #Cave_GerudoDesert_0008
    [-3827.19, 140.7133, 2650.319],

    # [-3242.9, 104.4685, 2936.6], #Cave_GerudoDesert_0015
    [-3238.816, 39.57154, 2939.655],

    # [-1795.805, 143.65, 1961.14], #Cave_GerudoDesert_0022
    # [-1967.004, 145.5133, 2059.611],
    [-1967.004, 135.5133, 2059.611],
    # [-1795.805, 136.65, 1961.14],

    # [-1527.762, 89.89854, 2222.542], #Cave_GerudoDesert_0030
    [-1527.762, 84.89854, 2222.542],

    # [-2696.307, 94.37949, 2809.372],#Cave_GerudoDesert_0031
    [-2696.025, 38.1045, 2808.615],

    # [-3679.051, 97.04066, 3255.366], #Cave_GerudoDesert_0032
    [-3679.051, 87.04066, 3255.366],

    # [-1726.964, 115.5759, 2183.379], #Cave_GerudoDesert_0035
    [-1726.964, 110.5759, 2183.379],

    # [-1744.354, 99.30705, 2394.182], #Cave_GerudoDesert_0036
    [-1744.354, 94.30705, 2394.182],

    # [-2215.908, 357.7064, 2395.27], #Cave_GerudoDesert_0037
    [-2215.908, 352.7064, 2395.27],

    # [-3099.359, 63.95093, 3063.779], #Cave_GerudoDesert_0039
    [-3099.359, 53.95093, 3063.779],

    # [-2941, 100.52, 3857.9], #Cave_GerudoDesert_0040
    [-2939.102, 68.4035, 3857.828],

    # [-2173.727, 242.0874, 1841.648], #Cave_GerudoDesert_0041
    # [-2258.922, 171.9476, 1759.334],
    [-2258.922, 161.9476, 1759.334],
    # [-2173.727, 232.0874, 1841.648],

    # [-2521.423, 97.38815, 3725], #Cave_GerudoDesert_0044
    [-2535.542, 57.27916, 3626.101],
    # [-2518.917, 57.84764, 3671.562],
    # [-2584.241, 57.52135, 3638.208],
    # [-2570.56, 54.07516, 3744.447],
    # [-2530.788, 58.68051, 3769.119],
    # [-2480.565, 58.84991, 3758.143],
    # [-2521.204, 58.38428, 3724.844],
    # [-2564.693, 57.20284, 3681.715],
    # [-2451.857, 58.97064, 3676.729],
    # [-2480.763, 58.91989, 3632.817],
    # [-2477.854, 58.3941, 3709.82],
    # [-2604.787, 55.75517, 3709.315],

    # [-3354.8, 121, 2694.6], #Cave_GerudoDesert_0045
    [-3354.94, 101.1725, 2693.962],

    # [-4814.321, 112, 3875.428], #Cave_GerudoDesert_0046
    [-4814.321, 104.5, 3875.428],

    # [-4673.2, 119.7035, 1986.137], #Cave_GerudoDesert_0049
    [-4673.2, 114.7035, 1986.137],

    # [-2413.649, 255.2226, 1824.038], #Cave_GerudoDesert_0050
    [-2433.913, 251.2361, 1819.683],

    # [-2611.278, 222.9838, 2604.77], #Cave_GerudoDesert_0051
    # [-2676.715, 190.073, 2402.609],
    [-2611.278, 217.9838, 2604.77],
    # [-2676.715, 185.073, 2402.609],

    # [-2476.52, 287.5917, 1809.22], #Cave_GerudoHighlands_0002
    [-2457.328, 281.7868, 1798.546],

    # [-4384.535, 584.2957, 536.5526], #Cave_GerudoHighlands_0008
    [-4384.535, 579.2957, 536.5526],

    # [-3982.832, 542.1691, 1245.38], #Cave_GerudoHighlands_0014
    [-3982.832, 532.1691, 1245.38],

    # [-3881.652, 681.944, 726.7761], #Cave_GerudoHighlands_0017
    [-3881.652, 675.3375, 726.7761],

    # [3235.51, 177.44, 3017.51], #Cave_HateruEast_0000
    # [3291.834, 174, 3332.983],
    [3224.249, 164.9509, 3017.773],
    # [3291.353, 170.0782, 3296.459],

    # [1788.839, 194.6686, 3012], #Cave_HateruEast_0002
    # [1959.679, 181.6188, 2611.651],
    [1959.679, 176.6188, 2611.651],
    # [1789.542, 185.8739, 2985.635],

    # [1676.795, 274.8358, 3038.773], #Cave_HateruEast_0006
    [1676.795, 269.8358, 3038.773],

    # [1896.399, 265.528, 3111.244], #Cave_HateruEast_0007
    [1896.399, 237.528, 3111.244],

    # [1958.782, 314.8886, 3032.786], #Cave_HateruEast_0008
    # [2009.624, 288.4404, 3164.034],
    [1958.782, 298.3886, 3032.786],
    # [2009.624, 282.4404, 3164.034],

    # [1813.53, 229, 3738.02], #Cave_HateruEast_0009
    [1813.53, 224, 3738.02],

    # [4752.63, 121.7059, 3781.506], #Cave_HateruEast_0013
    [4752.63, 99.20595, 3781.506],

    # [1446.719, 184.7728, 3483.647], #Cave_HateruEast_0014
    [1446.719, 182.7728, 3483.65],

    # [2454, 175, 3193], #Cave_HateruEast_0016
    [2454, 170, 3193],

    # [1611.714, 128.7817, 804], #Cave_HateruWest_0002
    # [1617, 142.2283, 1260],
    [1617, 112.4627, 1260],
    # [1587.754, 111.5236, 812.1858],

    # [1947.489, 265.4827, 981.817], #Cave_HateruWest_0005
    [1947.489, 262.9827, 981.817],

    # [1877.434, 309.0427, 1160.383], #Cave_HateruWest_0006
    [1877.434, 304.0427, 1160.383],

    # [1328.358, 244.9518, 1156.223], #Cave_HateruWest_0008
    # [1373.024, 240.2808, 1197.249],
    [1373.024, 235.2808, 1197.249],
    # [1328.358, 239.9518, 1156.223],

    # [1194.246, 268.427, 1853.947], #Cave_HateruWest_0011
    [1194.457, 263.4327, 1854.056],

    # [1183.372, 356, 1947.553], #Cave_HateruWest_0012
    [1183.372, 351, 1947.553],

    # [-4041.161, 135.7831, -2671.444], #Cave_Hebra_0000
    [-4041.161, 128.7831, -2671.444],

    # [-4429.344, 333.8416, -3760.204], #Cave_Hebra_0013
    [-4429.344, 328.8416, -3760.204],

    # [-3932, 94.24, -2853.611], #Cave_Hebra_0015
    [-3930.992, 87.47372, -2861.257],

    # [-2900.156, 500.4017, -2510.26], #Cave_Hebra_0016
    [-2900.156, 493.4017, -2510.26],

    # [-2414.122, 485.1641, -3136.461], #Cave_Hebra_0019
    # [-2642.285, 361.5, -3268.3],
    [-2642.285, 354.5, -3268.3],
    # [-2414.122, 478.1641, -3136.461],

    # [-3814.609, 368.5, -3595.483], #Cave_Hebra_0021
    [-3814.609, 360.5, -3595.483],

    # [-3010.71, 673, -3216.431], #Cave_Hebra_0022
    [-2995.566, 645.4677, -3225.751],

    # [-3005.719, 311.8382, -1635.029], #Cave_Hebra_0023
    [-3005.719, 304.8382, -1635.029],

    # [-3571.5, 337.7415, -2475], #Cave_Hebra_0025
    [-3559.555, 332.716, -2488.378],

    # [-3214.608, 456.0323, -2462.24], #Cave_Hebra_0026
    [-3214.608, 451.0323, -2462.24],

    # [-3227.5, 551.66, -2535.71], #Cave_Hebra_0030
    # [-3398.434, 423.3941, -2499.361],
    [-3398.434, 418.6059, -2499.361],
    # [-3227.496, 547.1563, -2535.279],

    # [-2840.931, 334.4799, -1771.911], #Cave_Hebra_0035
    [-2840.931, 328.4799, -1771.911],

    # [-1372.09, 308.2222, -2861.308], #Cave_Hebra_0036
    [-1372.09, 303.2222, -2861.308],

    # [-2395.838, 283, -2276.628], #Cave_Hebra_0037
    [-2395.838, 275, -2276.628],

    # [-3958.686, 311.0806, -2029.48], #Cave_Hebra_0039
    [-3958.686, 306.0806, -2029.48],

    # [-3960.082, 349.4887, -3245.218], #Cave_Hebra_0040
    [-3960.082, 342.4887, -3245.218],

    # [-3555.201, 383.8807, -3088.22], #Cave_Hebra_0041
    # [-3978.405, 252, -3069.581],
    [-3555.201, 378.8807, -3088.22],
    # [-3989.371, 243.8339, -3062.853],

    # [676.4661, 156.6693, -1389.783], #Cave_HyruleForest_0001
    [676.4661, 150.6693, -1389.783],

    # [1244.07, 135.27, -1226.72], #Cave_HyruleForest_0006
    [1247.259, 131.0546, -1231.93],

    # [-643.5, 265, -2040], #Cave_HyruleForest_0007
    [-643.5, 260, -2040],

    # [307.1301, 199, -3579.347], #Cave_HyruleForest_0008
    [307.1301, 193, -3579.347],

    # [-1188.387, 181.3508, -644.5137], #Cave_HyruleRidge_0000
    # [-1234.645, 199.9723, -770],
    [-1234.178, 182.9717, -770.2173],
    # [-1188.387, 177.8508, -644.5137],

    # [-2921.855, 119.0728, 804.1642], #Cave_HyruleRidge_0002
    [-2921.855, 113.0728, 804.1642],

    # [-1730.5, 340.5, -1158], #Cave_HyruleRidge_0003
    [-1734.927, 334.1996, -1165.696],

    # [-2196.346, 229.6, 815.1], #Cave_HyruleRidge_0005
    [-2198.541, 222.7959, 807.5707],

    # [-2268.351, 201.6453, -899.2295], #Cave_HyruleRidge_0006
    [-2268.351, 191.6453, -899.2295],

    # [-2049.127, 55.87498, -1631.707], #Cave_HyruleRidge_0007
    [-2049.127, 48.87498, -1631.707],

    # [-2151.008, 386.5, 360.521], #Cave_HyruleRidge_0008
    [-2151.008, 381.5, 360.521],

    # [1144.714, 169.0162, -247.4642], #Cave_Lanayru_0006
    # [1349.549, 140.3217, -296.4998],
    [1144.714, 163.0162, -247.4642],
    # [1349.549, 134.3217, -296.4998],

    # [3094.097, 189.5792, 51.30798], #Cave_Lanayru_0008
    [3094.097, 184.5792, 51.30798],

    # [2909.617, 192.4868, 65.92992], #Cave_Lanayru_0014
    [2909.617, 187.4868, 65.92992],

    # [2601.823, 190.6994, -225.8443], #Cave_Lanayru_0019
    # [2674.985, 199.7526, -287.4286],
    # [2691.49, 212, -214.2797],
    [2674.985, 194.7526, -287.4286],
    # [2605.527, 181.4956, -227.0979],
    # [2679.644, 198.03, -217.6957],

    # [2185.078, 147.8939, -142.0787], #Cave_Lanayru_0024
    # [2215.354, 181.0875, -100.1791],
    # [2253.844, 126.6181, -14.21026],
    # [2254.5, 236.2, -98.5],
    [2185.078, 142.8939, -142.0787],
    # [2253.844, 121.6181, -14.21026],
    # [2215.354, 177.0875, -100.1791],
    # [2260.729, 216.0839, -108.3997],

    # [2570.025, 274.5424, -517.9893], #Cave_Lanayru_0032
    # [2633.5, 309.1393, -525.6262],
    [2570.025, 269.5424, -517.9893],
    # [2633.568, 294.1987, -526.1559],

    # [2700.302, 315.4945, -479.8156], #Cave_Lanayru_0033
    # [2863.632, 339.7472, -346.3295],
    [2863.632, 332.7472, -346.3295],
    # [2700.302, 307.4945, -479.8156],

    # [4243.966, 99.10972, 255.6655], #Cave_Lanayru_0035
    [4243.966, 89.10972, 255.6655],

    # [4473.68, 150.3593, 832.2194], #Cave_Lanayru_0036
    [4473.05, 137.0549, 826.9572],

    # [2912.125, 273.1285, -170.1434], #Cave_Lanayru_0048
    # [2958.832, 313.0372, -253.8851],
    [2958.832, 308.0372, -253.8851],
    # [2912.125, 263.1285, -170.1434],

    # [2849.799, 439.877, -478.9477], #Cave_Lanayru_0049
    [2850.636, 429.9589, -477.983],

    # [493.7314, 150, -730.937], #Cave_Lanayru_0052
    [493.7314, 146, -730.937],

    # [845.9233, 125.8293, -31.49684], #Cave_Lanayru_0053
    [845.9233, 121.3293, -31.49684],

    # [3809.582, 321.4452, -419.5987], #Cave_Lanayru_0055
    [3809.582, 314.4452, -419.5987],

    # [3660.875, 385.0333, -538.5847], #Cave_Lanayru_0057
    [3660.896, 374.0333, -538.5865],

    # [3147.392, 287.5269, -667.6096], #Cave_Lanayru_0060
    [3147.392, 282.5269, -667.6096],

    # [3240.992, 186.4779, -373.5201], #Cave_Lanayru_0061
    [3240.992, 181.4779, -373.5201],

    # [2698.728, 225.9755, 1292.447], #Cave_LanayruMountain_0002
    [2698.274, 216.7247, 1314.642],

    # [4585.332, 109.5976, 2246.283], #Cave_LanayruMountain_0006
    [4585.332, 103.5976, 2246.283],

    # [2504.104, 123.9471, 2106.521], #Cave_LanayruMountain_0008
    [2504.104, 111.9471, 2106.521],

    # [3074.555, 207.2067, 1138.09], #Cave_LanayruMountain_0010
    # [3476.452, 127.4407, 968.3922],
    [3073.536, 197.2633, 1137.785],
    # [3476.452, 97.4407, 968.3922],

    # [2492.99, 122.5274, 1477.647], #Cave_LanayruMountain_0014
    [2492.99, 117.5274, 1477.647],

    # [3933.575, 237.9416, 2069.003], #Cave_LanayruMountain_0016
    # [4225.536, 305.5, 1738.955],
    [4225.536, 285.5, 1738.955],
    # [3933.575, 232.9416, 2069.003],

    # [4207.23, 109.01, 2287.35], #Cave_LanayruMountain_0022
    [4213.486, 105.6649, 2262.576],

    # [3650.401, 111.8049, 3210.815], #Cave_LanayruMountain_0024
    [3650.401, 99.30487, 3210.815],

    # [3748.875, 300.5, 2026.508], #Cave_LanayruMountain_0025
    # [3757.448, 322.2258, 2066.606],
    [3757.448, 319.7258, 2066.606],
    # [3748.875, 295.5, 2026.508],

    # [2243.432, 134, 1689.599], #Cave_LanayruMountain_0026
    [2243.432, 129, 1689.599],

    # [-3865.5, 188, -1011.5], #Cave_Tabantha_0001
    #[-3931.099, 188.3087, -1090.969],
    [-3865.5, 178, -1011.5],
    # [-3931.099, 178.3087, -1090.969],

    # [-3465.121, 369.5734, -449.4601], #Cave_Tabantha_0002
    [-3465.121, 359.5734, -449.4601],

    # [-3308.472, 13.62203, -789.7637] #Cave_Tabantha_0003
    [-3308.472, 3.622033, -789.7637],

    # [486.9327, 117.2137, 3831.136] ,#Well_0043B
    [486.9327, 113.2137, 3831.136],
    [3622.3269, 275.002686, -583.486023],  # Zora_Imperial_Palace
    [3606.64111, 103, -122.3]  # ZoraZonauTerminal

]


##aftewr bunch of nonsence I realized that all you have to do in this context is just floor the numbers, fuck floating points
def better_round(num):
    return np.floor(num)


## difference from save editors:
##zelda dungeon and in game x y z
##save editor x z+105 -y
##layer 0: surface, 1 sky, -1 depths


def find_hash(x, y, z, hashes, coords):
    [a, b, c] = [better_round(x), better_round(-y), better_round(z)]
    coords_floored = [[better_round(x), better_round(y), better_round(z)] for [x, y, z] in coords]
    index = coords_floored.index([a, c + 105, b])
    return hashes[index]


if __name__ == '__main__':
    print(len(CHASM))
    print(len(CHASM_STATUS))
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='json file to convert')
    parser.add_argument('layer', help='layer')
    parser.add_argument('object', help='hashes')
    args = parser.parse_args()
    layer = args.layer
    object = args.object
    # find all json files in raw-data directory
    json_file = args.file
    # make sure the file exists and is a json
    if not os.path.exists(json_file):
        print(f'File {json_file} does not exist')
        exit(1)
    if not json_file.endswith('.json'):
        print(f'File {json_file} is not a json')
        exit(1)
    # load the json file
    with open(json_file, 'r') as f:
        data = json.load(f)
        # open another file to write to
        with open(f'{json_file[:-5]}_{layer}_converted.txt', 'w') as f2:
            for item in data:
                if re.search(r"\d{5,}", item['id']):
                    continue
                if item['id'] == 'Zora_Imperial_Palace':
                    continue
                name = item['name']
                x = float(item['x'])
                y = float(item['y'])
                z = float(item['z'])

                command = f'find_hash(x, y, z,{str.upper(object)}_STATUS,{str.upper(object)})'
                hash = eval(command)
                code = f'Data::{object}({hash}, "{name}", {x}f, {y}f,{z}f, {layer}),\n'
                # write to file
                f2.write(code)
            # close file
            f2.close()
