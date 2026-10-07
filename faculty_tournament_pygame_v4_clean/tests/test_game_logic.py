import unittest

from game_logic import (
    ACTIONS,
    EVENTS,
    EVENT_BY_PLAYER_AND_STEP,
    EVENT_STEPS,
    MAX_HP,
    MOVE_PER_TURN,
    PATH_LENGTH,
    QUESTIONS,
    START_RESOURCES,
    GameState,
    Player,
)


class TestPlayer(unittest.TestCase):

    def test_default_resources(self):
        player = Player(
            "Игрок",
            "Гриффиндор"
        )

        self.assertEqual(player.hp, 100)
        self.assertEqual(player.rating, 0)
        self.assertEqual(player.potions, 3)
        self.assertEqual(player.galleons, 10)
        self.assertEqual(player.scrolls, 1)


    def test_player_is_alive(self):
        player = Player(
            "Игрок",
            "Гриффиндор"
        )

        self.assertTrue(
            player.alive
        )


    def test_player_dead_at_zero_hp(self):
        player = Player(
            "Игрок",
            "Гриффиндор"
        )

        player.hp = 0

        self.assertFalse(
            player.alive
        )


    def test_hp_cannot_go_above_100(self):
        player = Player(
            "Игрок",
            "Гриффиндор",
            hp=95
        )

        player.change({
            "hp": 20
        })

        self.assertEqual(
            player.hp,
            MAX_HP
        )


    def test_hp_cannot_go_below_zero(self):
        player = Player(
            "Игрок",
            "Гриффиндор",
            hp=5
        )

        player.change({
            "hp": -50
        })

        self.assertEqual(
            player.hp,
            0
        )


    def test_rating_cannot_go_below_zero(self):
        player = Player(
            "Игрок",
            "Гриффиндор",
            rating=3
        )

        player.change({
            "rating": -10
        })

        self.assertEqual(
            player.rating,
            0
        )


    def test_resources_cannot_go_below_zero(self):
        player = Player(
            "Игрок",
            "Гриффиндор",
            potions=1,
            galleons=2,
            scrolls=1
        )

        player.change({
            "potions": -10,
            "galleons": -10,
            "scrolls": -10,
        })

        self.assertEqual(
            player.potions,
            0
        )

        self.assertEqual(
            player.galleons,
            0
        )

        self.assertEqual(
            player.scrolls,
            0
        )


class TestGameData(unittest.TestCase):

    def test_path_length(self):
        self.assertEqual(
            PATH_LENGTH,
            16
        )


    def test_move_per_turn(self):
        self.assertEqual(
            MOVE_PER_TURN,
            1
        )


    def test_event_steps(self):
        self.assertEqual(
            EVENT_STEPS,
            {
                3,
                6,
                9,
                12,
                15,
            }
        )


    def test_number_of_events(self):
        self.assertEqual(
            len(EVENTS),
            15
        )


    def test_number_of_questions(self):
        self.assertEqual(
            len(QUESTIONS),
            15
        )


    def test_event_and_question_ids_match(self):
        self.assertEqual(
            set(EVENTS.keys()),
            set(QUESTIONS.keys())
        )


    def test_every_question_has_four_options(self):

        for event_id, question in QUESTIONS.items():

            with self.subTest(
                event=event_id
            ):

                self.assertEqual(
                    len(
                        question[
                            "options"
                        ]
                    ),
                    4
                )


    def test_every_correct_index_is_valid(self):

        for event_id, question in QUESTIONS.items():

            with self.subTest(
                event=event_id
            ):

                self.assertIn(
                    question["correct"],
                    range(4)
                )


    def test_three_players_have_question_maps(self):

        self.assertEqual(
            set(
                EVENT_BY_PLAYER_AND_STEP.keys()
            ),
            {
                0,
                1,
                2,
            }
        )


    def test_every_player_has_five_questions(self):

        for player_number in (
            0,
            1,
            2
        ):

            with self.subTest(
                player=player_number
            ):

                self.assertEqual(
                    len(
                        EVENT_BY_PLAYER_AND_STEP[
                            player_number
                        ]
                    ),
                    5
                )


    def test_every_player_uses_correct_event_steps(self):

        expected = {
            3,
            6,
            9,
            12,
            15,
        }

        for player_number in (
            0,
            1,
            2
        ):

            with self.subTest(
                player=player_number
            ):

                self.assertEqual(
                    set(
                        EVENT_BY_PLAYER_AND_STEP[
                            player_number
                        ].keys()
                    ),
                    expected
                )


    def test_all_15_questions_are_unique_in_mapping(self):

        assigned_events = []

        for mapping in (
            EVENT_BY_PLAYER_AND_STEP.values()
        ):

            assigned_events.extend(
                mapping.values()
            )

        self.assertEqual(
            len(assigned_events),
            15
        )

        self.assertEqual(
            len(
                set(
                    assigned_events
                )
            ),
            15
        )


    def test_player_one_question_sequence(self):

        self.assertEqual(
            EVENT_BY_PLAYER_AND_STEP[0],
            {
                3: "E1",
                6: "E4",
                9: "E7",
                12: "E10",
                15: "E13",
            }
        )


    def test_player_two_question_sequence(self):

        self.assertEqual(
            EVENT_BY_PLAYER_AND_STEP[1],
            {
                3: "E2",
                6: "E5",
                9: "E8",
                12: "E11",
                15: "E14",
            }
        )


    def test_player_three_question_sequence(self):

        self.assertEqual(
            EVENT_BY_PLAYER_AND_STEP[2],
            {
                3: "E3",
                6: "E6",
                9: "E9",
                12: "E12",
                15: "E15",
            }
        )


