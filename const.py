### Game State Actions ###
CARD_AWARDED = 2  # card awarded (who, territory, symbol) (3 positions)
BATTLE_RESULT = 3  # battle result (attacking_territory, defending_territory, attacking_dead, defending_dead, a1, a2, a3, d1, d2)
MOVE_RESULT_BATTLE = 4  # move result (battle) (x_remain, x_move_to_territory)
MOVE_RESULT_REINFORCE = 5  # move result (reenforce) (from_territory, to_territory, number)
PLACE_ARMIES = 6  # place armies (number placed, (location, amouont) * for_each)
CARDS_PLAYED = 7  # cards played (amount increased)
GENERATE_ARMIES = 8  # Generate armies (amount increased)
ATTACK_ENDED = 9  # ended attack (from_territory, to_territory)
NEXT_TURN = 10  # New player
NEW_GAME = 11  # New Game  - (your player number)

# State Types
PLAYER_STATE = 2
GAME_STATE = 3

# Game constants
TOTAL_LOCATIONS = 48

# Status Constants
SUCCESS = 4
INVALID_MOVE = 5

# Player Actions
CREATE_GAME = 12
ADD_PLAYER = 13

# Player Colours
PLAYER_COLOURS = [
    (0, 86, 163),
    (6, 151, 66),
    (176, 42, 33),
    (102, 86, 145),
    (99, 75, 68),
    (156, 146, 3)
]

PLAYER_COLOUR_NAMES = [
    'Blue',
    'Green',
    'Red',
    'Purple',
    'Brown',
    'Yellow'
]

# Colours
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 0
RED = 255, 0, 0

