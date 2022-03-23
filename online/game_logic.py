"""Helper for generating certain roles for a game.
Utilizes the percent likely to randomize role inclusion
and assigning.

Follows several rules-

1. Assassinable roles in game must be between min and max given
2. If a lover exists, then both lovers must exist
3. Must have appropiate number of spies in each game depending on user count
4. Assassin must be assigned to a spy if determiend to exist, calculated based on likelyhood given

"""

from random import randint, shuffle
import json
# randint is inclusive on both ends

# good
JESTER = 'jester'
MERLIN = 'merlin'
PUCK = 'puck'
LANCELOT = 'lancelot'
UTHER = 'uther'
TRISTAN = 'tristan'
ISEULT = 'iseult'
PERCIVAL = 'percival'
GUINEVERE = 'guinevere'
ARTHUR = 'arthur'
GOOD_ROLES = (PERCIVAL, JESTER, GUINEVERE, MERLIN, PUCK, LANCELOT, UTHER, TRISTAN, ISEULT, ARTHUR)
ASSASSINABLE_ROLES = (ISEULT, TRISTAN, ISEULT, MERLIN, ARTHUR)

# bad
ASSASSIN = 'assassin'
MORDRED = 'mordred'
MORGANA = 'morgana'
MAELAGANT = 'maelagant'
COLGREVANCE = 'colgrevance'
BAD_ROLES = (ASSASSIN, MORDRED, MAELAGANT, MORGANA, COLGREVANCE)

ALL_ROLES = GOOD_ROLES + BAD_ROLES

MIN_ASSASSIN = 'min_assassinable_roles'
MAX_ASSASSIN = 'max_assassinable_roles'

"""
JESTER, \
MERLIN, \
PUCK, \
LANCELOT, \
UTHER, \
TRISTAN, \
ISEULT, \
ARTHUR, \
ASSASSIN, \
MORDRED, \
GUINEVERE, \
MORGANA, \
MAELAGANT, \
COLGREVANCE
"""

def create_game_logic(players: list, settings: dict) -> dict:
    """Starts the game
    
    Args:
        players (list): list of players name (strings)
        settings (dict): contains roles and percentages
        
    Returns:
        dict: contains players with their roles, teams, and if assasin
    
    """
    # make sure order of players is shuffled
    shuffle(players)
    settings = json.loads(settings)
    # half the chances of each since getting one assigns both
    settings[ISEULT] = int(settings[ISEULT]) / 2
    settings[TRISTAN] = int(settings[TRISTAN]) / 2
    assassinable_range = (int(settings[MIN_ASSASSIN]), int(settings[MAX_ASSASSIN]))
    good_chances = {}
    bad_chances = {}
    good_start = 0
    bad_start = 0
    # create role chances from settings
    for role, chance in settings.items():
        role = role.lower()
        # assasin is not a role assigned
        if role == ASSASSIN or role == MIN_ASSASSIN or role == MAX_ASSASSIN:
            continue
        if int(chance) == 0:
            continue
        chance = int(chance)
        if role in GOOD_ROLES:
            good_chances[role] = (good_start, good_start + chance-1)
            good_start += chance
        elif role.lower() in BAD_ROLES:
            bad_chances[role] = (bad_start, bad_start + chance-1)
            bad_start += chance
        else:
            print(role)
            raise Exception
    roles = {} # in format {player: (good/bad, role, assasing/not assasin)}
    # determine number of spies
    if len(players) < 7:
        num_bad = 2
    elif len(players) < 9:
        num_bad = 3
    else:
        num_bad = 4
    ran_num = set()
    if (len(players) - num_bad) > len(good_chances):
        print('not enough good roles')
        return False
    # generate indexes of the spies/bad players
    while len(ran_num) < num_bad:
        ran_num.add(randint(0, len(players) - 1))
    # assign a team to each player
    for index, player in enumerate(players):
        if index in ran_num:
            # bad role
            roles[player] = [True, '', False]
        else:
            # good role
            roles[player] = [False, '', False]
    # assign a role to each player
    for player in roles:
        if roles[player][0] is False:
            # good role
            # check if player was already assigned as lover
            if roles[player][1] != '':
                continue
            good_start, good_chances, roles = get_individual_role(good_start, good_chances, roles, player)
        else:
            # bad role
            bad_start, bad_chances, roles = get_individual_role(bad_start, bad_chances, roles, player)
    # after assiging roles, verify we have correct # of assassinable roles
    roles = adjust_assassinable_roles(good_start, good_chances, roles, assassinable_range)
    # determine if assassin exists and assign to one spy
    # randint is inclusive of 0 and 100
    # 'in range' is not inclusive of far end, so we need to add 1
    if randint(0, 100) in range(int(settings[ASSASSIN]) + 1):
        spy_index = randint(0, num_bad - 1)
        count = 0
        for player in roles:
            if roles[player][0] is True:
                if spy_index == count:
                    roles[player][2] = True
                    break
                else:
                    count += 1
    return roles
                    
