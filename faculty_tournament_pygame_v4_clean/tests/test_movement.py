import unittest
from game_logic import GameState, Player


class TestMovement(unittest.TestCase):

    def setUp(self):
        self.players = [
            Player('Игрок 1', 'Гриффиндор'),
            Player('Игрок 2', 'Когтевран'),
            Player('Игрок 3', 'Пуффендуй')
        ]
        self.game = GameState(self.players)

    def test_player_moves_exactly_one_cell(self):
        self.game.move_current()
        self.assertEqual(self.players[0].position, 1)

    def test_normal_cell_is_not_event(self):
        event = self.game.move_current()
        self.assertFalse(event)

    def test_cell_three_is_event(self):
        self.players[0].position = 2
        event = self.game.move_current()

        self.assertTrue(event)
        self.assertEqual(self.players[0].position, 3)

    def test_all_event_cells_are_detected(self):
        for event_step in (3, 6, 9, 12, 15):
            player = Player('Игрок', 'Гриффиндор')

            game = GameState([
                player,
                Player('Игрок 2', 'Когтевран'),
                Player('Игрок 3', 'Пуффендуй')
            ])

            player.position = event_step - 1

            with self.subTest(step=event_step):
                self.assertTrue(game.move_current())

    def test_player_reaches_cup_at_16(self):
        self.players[0].position = 15
        self.game.move_current()

        self.assertEqual(self.players[0].position, 16)
        self.assertTrue(self.players[0].reached_cup)

    def test_position_cannot_go_beyond_finish(self):
        self.players[0].position = 15

        self.game.move_current()
        self.game.move_current()

        self.assertEqual(self.players[0].position, 16)

    def test_dead_player_cannot_move(self):
        self.players[0].hp = 0
        self.game.move_current()

        self.assertEqual(self.players[0].position, 0)

    def test_finished_player_cannot_move_again(self):
        self.players[0].position = 16
        self.players[0].reached_cup = True

        self.game.move_current()

        self.assertEqual(self.players[0].position, 16)