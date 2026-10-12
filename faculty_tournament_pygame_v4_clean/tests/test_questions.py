import unittest
from game_logic import EVENTS, GameState, Player, QUESTIONS


class TestQuestions(unittest.TestCase):

    def setUp(self):
        self.player = Player(
            'Игрок',
            'Гриффиндор',
            hp=50,
            rating=50,
            potions=10,
            galleons=20,
            scrolls=3
        )

        self.other_players = [
            Player('Игрок 2', 'Когтевран'),
            Player('Игрок 3', 'Пуффендуй')
        ]

        self.game = GameState([
            self.player,
            *self.other_players
        ])

    def test_all_correct_answers_are_accepted(self):
        for event_id, question in QUESTIONS.items():
            player = Player(
                'Игрок',
                'Гриффиндор',
                hp=50,
                rating=50,
                potions=10,
                galleons=20
            )

            game = GameState([
                player,
                Player('Игрок 2', 'Когтевран'),
                Player('Игрок 3', 'Пуффендуй')
            ])

            with self.subTest(event=event_id):
                correct, outcome, _ = game.resolve_question(
                    player,
                    event_id,
                    question['correct']
                )

                self.assertTrue(correct)
                self.assertEqual(outcome, 'good')

    def test_all_wrong_answers_are_rejected(self):
        for event_id, question in QUESTIONS.items():
            player = Player(
                'Игрок',
                'Гриффиндор',
                hp=50,
                rating=50,
                potions=10,
                galleons=20
            )

            game = GameState([
                player,
                Player('Игрок 2', 'Когтевран'),
                Player('Игрок 3', 'Пуффендуй')
            ])

            wrong_answer = (question['correct'] + 1) % 4

            with self.subTest(event=event_id):
                correct, outcome, _ = game.resolve_question(
                    player,
                    event_id,
                    wrong_answer
                )

                self.assertFalse(correct)
                self.assertEqual(outcome, 'bad')

    def test_all_good_event_effects(self):
        for event_id in EVENTS:
            player = Player(
                'Игрок',
                'Гриффиндор',
                hp=50,
                rating=50,
                potions=10,
                galleons=20,
                scrolls=3
            )

            game = GameState([
                player,
                Player('Игрок 2', 'Когтевран'),
                Player('Игрок 3', 'Пуффендуй')
            ])

            before = {
                'hp': player.hp,
                'rating': player.rating,
                'potions': player.potions,
                'galleons': player.galleons,
                'scrolls': player.scrolls
            }

            correct_index = QUESTIONS[event_id]['correct']

            game.resolve_question(
                player,
                event_id,
                correct_index
            )

            expected_delta = EVENTS[event_id]['good']

            with self.subTest(event=event_id):
                for key, value in expected_delta.items():
                    self.assertEqual(
                        getattr(player, key),
                        before[key] + value
                    )

    def test_all_bad_event_effects(self):
        for event_id in EVENTS:
            player = Player(
                'Игрок',
                'Гриффиндор',
                hp=50,
                rating=50,
                potions=10,
                galleons=20,
                scrolls=3
            )

            game = GameState([
                player,
                Player('Игрок 2', 'Когтевран'),
                Player('Игрок 3', 'Пуффендуй')
            ])

            before = {
                'hp': player.hp,
                'rating': player.rating,
                'potions': player.potions,
                'galleons': player.galleons,
                'scrolls': player.scrolls
            }

            correct_index = QUESTIONS[event_id]['correct']
            wrong_index = (correct_index + 1) % 4

            game.resolve_question(
                player,
                event_id,
                wrong_index
            )

            expected_delta = EVENTS[event_id]['bad']

            with self.subTest(event=event_id):
                for key, value in expected_delta.items():
                    self.assertEqual(
                        getattr(player, key),
                        before[key] + value
                    )