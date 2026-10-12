import unittest
from game_logic import GameState, Player


class TestQuestionAssignment(unittest.TestCase):

    def setUp(self):
        self.players = [
            Player('Игрок 1', 'Гриффиндор'),
            Player('Игрок 2', 'Когтевран'),
            Player('Игрок 3', 'Пуффендуй')
        ]
        self.game = GameState(self.players)

    def test_player_one_first_question_is_e1(self):
        self.game.current = 0
        self.players[0].position = 3

        self.assertEqual(
            self.game.get_current_event_id(),
            'E1'
        )

    def test_player_two_first_question_is_e2(self):
        self.game.current = 1
        self.players[1].position = 3

        self.assertEqual(
            self.game.get_current_event_id(),
            'E2'
        )

    def test_player_three_first_question_is_e3(self):
        self.game.current = 2
        self.players[2].position = 3

        self.assertEqual(
            self.game.get_current_event_id(),
            'E3'
        )

    def test_normal_cell_has_no_question(self):
        self.game.current = 0
        self.players[0].position = 4

        self.assertIsNone(
            self.game.get_current_event_id()
        )

    def test_last_question_for_player_one(self):
        self.game.current = 0
        self.players[0].position = 15

        self.assertEqual(
            self.game.get_current_event_id(),
            'E13'
        )

    def test_last_question_for_player_two(self):
        self.game.current = 1
        self.players[1].position = 15

        self.assertEqual(
            self.game.get_current_event_id(),
            'E14'
        )

    def test_last_question_for_player_three(self):
        self.game.current = 2
        self.players[2].position = 15

        self.assertEqual(
            self.game.get_current_event_id(),
            'E15'
        )