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

# bad
ASSASSIN = 'assassin'
MORDRED = 'mordred'
MORGANA = 'morgana'
MAELAGANT = 'maelagant'
COLGREVANCE = 'colgrevance'
BAD_ROLES = (ASSASSIN, MORDRED, MAELAGANT, MORGANA, COLGREVANCE)

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

def start_game(players, settings):
    """Starts the game
    
    Args:
        players (list): list of players name (strings)
        settings (dict): contains roles and percentages
        
    Returns:
        dictionary: contains players with their roles, teams, and if assasin
    
    """
    # make sure order of players is shuffled
    shuffle(players)
    settings = json.loads(settings)
    good_chances = {}
    bad_chances = {}
    good_start = 0
    bad_start = 0
    # create role chances from settings
    for role, chance in settings.items():
        # assasin is not a role assigned
        if role.lower() == 'assassin': continue
        if int(chance) == 0: continue
        chance = int(chance)
        if role.lower() in GOOD_ROLES:
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
            good_start, good_chances, roles = get_individual_role(good_start, good_chances, roles, player)
        else:
            # bad role
            bad_start, bad_chances, roles = get_individual_role(bad_start, bad_chances, roles, player)
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
                    
def get_individual_role(start, chances, roles, player):
    """Randomly assigns a role to a player
    
    Args:
        start (int): range of numbers
        chances (list): each index is a tuple of indexes (#, #)
                        which represent a range
        roles (dict): contains players and their role information to be changed
        
    Returns:
        tuple: contains the adjusted start, chances, and roles args
        
    """
    # randint is inclusive of 0 and start
    # 'in range' is not inclusive of far end, so we need to add 1
    while True:
        ran_num = randint(0, start)
        for role in chances:
            if ran_num in range(int(chances[role][0]), int(chances[role][1]) + 1):
                roles[player][1] = role
                del chances[role]
                return start, chances, roles
            
    