class TestMovement(unittest.TestCase):

    def setUp(self):

        self.players = [
            Player(
                "Игрок 1",
                "Гриффиндор"
            ),

            Player(
                "Игрок 2",
                "Когтевран"
            ),

            Player(
                "Игрок 3",
                "Пуффендуй"
            ),
        ]

        self.game = GameState(
            self.players
        )


    def test_player_moves_exactly_one_cell(self):

        self.game.move_current()

        self.assertEqual(
            self.players[0].position,
            1
        )


    def test_normal_cell_is_not_event(self):

        event = (
            self.game.move_current()
        )

        self.assertFalse(
            event
        )


    def test_cell_three_is_event(self):

        self.players[0].position = 2

        event = (
            self.game.move_current()
        )

        self.assertTrue(
            event
        )

        self.assertEqual(
            self.players[0].position,
            3
        )


    def test_all_event_cells_are_detected(self):

        for event_step in (
            3,
            6,
            9,
            12,
            15
        ):

            player = Player(
                "Игрок",
                "Гриффиндор"
            )

            game = GameState([
                player,
                Player(
                    "Игрок 2",
                    "Когтевран"
                ),
                Player(
                    "Игрок 3",
                    "Пуффендуй"
                ),
            ])

            player.position = (
                event_step - 1
            )

            with self.subTest(
                step=event_step
            ):

                self.assertTrue(
                    game.move_current()
                )


    def test_player_reaches_cup_at_16(self):

        self.players[0].position = 15

        self.game.move_current()

        self.assertEqual(
            self.players[0].position,
            16
        )

        self.assertTrue(
            self.players[0].reached_cup
        )


    def test_position_cannot_go_beyond_finish(self):

        self.players[0].position = 15

        self.game.move_current()

        self.game.move_current()

        self.assertEqual(
            self.players[0].position,
            16
        )


    def test_dead_player_cannot_move(self):

        self.players[0].hp = 0

        self.game.move_current()

        self.assertEqual(
            self.players[0].position,
            0
        )


    def test_finished_player_cannot_move_again(self):

        self.players[0].position = 16
        self.players[0].reached_cup = True

        self.game.move_current()

        self.assertEqual(
            self.players[0].position,
            16
        )


