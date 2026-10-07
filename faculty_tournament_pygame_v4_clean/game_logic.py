from dataclasses import dataclass
from typing import Dict, List, Optional


MAX_HP = 100

PATH_LENGTH = 16
EVENT_STEPS = {3, 6, 9, 12, 15}
MOVE_PER_TURN = 1


START_RESOURCES = {
    "hp": 100,
    "rating": 0,
    "potions": 3,
    "galleons": 10,
    "scrolls": 1,
}


# =========================================================
# СОБЫТИЯ
# =========================================================

EVENTS: Dict[str, dict] = {
    # 1 ТОЧКА — ЛЁГКИЕ

    "E1": {
        "name": "Распределяющая шляпа",
        "good": {"hp": 5},
        "bad": {"hp": -5},
    },

    "E2": {
        "name": "Совиная почта",
        "good": {"rating": 5},
        "bad": {"rating": -5},
    },

    "E3": {
        "name": "Встреча с семьёй Уизли",
        "good": {"potions": 1},
        "bad": {"hp": -5},
    },


    # 2 ТОЧКА — ЧУТЬ СЛОЖНЕЕ

    "E4": {
        "name": "Матч по квиддичу",
        "good": {"rating": 5},
        "bad": {"hp": -10},
    },

    "E5": {
        "name": "Запертая дверь",
        "good": {"galleons": 5},
        "bad": {"rating": -5},
    },

    "E6": {
        "name": "Тайна Карты Мародёров",
        "good": {"hp": 10},
        "bad": {"hp": -10},
    },


    # 3 ТОЧКА — СРЕДНИЕ

    "E7": {
        "name": "Тайна R.A.B.",
        "good": {"rating": 10},
        "bad": {"hp": -10},
    },

    "E8": {
        "name": "Испытание Феликс Фелицис",
        "good": {"hp": 10},
        "bad": {"hp": -10},
    },

    "E9": {
        "name": "Завещание Дамблдора",
        "good": {
            "potions": 1,
            "galleons": 5,
        },
        "bad": {
            "hp": -10,
            "galleons": -5,
        },
    },


    # 4 ТОЧКА — СЛОЖНЫЕ

    "E10": {
        "name": "Испытание Бузинной палочки",
        "good": {"rating": 10},
        "bad": {"hp": -15},
    },

    "E11": {
        "name": "Тайна крестража",
        "good": {"potions": 2},
        "bad": {
            "hp": -10,
            "rating": -5,
        },
    },

    "E12": {
        "name": "Пророчество",
        "good": {"hp": 15},
        "bad": {"hp": -15},
    },


    # 5 ТОЧКА — ХАРД

    "E13": {
        "name": "Последний снитч",
        "good": {"rating": 10},
        "bad": {"hp": -15},
    },

    "E14": {
        "name": "Потерянная диадема Когтевран",
        "good": {
            "potions": 2,
            "galleons": 5,
        },
        "bad": {
            "hp": -10,
            "rating": -10,
        },
    },

    "E15": {
        "name": "Верность Бузинной палочки",
        "good": {
            "hp": 15,
            "rating": 10,
        },
        "bad": {
            "hp": -15,
            "rating": -10,
        },
    },
}


# =========================================================
# ВОПРОСЫ
# =========================================================

