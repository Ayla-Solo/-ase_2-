import unittest

from game_logic import (
    EVENTS,
    EVENT_BY_PLAYER_AND_STEP,
    EVENT_STEPS,
    MOVE_PER_TURN,
    PATH_LENGTH,
    QUESTIONS
)


class TestGameData(unittest.TestCase):

    def test_path_length(self):
        self.assertEqual(PATH_LENGTH, 16)

    def test_move_per_turn(self):
        self.assertEqual(MOVE_PER_TURN, 1)

    def test_event_steps(self):
        self.assertEqual(EVENT_STEPS, {3, 6, 9, 12, 15})

    def test_number_of_events(self):
        self.assertEqual(len(EVENTS), 15)

    def test_number_of_questions(self):
        self.assertEqual(len(QUESTIONS), 15)

    def test_event_and_question_ids_match(self):
        self.assertEqual(
            set(EVENTS.keys()),
            set(QUESTIONS.keys())
        )

    def test_every_question_has_four_options(self):
        for event_id, question in QUESTIONS.items():
            with self.subTest(event=event_id):
                self.assertEqual(len(question['options']), 4)

    def test_every_correct_index_is_valid(self):
        for event_id, question in QUESTIONS.items():
            with self.subTest(event=event_id):
                self.assertIn(question['correct'], range(4))

    def test_three_players_have_question_maps(self):
        self.assertEqual(
            set(EVENT_BY_PLAYER_AND_STEP.keys()),
            {0, 1, 2}
        )

    def test_every_player_has_five_questions(self):
        for player_number in (0, 1, 2):
            with self.subTest(player=player_number):
                self.assertEqual(
                    len(EVENT_BY_PLAYER_AND_STEP[player_number]),
                    5
                )

    def test_every_player_uses_correct_event_steps(self):
        expected = {3, 6, 9, 12, 15}

        for player_number in (0, 1, 2):
            with self.subTest(player=player_number):
                self.assertEqual(
                    set(EVENT_BY_PLAYER_AND_STEP[player_number].keys()),
                    expected
                )

    def test_all_15_questions_are_unique_in_mapping(self):
        assigned_events = []

        for mapping in EVENT_BY_PLAYER_AND_STEP.values():
            assigned_events.extend(mapping.values())

        self.assertEqual(len(assigned_events), 15)
        self.assertEqual(len(set(assigned_events)), 15)

    def test_player_one_question_sequence(self):
        self.assertEqual(
            EVENT_BY_PLAYER_AND_STEP[0],
            {
                3: 'E1',
                6: 'E4',
                9: 'E7',
                12: 'E10',
                15: 'E13'
            }
        )

    def test_player_two_question_sequence(self):
        self.assertEqual(
            EVENT_BY_PLAYER_AND_STEP[1],
            {
                3: 'E2',
                6: 'E5',
                9: 'E8',
                12: 'E11',
                15: 'E14'
            }
        )

    def test_player_three_question_sequence(self):
        self.assertEqual(
            EVENT_BY_PLAYER_AND_STEP[2],
            {
                3: 'E3',
                6: 'E6',
                9: 'E9',
                12: 'E12',
                15: 'E15'
            }
        )