class TestQuestionAssignment(unittest.TestCase):

    def setUp(self):

        self.players = [
            Player(
                "Игрок 1",
                "Гриффиндор"
            ),

            Player(
                "Игрок 2",
                "Когтевран"
            ),

            Player(
                "Игрок 3",
                "Пуффендуй"
            ),
        ]

        self.game = GameState(
            self.players
        )


    def test_player_one_first_question_is_e1(self):

        self.game.current = 0

        self.players[0].position = 3

        self.assertEqual(
            self.game.get_current_event_id(),
            "E1"
        )


    def test_player_two_first_question_is_e2(self):

        self.game.current = 1

        self.players[1].position = 3

        self.assertEqual(
            self.game.get_current_event_id(),
            "E2"
        )


    def test_player_three_first_question_is_e3(self):

        self.game.current = 2

        self.players[2].position = 3

        self.assertEqual(
            self.game.get_current_event_id(),
            "E3"
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
            "E13"
        )


    def test_last_question_for_player_two(self):

        self.game.current = 1

        self.players[1].position = 15

        self.assertEqual(
            self.game.get_current_event_id(),
            "E14"
        )


    def test_last_question_for_player_three(self):

        self.game.current = 2

        self.players[2].position = 15

        self.assertEqual(
            self.game.get_current_event_id(),
            "E15"
        )


class TestQuestions(unittest.TestCase):

    def setUp(self):

        self.player = Player(
            "Игрок",
            "Гриффиндор",
            hp=50,
            rating=50,
            potions=10,
            galleons=20,
            scrolls=3,
        )

        self.other_players = [
            Player(
                "Игрок 2",
                "Когтевран"
            ),

            Player(
                "Игрок 3",
                "Пуффендуй"
            ),
        ]

        self.game = GameState(
            [
                self.player,
                *self.other_players
            ]
        )


    def test_all_correct_answers_are_accepted(self):

        for event_id, question in QUESTIONS.items():

            player = Player(
                "Игрок",
                "Гриффиндор",
                hp=50,
                rating=50,
                potions=10,
                galleons=20,
            )

            game = GameState([
                player,
                Player(
                    "Игрок 2",
                    "Когтевран"
                ),
                Player(
                    "Игрок 3",
                    "Пуффендуй"
                ),
            ])


            with self.subTest(
                event=event_id
            ):

                correct, outcome, _ = (
                    game.resolve_question(
                        player,
                        event_id,
                        question["correct"]
                    )
                )

                self.assertTrue(
                    correct
                )

                self.assertEqual(
                    outcome,
                    "good"
                )


    def test_all_wrong_answers_are_rejected(self):

        for event_id, question in QUESTIONS.items():

            player = Player(
                "Игрок",
                "Гриффиндор",
                hp=50,
                rating=50,
                potions=10,
                galleons=20,
            )

            game = GameState([
                player,
                Player(
                    "Игрок 2",
                    "Когтевран"
                ),
                Player(
                    "Игрок 3",
                    "Пуффендуй"
                ),
            ])


            wrong_answer = (
                question["correct"] + 1
            ) % 4


            with self.subTest(
                event=event_id
            ):

                correct, outcome, _ = (
                    game.resolve_question(
                        player,
                        event_id,
                        wrong_answer
                    )
                )

                self.assertFalse(
                    correct
                )

                self.assertEqual(
                    outcome,
                    "bad"
                )


    def test_all_good_event_effects(self):

        for event_id in EVENTS:

            player = Player(
                "Игрок",
                "Гриффиндор",
                hp=50,
                rating=50,
                potions=10,
                galleons=20,
                scrolls=3,
            )


            game = GameState([
                player,
                Player(
                    "Игрок 2",
                    "Когтевран"
                ),
                Player(
                    "Игрок 3",
                    "Пуффендуй"
                ),
            ])


            before = {
                "hp": player.hp,
                "rating": player.rating,
                "potions": player.potions,
                "galleons": player.galleons,
                "scrolls": player.scrolls,
            }


            correct_index = (
                QUESTIONS[
                    event_id
                ]["correct"]
            )


            game.resolve_question(
                player,
                event_id,
                correct_index
            )


            expected_delta = (
                EVENTS[
                    event_id
                ]["good"]
            )


            with self.subTest(
                event=event_id
            ):

                for key, value in (
                    expected_delta.items()
                ):

                    self.assertEqual(
                        getattr(
                            player,
                            key
                        ),
                        before[key]
                        + value
                    )


    def test_all_bad_event_effects(self):

        for event_id in EVENTS:

            player = Player(
                "Игрок",
                "Гриффиндор",
                hp=50,
                rating=50,
                potions=10,
                galleons=20,
                scrolls=3,
            )


            game = GameState([
                player,
                Player(
                    "Игрок 2",
                    "Когтевран"
                ),
                Player(
                    "Игрок 3",
                    "Пуффендуй"
                ),
            ])


            before = {
                "hp": player.hp,
                "rating": player.rating,
                "potions": player.potions,
                "galleons": player.galleons,
                "scrolls": player.scrolls,
            }


            correct_index = (
                QUESTIONS[
                    event_id
                ]["correct"]
            )


            wrong_index = (
                correct_index + 1
            ) % 4


            game.resolve_question(
                player,
                event_id,
                wrong_index
            )


            expected_delta = (
                EVENTS[
                    event_id
                ]["bad"]
            )


            with self.subTest(
                event=event_id
            ):

                for key, value in (
                    expected_delta.items()
                ):

                    self.assertEqual(
                        getattr(
                            player,
                            key
                        ),
                        before[key]
                        + value
                    )


