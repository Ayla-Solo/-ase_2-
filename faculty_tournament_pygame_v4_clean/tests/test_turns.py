import unittest
from game_logic import GameState, Player


class TestTurns(unittest.TestCase):

    def setUp(self):
        self.player1 = Player('Игрок 1', 'Гриффиндор')
        self.player2 = Player('Игрок 2', 'Когтевран')
        self.player3 = Player('Игрок 3', 'Пуффендуй')

        self.game = GameState([
            self.player1,
            self.player2,
            self.player3
        ])

    def test_first_player_starts(self):
        self.assertEqual(self.game.current, 0)

    def test_next_turn_goes_to_second_player(self):
        self.game.next_turn()
        self.assertEqual(self.game.current, 1)

    def test_turn_order_cycles(self):
        self.game.next_turn()
        self.assertEqual(self.game.current, 1)

        self.game.next_turn()
        self.assertEqual(self.game.current, 2)

        self.game.next_turn()
        self.assertEqual(self.game.current, 0)

    def test_dead_player_is_skipped(self):
        self.player2.hp = 0
        self.game.next_turn()

        self.assertEqual(self.game.current, 2)

    def test_cursed_player_skips_one_turn(self):
        self.player2.skip_turn = True
        self.game.next_turn()

        self.assertEqual(self.game.current, 2)
        self.assertFalse(self.player2.skip_turn)

    def test_player_at_cup_is_skipped(self):
        self.player2.position = 16
        self.player2.reached_cup = True

        self.game.next_turn()

        self.assertEqual(self.game.current, 2)