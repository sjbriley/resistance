from django.test import TestCase
from .. import game_logic
import json

class GameLogic(TestCase):
    
    def test_randomness(self):
        """Test the randomness of team generation"""
        players = ['sam', 'joe', 'bob', 'matt', 'joey']
        settings = {}
        for role in game_logic.GOOD_ROLES:
            settings[role] = '100'
        for role in game_logic.BAD_ROLES:
            settings[role] = '100'
        settings = json.dumps(settings)
        log = {}
        for player in players:
            log[player] = 0
        for _ in range(10000):
            results = game_logic.start_game(players, settings)
            for player in results:
                if results[player][0] is True:
                    log[player] += 1
        for player in log:
            # assert randomness +- 5%, expected 40%
            self.assertGreater(float(log[player]/10000), 0.35)
            self.assertLess(float(log[player]/10000), 0.45)

            
    def test_5_players(self):
        """Test team generation of 5 players with an assassin"""
        players = ['sam', 'joe', 'bob', 'matt', 'joey']
        settings = {}
        for role in game_logic.GOOD_ROLES:
            settings[role] = '100'
        for role in game_logic.BAD_ROLES:
            settings[role] = '100'
        settings = json.dumps(settings)
        results = game_logic.start_game(players, settings)
        # assert the correct # of good/bad roles as well as only 1 assassin
        good = 0
        bad = 0
        assassin = 0
        for player in results:
            if results[player][0] is True:
                bad += 1
            else:
                good += 1
            if results[player][2] is True:
                assassin += 1
        self.assertEqual(bad, 2)
        self.assertEqual(good, 3)
        self.assertEqual(assassin, 1)
    
    def test_10_players(self):
        """Checks team generation of 10 players with no assassin"""
        players = ['sam', 'joe', 'bob', 'matt', 'joey',
                   'tyler', 'billy', 'niels', 'bob2', 'frankie']
        settings = {}
        for role in game_logic.GOOD_ROLES:
            settings[role] = '100'
        for role in game_logic.BAD_ROLES:
            settings[role] = '100'
        settings[game_logic.ASSASSIN] = '0'
        settings = json.dumps(settings)
        results = game_logic.start_game(players, settings)
        # assert the correct # of good/bad roles as well as only 1 assassin
        good = 0
        bad = 0
        assassin = 0
        for player in results:
            if results[player][0] is True:
                bad += 1
            else:
                good += 1
            if results[player][2] is True:
                assassin += 1
        self.assertEqual(bad, 4)
        self.assertEqual(good, 6)
        self.assertEqual(assassin, 0)
        
    def test_assassin_randomness(self):
        """Verifies assassin chance is appropiate and randomly assigned"""
        players = ['sam', 'joe', 'bob', 'matt', 'joey']
        settings = {}
        for role in game_logic.GOOD_ROLES:
            settings[role] = '100'
        for role in game_logic.BAD_ROLES:
            settings[role] = '100'
        # 75% chance assassin exists
        settings[game_logic.ASSASSIN] = '75'
        settings = json.dumps(settings)
        # assert the correct # of good/bad roles as well as only 1 assassin
        log = {}
        total_assassin = 0
        for player in players:
            log[player] = 0
        for _ in range(10000):
            results = game_logic.start_game(players, settings)
            for player in results:
                if results[player][2] is True:
                    log[player] += 1
                    total_assassin += 1
        # assert assassin randomness within +- 5% of 75% specified
        self.assertLess(total_assassin / 10000, 0.8)
        self.assertGreater(total_assassin / 10000, 0.7)
        for player in log:
            # assert each player assassin total is within 10% of 20% expected for 5 players
            self.assertLess(log[player] / total_assassin, 0.3)
            self.assertGreater(log[player] / total_assassin, 0.1)