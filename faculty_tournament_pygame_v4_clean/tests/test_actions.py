import unittest
from game_logic import ACTIONS, GameState, Player


class TestActions(unittest.TestCase):

    def setUp(self):
        self.player1 = Player('Игрок 1', 'Гриффиндор')
        self.player2 = Player('Игрок 2', 'Когтевран')
        self.player3 = Player('Игрок 3', 'Пуффендуй')

        self.game = GameState([
            self.player1,
            self.player2,
            self.player3
        ])

    def test_six_actions_exist(self):
        self.assertEqual(len(ACTIONS), 6)

    def test_can_pay_when_resources_available(self):
        self.assertTrue(
            self.game.can_pay(
                self.player1,
                {'galleons': 5}
            )
        )

    def test_cannot_pay_when_resources_missing(self):
        self.assertFalse(
            self.game.can_pay(
                self.player1,
                {'galleons': 100}
            )
        )

    def test_trade(self):
        success = self.game.perform_action(
            'A1',
            self.player1,
            self.player2
        )

        self.assertTrue(success)
        self.assertEqual(self.player1.galleons, 7)
        self.assertEqual(self.player1.potions, 4)
        self.assertEqual(self.player2.potions, 2)
        self.assertEqual(self.player2.galleons, 13)

    def test_trade_fails_if_target_has_no_potion(self):
        self.player2.potions = 0

        success = self.game.perform_action(
            'A1',
            self.player1,
            self.player2
        )

        self.assertFalse(success)
        self.assertEqual(self.player1.galleons, 10)

    def test_bribe(self):
        success = self.game.perform_action(
            'A2',
            self.player1,
            self.player2
        )

        self.assertTrue(success)
        self.assertEqual(self.player1.galleons, 5)
        self.assertEqual(self.player2.hp, 90)

    def test_duel(self):
        success = self.game.perform_action(
            'A3',
            self.player1,
            self.player2
        )

        self.assertTrue(success)
        self.assertEqual(self.player1.hp, 90)
        self.assertEqual(self.player2.hp, 85)

    def test_alliance(self):
        self.player1.hp = 70
        self.player2.hp = 60

        success = self.game.perform_action(
            'A4',
            self.player1,
            self.player2
        )

        self.assertTrue(success)
        self.assertEqual(self.player1.potions, 2)
        self.assertEqual(self.player1.hp, 80)
        self.assertEqual(self.player2.hp, 70)

    def test_alliance_does_not_raise_hp_over_100(self):
        self.player1.hp = 95
        self.player2.hp = 95

        self.game.perform_action(
            'A4',
            self.player1,
            self.player2
        )

        self.assertEqual(self.player1.hp, 100)
        self.assertEqual(self.player2.hp, 100)

    def test_curse(self):
        success = self.game.perform_action(
            'A5',
            self.player1,
            self.player2
        )

        self.assertTrue(success)
        self.assertEqual(self.player1.scrolls, 0)
        self.assertTrue(self.player2.skip_turn)

    def test_drink_potion(self):
        self.player1.hp = 70

        success = self.game.perform_action(
            'A6',
            self.player1
        )

        self.assertTrue(success)
        self.assertEqual(self.player1.hp, 80)
        self.assertEqual(self.player1.potions, 2)

    def test_drink_potion_cannot_raise_hp_over_100(self):
        self.player1.hp = 95

        self.game.perform_action(
            'A6',
            self.player1
        )

        self.assertEqual(self.player1.hp, 100)

    def test_action_fails_without_resources(self):
        self.player1.galleons = 0

        success = self.game.perform_action(
            'A2',
            self.player1,
            self.player2
        )

        self.assertFalse(success)
        self.assertEqual(self.player2.hp, 100)

    def test_player_cannot_target_self(self):
        success = self.game.perform_action(
            'A2',
            self.player1,
            self.player1
        )

        self.assertFalse(success)

    def test_dead_player_cannot_be_targeted(self):
        self.player2.hp = 0

        success = self.game.perform_action(
            'A2',
            self.player1,
            self.player2
        )

        self.assertFalse(success)

    def test_dead_player_cannot_perform_action(self):
        self.player1.hp = 0

        success = self.game.perform_action(
            'A2',
            self.player1,
            self.player2
        )

        self.assertFalse(success)