QUESTIONS: Dict[str, dict] = {
    # 1 ТОЧКА — ЛЁГКИЕ

    "E1": {
        "question": "На каком факультете учился Гарри Поттер?",
        "options": [
            "Гриффиндор",
            "Слизерин",
            "Когтевран",
            "Пуффендуй",
        ],
        "correct": 0,
    },

    "E2": {
        "question": "Как зовут сову Гарри Поттера?",
        "options": [
            "Букля",
            "Нагайна",
            "Живоглот",
            "Клювокрыл",
        ],
        "correct": 0,
    },

    "E3": {
        "question": "Кто лучший друг Гарри из семьи Уизли?",
        "options": [
            "Рон",
            "Фред",
            "Джордж",
            "Перси",
        ],
        "correct": 0,
    },


    # 2 ТОЧКА

    "E4": {
        "question": "На какой позиции Гарри играет в квиддич?",
        "options": [
            "Ловец",
            "Охотник",
            "Загонщик",
            "Вратарь",
        ],
        "correct": 0,
    },

    "E5": {
        "question": "Какое заклинание открывает запертые двери?",
        "options": [
            "Алохомора",
            "Люмос",
            "Акцио",
            "Протего",
        ],
        "correct": 0,
    },

    "E6": {
        "question": (
            "Как называется карта, показывающая людей "
            "и их перемещения по Хогвартсу?"
        ),
        "options": [
            "Карта Мародёров",
            "Карта Основателей",
            "Карта Хогвартса",
            "Волшебный атлас",
        ],
        "correct": 0,
    },


    # 3 ТОЧКА

    "E7": {
        "question": "Кто скрывался под инициалами R.A.B.?",
        "options": [
            "Регулус Арктурус Блэк",
            "Сириус Блэк",
            "Ремус Люпин",
            "Бартемиус Крауч",
        ],
        "correct": 0,
    },

    "E8": {
        "question": (
            "Какое зелье приносит выпившему "
            "необычайную удачу?"
        ),
        "options": [
            "Феликс Фелицис",
            "Амортенция",
            "Веритасерум",
            "Оборотное зелье",
        ],
        "correct": 0,
    },

    "E9": {
        "question": (
            "Что Дамблдор оставил Рону Уизли "
            "в своём завещании?"
        ),
        "options": [
            "Делюминатор",
            "Снитч",
            "Меч Гриффиндора",
            "Карту Мародёров",
        ],
        "correct": 0,
    },


    # 4 ТОЧКА

    "E10": {
        "question": (
            "Кто был истинным хозяином Бузинной палочки "
            "непосредственно перед Гарри Поттером?"
        ),
        "options": [
            "Северус Снейп",
            "Волан-де-Морт",
            "Драко Малфой",
            "Альбус Дамблдор",
        ],
        "correct": 2,
    },

    "E11": {
        "question": (
            "Какой из крестражей Гарри уничтожил "
            "ещё на втором курсе?"
        ),
        "options": [
            "Медальон Слизерина",
            "Дневник Тома Реддла",
            "Диадема Когтевран",
            "Кольцо Марволо Мракса",
        ],
        "correct": 1,
    },

    "E12": {
        "question": (
            "Кто услышал часть пророчества о Гарри "
            "и Волан-де-Морте и передал её Волан-де-Морту?"
        ),
        "options": [
            "Люциус Малфой",
            "Питер Петтигрю",
            "Северус Снейп",
            "Бартемиус Крауч-младший",
        ],
        "correct": 2,
    },


    # 5 ТОЧКА — ХАРД

    "E13": {
        "question": (
            "Что было написано на снитче, "
            "который Дамблдор оставил Гарри?"
        ),
        "options": [
            "Всё начинается здесь",
            "Я открываюсь под конец",
            "Последний враг — смерть",
            "Следуй за светом",
        ],
        "correct": 1,
    },

    "E14": {
        "question": (
            "Какой предмет Ровены Когтевран "
            "Волан-де-Морт превратил в крестраж?"
        ),
        "options": [
            "Кубок",
            "Диадему",
            "Медальон",
            "Кольцо",
        ],
        "correct": 1,
    },

    "E15": {
        "question": (
            "Почему Бузинная палочка не подчинялась "
            "Волан-де-Морту полностью?"
        ),
        "options": [
            "Палочка была повреждена",
            "Он не был её истинным хозяином",
            "Она принадлежала только Дамблдору",
            "Она не могла использоваться против Гарри",
        ],
        "correct": 1,
    },
}