class TestActions(unittest.TestCase):

    def setUp(self):

        self.player1 = Player(
            "Игрок 1",
            "Гриффиндор"
        )

        self.player2 = Player(
            "Игрок 2",
            "Когтевран"
        )

        self.player3 = Player(
            "Игрок 3",
            "Пуффендуй"
        )


        self.game = GameState([
            self.player1,
            self.player2,
            self.player3,
        ])


    def test_six_actions_exist(self):

        self.assertEqual(
            len(ACTIONS),
            6
        )


    def test_can_pay_when_resources_available(self):

        self.assertTrue(
            self.game.can_pay(
                self.player1,
                {
                    "galleons": 5
                }
            )
        )


    def test_cannot_pay_when_resources_missing(self):

        self.assertFalse(
            self.game.can_pay(
                self.player1,
                {
                    "galleons": 100
                }
            )
        )


    def test_trade(self):

        success = (
            self.game.perform_action(
                "A1",
                self.player1,
                self.player2
            )
        )


        self.assertTrue(
            success
        )

        self.assertEqual(
            self.player1.galleons,
            7
        )

        self.assertEqual(
            self.player1.potions,
            4
        )

        self.assertEqual(
            self.player2.potions,
            2
        )

        self.assertEqual(
            self.player2.galleons,
            13
        )


    def test_trade_fails_if_target_has_no_potion(self):

        self.player2.potions = 0


        success = (
            self.game.perform_action(
                "A1",
                self.player1,
                self.player2
            )
        )


        self.assertFalse(
            success
        )

        self.assertEqual(
            self.player1.galleons,
            10
        )


    def test_bribe(self):

        success = (
            self.game.perform_action(
                "A2",
                self.player1,
                self.player2
            )
        )


        self.assertTrue(
            success
        )

        self.assertEqual(
            self.player1.galleons,
            5
        )

        self.assertEqual(
            self.player2.hp,
            90
        )


    def test_duel(self):

        success = (
            self.game.perform_action(
                "A3",
                self.player1,
                self.player2
            )
        )


        self.assertTrue(
            success
        )

        self.assertEqual(
            self.player1.hp,
            90
        )

        self.assertEqual(
            self.player2.hp,
            85
        )


    def test_alliance(self):

        self.player1.hp = 70
        self.player2.hp = 60


        success = (
            self.game.perform_action(
                "A4",
                self.player1,
                self.player2
            )
        )


        self.assertTrue(
            success
        )

        self.assertEqual(
            self.player1.potions,
            2
        )

        self.assertEqual(
            self.player1.hp,
            80
        )

        self.assertEqual(
            self.player2.hp,
            70
        )


    def test_alliance_does_not_raise_hp_over_100(self):

        self.player1.hp = 95
        self.player2.hp = 95


        self.game.perform_action(
            "A4",
            self.player1,
            self.player2
        )


        self.assertEqual(
            self.player1.hp,
            100
        )

        self.assertEqual(
            self.player2.hp,
            100
        )


    def test_curse(self):

        success = (
            self.game.perform_action(
                "A5",
                self.player1,
                self.player2
            )
        )


        self.assertTrue(
            success
        )

        self.assertEqual(
            self.player1.scrolls,
            0
        )

        self.assertTrue(
            self.player2.skip_turn
        )


    def test_drink_potion(self):

        self.player1.hp = 70


        success = (
            self.game.perform_action(
                "A6",
                self.player1
            )
        )


        self.assertTrue(
            success
        )

        self.assertEqual(
            self.player1.hp,
            80
        )

        self.assertEqual(
            self.player1.potions,
            2
        )


    def test_drink_potion_cannot_raise_hp_over_100(self):

        self.player1.hp = 95


        self.game.perform_action(
            "A6",
            self.player1
        )


        self.assertEqual(
            self.player1.hp,
            100
        )


    def test_action_fails_without_resources(self):

        self.player1.galleons = 0


        success = (
            self.game.perform_action(
                "A2",
                self.player1,
                self.player2
            )
        )


        self.assertFalse(
            success
        )

        self.assertEqual(
            self.player2.hp,
            100
        )


    def test_player_cannot_target_self(self):

        success = (
            self.game.perform_action(
                "A2",
                self.player1,
                self.player1
            )
        )


        self.assertFalse(
            success
        )


    def test_dead_player_cannot_be_targeted(self):

        self.player2.hp = 0


        success = (
            self.game.perform_action(
                "A2",
                self.player1,
                self.player2
            )
        )


        self.assertFalse(
            success
        )


    def test_dead_player_cannot_perform_action(self):

        self.player1.hp = 0


        success = (
            self.game.perform_action(
                "A2",
                self.player1,
                self.player2
            )
        )


        self.assertFalse(
            success
        )


