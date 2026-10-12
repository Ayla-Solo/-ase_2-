import unittest
from game_logic import GameState, Player


class TestWinner(unittest.TestCase):

    def setUp(self):
        self.player1 = Player('Игрок 1', 'Гриффиндор')
        self.player2 = Player('Игрок 2', 'Когтевран')
        self.player3 = Player('Игрок 3', 'Пуффендуй')

        self.game = GameState([
            self.player1,
            self.player2,
            self.player3
        ])

    def test_no_winner_at_start(self):
        self.assertIsNone(self.game.winner())

    def test_last_alive_player_wins(self):
        self.player2.hp = 0
        self.player3.hp = 0

        self.assertIs(
            self.game.winner(),
            self.player1
        )

    def test_player_at_cup_wins(self):
        self.player1.position = 15
        self.game.move_current()

        self.assertTrue(self.player1.reached_cup)
        self.assertIs(
            self.game.winner(),
            self.player1
        )

    def test_first_finisher_wins(self):
        self.player1.reached_cup = True
        self.player1.position = 16
        self.player1.finished_order = 1

        self.player2.reached_cup = True
        self.player2.position = 16
        self.player2.finished_order = 2

        self.assertIs(
            self.game.winner(),
            self.player1
        )

    def test_zero_hp_player_does_not_win(self):
        self.player1.hp = 0
        self.player1.reached_cup = True
        self.player1.position = 16
        self.player1.finished_order = 1

        self.assertIsNot(
            self.game.winner(),
            self.player1
        )