# =========================================================
# ВОПРОСЫ ДЛЯ КАЖДОГО ИГРОКА
# =========================================================

EVENT_BY_PLAYER_AND_STEP = {
    0: {
        3: "E1",
        6: "E4",
        9: "E7",
        12: "E10",
        15: "E13",
    },

    1: {
        3: "E2",
        6: "E5",
        9: "E8",
        12: "E11",
        15: "E14",
    },

    2: {
        3: "E3",
        6: "E6",
        9: "E9",
        12: "E12",
        15: "E15",
    },
}


# =========================================================
# ДЕЙСТВИЯ
# =========================================================

ACTIONS: Dict[str, dict] = {
    "A1": {
        "name": "Торговля",
        "cost": {"galleons": 3},
        "target": True,
    },

    "A2": {
        "name": "Подкуп",
        "cost": {"galleons": 5},
        "target": True,
    },

    "A3": {
        "name": "Дуэль",
        "cost": {"hp": 10},
        "target": True,
    },

    "A4": {
        "name": "Союз",
        "cost": {"potions": 1},
        "target": True,
    },

    "A5": {
        "name": "Проклятие",
        "cost": {"scrolls": 1},
        "target": True,
    },

    "A6": {
        "name": "Выпить зелье",
        "cost": {"potions": 1},
        "target": False,
    },
}


# =========================================================
# ИГРОК
# =========================================================

@dataclass
class Player:
    name: str
    faculty: str

    hp: int = 100
    rating: int = 0

    potions: int = 3
    galleons: int = 10
    scrolls: int = 1

    position: int = 0

    skip_turn: bool = False
    reached_cup: bool = False

    finished_order: Optional[int] = None


    @property
    def alive(self) -> bool:
        return self.hp > 0


    def change(
        self,
        delta: Dict[str, int]
    ) -> None:

        for key, value in delta.items():

            new_value = (
                getattr(self, key)
                + value
            )

            if key == "hp":

                new_value = max(
                    0,
                    min(
                        MAX_HP,
                        new_value
                    )
                )

            elif key in (
                "rating",
                "potions",
                "galleons",
                "scrolls",
            ):

                new_value = max(
                    0,
                    new_value
                )

            setattr(
                self,
                key,
                new_value
            )


# =========================================================
# ИГРА
# =========================================================

class GameState:

    def __init__(
        self,
        players: List[Player]
    ):

        self.players = players
        self.current = 0

        self.log: List[str] = []

        self.finish_counter = 0


    def living_players(
        self
    ) -> List[Player]:

        return [
            player
            for player in self.players
            if player.alive
        ]


    # -----------------------------------------------------
    # ДВИЖЕНИЕ
    # -----------------------------------------------------

    def move_current(
        self
    ) -> bool:

        player = self.players[
            self.current
        ]

        if not player.alive:
            return False

        if player.reached_cup:
            return False


        player.position = min(
            PATH_LENGTH,
            player.position
            + MOVE_PER_TURN
        )


        landed_on_event = (
            player.position
            in EVENT_STEPS
        )


        if (
            player.position
            >= PATH_LENGTH
            and not player.reached_cup
        ):

            player.reached_cup = True

            self.finish_counter += 1

            player.finished_order = (
                self.finish_counter
            )


        return landed_on_event


    # -----------------------------------------------------
    # ВОПРОС ТЕКУЩЕГО ИГРОКА
    # -----------------------------------------------------

    def get_current_event_id(
        self
    ) -> Optional[str]:

        player = self.players[
            self.current
        ]

        return (
            EVENT_BY_PLAYER_AND_STEP
            .get(
                self.current,
                {}
            )
            .get(
                player.position
            )
        )


    # -----------------------------------------------------
    # ПРОВЕРКА ОТВЕТА
    # -----------------------------------------------------

    def resolve_question(
        self,
        player: Player,
        event_id: str,
        selected_index: int
    ):

        question = QUESTIONS[
            event_id
        ]

        correct = (
            selected_index
            == question["correct"]
        )


        if correct:
            outcome = "good"
        else:
            outcome = "bad"


        delta = EVENTS[
            event_id
        ][outcome]


        player.change(
            delta
        )


        self.log.append(
            f"{player.name}: "
            f"{EVENTS[event_id]['name']} -> "
            f"{'правильно' if correct else 'неправильно'} -> "
            f"{delta}"
        )


        return (
            correct,
            outcome,
            delta
        )


    # -----------------------------------------------------
    # ПРОВЕРКА РЕСУРСОВ
    # -----------------------------------------------------

    def can_pay(
        self,
        player: Player,
        cost: Dict[str, int]
    ) -> bool:

        return all(
            getattr(
                player,
                key
            ) >= value
            for key, value
            in cost.items()
        )


    # -----------------------------------------------------
    # ДЕЙСТВИЯ
    # -----------------------------------------------------

    def perform_action(
        self,
        action_id: str,
        actor: Player,
        target: Optional[Player] = None
    ) -> bool:

        action = ACTIONS[
            action_id
        ]


        if not actor.alive:
            return False


        if not self.can_pay(
            actor,
            action["cost"]
        ):
            return False


        if action["target"]:

            if target is None:
                return False

            if target is actor:
                return False

            if not target.alive:
                return False


        # Для торговли у другого игрока
        # должно быть хотя бы одно зелье.

        if (
            action_id == "A1"
            and target.potions < 1
        ):
            return False


        # Списываем стоимость действия.

        actor.change({
            key: -value
            for key, value
            in action["cost"].items()
        })


        # ТОРГОВЛЯ
        if action_id == "A1":

            target.potions -= 1

            actor.potions += 1

            target.galleons += 3


        # ПОДКУП
        elif action_id == "A2":

            target.change({
                "hp": -10
            })


        # ДУЭЛЬ
        elif action_id == "A3":

            target.change({
                "hp": -15
            })


        # СОЮЗ
        elif action_id == "A4":

            actor.change({
                "hp": 10
            })

            target.change({
                "hp": 10
            })


        # ПРОКЛЯТИЕ
        elif action_id == "A5":

            target.skip_turn = True


        # ВЫПИТЬ ЗЕЛЬЕ
        elif action_id == "A6":

            actor.change({
                "hp": 10
            })


        self.log.append(
            f"{actor.name}: "
            f"{action['name']}"
            + (
                f" -> {target.name}"
                if target
                else ""
            )
        )


        return True


    # -----------------------------------------------------
    # ПОБЕДИТЕЛЬ
    # -----------------------------------------------------

    def winner(
        self
    ) -> Optional[Player]:

        alive = (
            self.living_players()
        )


        # Если в живых остался только один —
        # он автоматически побеждает.

        if len(alive) == 1:

            return alive[0]


        # Иначе выигрывает тот,
        # кто первым дошёл до Кубка.

        finishers = [
            player
            for player in alive
            if player.reached_cup
        ]


        if finishers:

            return min(
                finishers,
                key=lambda player:
                    player.finished_order
                    or 999999
            )


        return None


    # -----------------------------------------------------
    # СЛЕДУЮЩИЙ ХОД
    # -----------------------------------------------------

    def next_turn(
        self
    ) -> None:

        checked = 0


        while (
            checked
            < len(self.players) * 2
        ):

            self.current = (
                self.current + 1
            ) % len(self.players)


            checked += 1


            player = self.players[
                self.current
            ]


            # Игрок выбыл.
            if not player.alive:
                continue


            # Игрок уже дошёл до Кубка.
            if player.reached_cup:
                continue


            # Игрок проклят.
            if player.skip_turn:

                player.skip_turn = False

                self.log.append(
                    f"{player.name} "
                    f"пропускает ход "
                    f"из-за проклятия."
                )

                continue


            return