# Territory Info
TERRITORIES = [
    {'name': 'Skagos', 'region': 0, 'castle': False, 'port': False, 'card': 'knight', 'neighbours': [1, 2]},  # 0
    {'name': 'The Gift', 'region': 0, 'castle': False, 'port': False, 'card': 'castle', 'neighbours': [0, 2, 4, 3]},  # 1
    {'name': 'Karhold', 'region': 0, 'castle': False, 'port': False, 'card': 'catapult', 'neighbours': [0, 1, 4]},  # 2
    {'name': 'Winterfell', 'region': 0, 'castle': True, 'port': False, 'card': 'knight', 'neighbours': [1, 4, 5, 6, 9, 8, 7]},  # 3
    {'name': 'The Dreadfort', 'region': 0, 'castle': True, 'port': False, 'card': 'castle', 'neighbours': [2, 1, 3, 5]},  # 4
    {'name': 'Widow\'s Watch', 'region': 0, 'castle': False, 'port': True, 'card': 'catapult', 'neighbours': [4, 3, 47, 34, 26, 25, 16, 6]},  # 5
    {'name': 'White Harbour', 'region': 0, 'castle': False, 'port': True, 'card': 'knight', 'neighbours': [3, 9, 11, 47, 34, 26, 25, 16, 5]},  # 6
    {'name': 'Bear Island', 'region': 0, 'castle': False, 'port': False, 'card': 'castle', 'neighbours': [10, 9, 3]},  # 7
    {'name': 'Wolfswood', 'region': 0, 'castle': False, 'port': True, 'card': 'catapult', 'neighbours': [10, 9, 7, 3, 41, 30, 23, 22, 18, 12]},  # 8
    {'name': 'Barrowlands', 'region': 0, 'castle': True, 'port': False, 'card': 'knight', 'neighbours': [11, 6, 3, 8, 10]},  # 9
    {'name': 'Stoney Shore', 'region': 0, 'castle': False, 'port': False, 'card': 'catapult', 'neighbours': [9, 8, 7]},  # 10
    {'name': 'The Neck', 'region': 0, 'castle': False, 'port': False, 'card': 'castle', 'neighbours': [9, 6, 12, 14, 23, 17]},  # 11
    {'name': 'Cape Kraken', 'region': 0, 'castle': False, 'port': True, 'card': 'knight', 'neighbours': [11, 41, 30, 23, 22, 18, 8]},  # 12
    {'name': 'The Fingers', 'region': 1, 'castle': False, 'port': False, 'card': 'catapult', 'neighbours': [14]},  # 13
    {'name': 'Mountains of the Moon', 'region': 1, 'castle': False, 'port': False, 'card': 'castle', 'neighbours': [13, 11, 17, 18, 20, 15]},  # 14
    {'name': 'The Eyrie', 'region': 1, 'castle': True, 'port': False, 'card': 'knight', 'neighbours': [14, 16]},  # 15
    {'name': 'Gulltown', 'region': 1, 'castle': False, 'port': True, 'card': 'catapult', 'neighbours': [15, 47, 34, 26, 25, 5, 6]},  # 16
    {'name': 'The Twins', 'region': 2, 'castle': True, 'port': False, 'card': 'castle', 'neighbours': [11, 14, 18, 23]},  # 17
    {'name': 'The Trident', 'region': 2, 'castle': False, 'port': True, 'card': 'knight', 'neighbours': [14, 17, 19, 20, 41, 30, 23, 22, 12, 8]},  # 18
    {'name': 'Riverrun', 'region': 2, 'castle': True, 'port': False, 'card': 'catapult', 'neighbours': [18, 20, 21, 22, 28, 29]},  # 19
    {'name': 'Harrenhal', 'region': 2, 'castle': True, 'port': False, 'card': 'castle', 'neighbours': [14, 18, 19, 21, 25, 37]},  # 20
    {'name': 'Stoney Sept', 'region': 2, 'castle': False, 'port': False, 'card': 'knight', 'neighbours': [19, 20, 37, 29, 30, 32]},  # 21
    {'name': 'Pyke', 'region': 3, 'castle': True, 'port': True, 'card': 'catapult', 'neighbours': [28, 19, 41, 30, 23, 18, 12, 8]},  # 22
    {'name': 'Harlow', 'region': 3, 'castle': False, 'port': True, 'card': 'castle', 'neighbours': [17, 11, 41, 30, 22, 18, 12, 8]},  # 23
    {'name': 'Crackclaw Point', 'region': 4, 'castle': False, 'port': False, 'card': 'catapult', 'neighbours': [25, 26]},  # 24
    {'name': 'King\'s Landing', 'region': 4, 'castle': True, 'port': True, 'card': 'knight', 'neighbours': [24, 20, 37, 27, 47, 34, 26, 16, 5, 6]},  # 25
    {'name': 'Dragonstone', 'region': 4, 'castle': True, 'port': True, 'card': 'castle', 'neighbours': [24, 27, 47, 34, 25, 16, 5, 6]},  # 26
    {'name': 'Kingswood', 'region': 4, 'castle': False, 'port': False, 'card': 'knight', 'neighbours': [25, 26, 37, 38, 34]},  # 27
    {'name': 'The Crag', 'region': 5, 'castle': False, 'port': False, 'card': 'catapult', 'neighbours': [19, 22, 29, 30]},  # 28
    {'name': 'Golden Tooth', 'region': 5, 'castle': False, 'port': False, 'card': 'castle', 'neighbours': [19, 21, 28, 30]},  # 29
    {'name': 'Casterly Rock', 'region': 5, 'castle': True, 'port': True, 'card': 'knight', 'neighbours': [21, 28, 29, 31, 32, 41, 23, 22, 18, 12, 8]},  # 30
    {'name': 'Crakehall', 'region': 5, 'castle': True, 'port': False, 'card': 'catapult', 'neighbours': [30, 32, 39]},  # 31
    {'name': 'Silverhill', 'region': 5, 'castle': False, 'port': False, 'card': 'knight', 'neighbours': [21, 30, 31, 37, 39]},  # 32
    {'name': 'Tarth', 'region': 6, 'castle': False, 'port': False, 'card': 'castle', 'neighbours': [34, 36]},  # 33
    {'name': 'Storm\'s End', 'region': 6, 'castle': True, 'port': True, 'card': 'catapult', 'neighbours': [27, 38, 33, 35, 36, 47, 26, 25, 16, 5, 6]},  # 34
    {'name': 'Dornish Marches', 'region': 6, 'castle': True, 'port': False, 'card': 'knight', 'neighbours': [38, 40, 44, 34, 36]},  # 35
    {'name': 'Rainwood', 'region': 6, 'castle': False, 'port': False, 'card': 'castle', 'neighbours': [33, 34, 35]},  # 36
    {'name': 'Blackwater Rush', 'region': 7, 'castle': False, 'port': False, 'card': 'catapult', 'neighbours': [20, 21, 32, 25, 27, 38, 39, 40]},  # 37
    {'name': 'The Mander', 'region': 7, 'castle': True, 'port': False, 'card': 'castle', 'neighbours': [37, 40, 27, 34, 35]},  # 38
    {'name': 'Searoad Marshes', 'region': 7, 'castle': False, 'port': False, 'card': 'knight', 'neighbours': [31, 32, 37, 40]},  # 39
    {'name': 'Highgarden', 'region': 7, 'castle': True, 'port': False, 'card': 'catapult', 'neighbours': [37, 38, 39, 41, 42, 35, 44]},  # 40
    {'name': 'Oldtown', 'region': 7, 'castle': True, 'port': True, 'card': 'castle', 'neighbours': [40, 42, 43, 30, 23, 22, 18, 12, 8]},  # 41
    {'name': 'Three Towers', 'region': 7, 'castle': False, 'port': False, 'card': 'knight', 'neighbours': [40, 41, 43, 44]},  # 42
    {'name': 'The Arbor', 'region': 7, 'castle': False, 'port': False, 'card': 'catapult', 'neighbours': [41, 42]},  # 43
    {'name': 'Red Mountains', 'region': 8, 'castle': False, 'port': False, 'card': 'castle', 'neighbours': [35, 40, 42, 45, 46]},  # 44
    {'name': 'Sandstone', 'region': 8, 'castle': True, 'port': False, 'card': 'knight', 'neighbours': [44, 46]},  # 45
    {'name': 'Greenblood', 'region': 8, 'castle': False, 'port': False, 'card': 'catapult', 'neighbours': [44, 45, 47]},  # 46
    {'name': 'Sunspear', 'region': 8, 'castle': False, 'port': True, 'card': 'castle', 'neighbours': [46, 34, 26, 25, 16, 5, 6]},  # 47
]

# Region Info
REGIONS = [
    {'name': 'The North', 'bonus': 5, 'territories': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]},
    {'name': 'The Vale or Arryn', 'bonus': 1, 'territories': [13, 14, 15, 16]},
    {'name': 'The Riverlands', 'bonus': 2, 'territories': [17, 18, 19, 20, 21]},
    {'name': 'The Iron Islands', 'bonus': 1, 'territories': [22, 23]},
    {'name': 'The Crownlands', 'bonus': 2, 'territories': [24, 25, 26, 27]},
    {'name': 'The Westerlands', 'bonus': 2, 'territories': [28, 29, 30, 31, 32]},
    {'name': 'The Stormlands', 'bonus': 1, 'territories': [33, 34, 35, 36]},
    {'name': 'The Reach', 'bonus': 4, 'territories': [37, 38, 39, 40, 41, 42, 43]},
    {'name': 'Dorne', 'bonus': 1, 'territories': [44, 45, 46, 47]},
]


