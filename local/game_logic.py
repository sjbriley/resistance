# good
JESTER = 'jester'
MERLIN = 'merlin'
PUCK = 'puck'
LANCELOT = 'lancelot'
UTHER = 'uther'
TRISTAN = 'tristan'
ISEULT = 'iseult'
ARTHUR = 'arthur'

# bad
ASSASSIN = 'assasin'
MORDRED = 'mordred'
GUINEVERE = 'guinevere'
MORGANA = 'morgana'
MAELAGANT = 'maelagant'
COLGREVANCE = 'colgrevance'

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


def start_game(numPlayers, players, settings):
    """Returns a dictionary of players and their respective roles and knowledge in a list
    Parameters:
        numPlayers (int)
        players (list of strings): list of players
        settings: a dictionary of roles that are on/off
    Returns:
        info (dictionary): where key is username from players
                           and value is in form ['role': 'knowledge from role', 'assasin True/False']
        """
    info = {}
    for count, user in enumerate(players):
        if count==0:
            info[user] = ['jester', '', False]
        if count==1:
            info[user] = ['mordred', '', True]
        if count ==2:
            info[user] = ['uther', 'tergnerg', False]
    return user