def get_individual_role(start: int, chances: list, roles: dict, player: str) -> tuple:
    """Randomly assigns a role to a player
    
    Args:
        start (int): max range of chances index
        chances (list): each value is a tuple of indexes (#, #)
                        which represent a range for a role
        roles (dict): contains players and their role information to be changed
        player (str): player name to assign a role to
        
    Returns:
        tuple: contains the adjusted start, chances, and roles args
        
    """
    # randint is inclusive of 0 and start
    # 'in range' is not inclusive of far end, so we need to add 1
    for _ in range(100000):
        ran_num = randint(0, start)
        for role in chances:
            if ran_num in range(int(chances[role][0]), int(chances[role][1]) + 1):
                roles[player][1] = role
                if role == TRISTAN or role == ISEULT:
                    # if we received a lover role, assign the other lover
                    chances, roles = assign_lovers(chances, roles, role)
                del chances[role]
                return start, chances, roles
    raise Exception("Role could not be assigned in get_individual_roles")
            
def assign_lovers(good_chances: dict, roles: dict, lover_role: str) -> dict:
    """Assigns lovers to 2 players, overwrites role if needed.
    
    Args:
        good_chances (dict): each value is a tuple of indexes (#, #)
                        which represent a range for a role
        roles (dict): dictionary of players and their role info
        lover_role (str): either ISEULT or TRISTAN
        
    Returns:
        dict: updated roles
        
    """
    # shuffle the roles so other lover is completely random
    roles = list(roles.items())
    shuffle(roles)
    roles = dict(roles)
    if lover_role == TRISTAN:
        other_lover = ISEULT
    else:
        other_lover = TRISTAN
    for player in roles:
        if roles[player][0] is False and roles[player][1] == '':
            roles[player][1] = other_lover
            del good_chances[other_lover]
            return good_chances, roles
    for player in roles:
        if roles[player][0] is False and roles[player][1] != lover_role:
            roles[player][1] = other_lover
            del good_chances[other_lover]
            return good_chances, roles
    
def adjust_assassinable_roles(start: int, chances: dict, roles: dict, assassinable_range: tuple) -> dict:
    """Verifies the minimum and maximum num of assassinable roles are met.
    Removes or adds an assinable role if criteria not met.
    
    Args:
        start (int): max range of choice index
        chances (dict): each value is a tuple of indexes (#, #)
                        which represent a range for a role
        roles (dict): dictionary of players and their role info
        assassinable_range (tuple): (min # assassinable, max # assassinable)
    
    Returns:
        dict: updated roles
    """
    # shuffle the roles
    roles = list(roles.items())
    shuffle(roles)
    roles = dict(roles)
    num_assassinable = 0
    for player in roles:
        if roles[player][1] in ASSASSINABLE_ROLES:
            num_assassinable += 1
    if num_assassinable <= assassinable_range[1] and num_assassinable >= assassinable_range[0]:
        return roles
    elif num_assassinable > assassinable_range[1]:
        # remove an assassinable role
        while num_assassinable > assassinable_range[1]:
            pass
    elif num_assassinable < assassinable_range[0]:
        # add an assassinable role
        while num_assassinable < assassinable_range[0]:
            new_chance = {}
            for chance in chances:
                if chance in ASSASSINABLE_ROLES:
                    new_chance[chance] = chances[chance]
            for player in roles:
                if roles[player][0] is False and roles[player][1] == '':
                    start, chances, roles = get_individual_role(start, new_chance, roles, player)
    return roles