class TestTurns(unittest.TestCase):

    def setUp(self):

        self.player1 = Player(
            "Игрок 1",
            "Гриффиндор"
        )

        self.player2 = Player(
            "Игрок 2",
            "Когтевран"
        )

        self.player3 = Player(
            "Игрок 3",
            "Пуффендуй"
        )


        self.game = GameState([
            self.player1,
            self.player2,
            self.player3,
        ])


    def test_first_player_starts(self):

        self.assertEqual(
            self.game.current,
            0
        )


    def test_next_turn_goes_to_second_player(self):

        self.game.next_turn()

        self.assertEqual(
            self.game.current,
            1
        )


    def test_turn_order_cycles(self):

        self.game.next_turn()

        self.assertEqual(
            self.game.current,
            1
        )


        self.game.next_turn()

        self.assertEqual(
            self.game.current,
            2
        )


        self.game.next_turn()

        self.assertEqual(
            self.game.current,
            0
        )


    def test_dead_player_is_skipped(self):

        self.player2.hp = 0


        self.game.next_turn()


        self.assertEqual(
            self.game.current,
            2
        )


    def test_cursed_player_skips_one_turn(self):

        self.player2.skip_turn = True


        self.game.next_turn()


        self.assertEqual(
            self.game.current,
            2
        )


        self.assertFalse(
            self.player2.skip_turn
        )


    def test_player_at_cup_is_skipped(self):

        self.player2.position = 16

        self.player2.reached_cup = True


        self.game.next_turn()


        self.assertEqual(
            self.game.current,
            2
        )


class TestWinner(unittest.TestCase):

    def setUp(self):

        self.player1 = Player(
            "Игрок 1",
            "Гриффиндор"
        )

        self.player2 = Player(
            "Игрок 2",
            "Когтевран"
        )

        self.player3 = Player(
            "Игрок 3",
            "Пуффендуй"
        )


        self.game = GameState([
            self.player1,
            self.player2,
            self.player3,
        ])


    def test_no_winner_at_start(self):

        self.assertIsNone(
            self.game.winner()
        )


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


        self.assertTrue(
            self.player1.reached_cup
        )


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


class TestStartResources(unittest.TestCase):

    def test_start_hp(self):

        self.assertEqual(
            START_RESOURCES["hp"],
            100
        )


    def test_start_rating(self):

        self.assertEqual(
            START_RESOURCES["rating"],
            0
        )


    def test_start_potions(self):

        self.assertEqual(
            START_RESOURCES["potions"],
            3
        )


    def test_start_galleons(self):

        self.assertEqual(
            START_RESOURCES["galleons"],
            10
        )


    def test_start_scrolls(self):

        self.assertEqual(
            START_RESOURCES["scrolls"],
            1
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )