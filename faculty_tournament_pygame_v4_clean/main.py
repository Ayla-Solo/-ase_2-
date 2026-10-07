import math
import sys
from pathlib import Path

import pygame

from game_logic import (
    ACTIONS,
    EVENTS,
    EVENT_STEPS,
    PATH_LENGTH,
    QUESTIONS,
    GameState,
    Player,
)


# =========================================================
# PYGAME
# =========================================================

pygame.init()

WIDTH, HEIGHT = 1400, 860

screen = pygame.display.set_mode(
    (
        WIDTH,
        HEIGHT
    )
)

pygame.display.set_caption(
    "Турнир Факультетов — Кубок Огня"
)

clock = pygame.time.Clock()


ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"


# =========================================================
# ШРИФТЫ
# =========================================================

FONT = pygame.font.SysFont(
    "arial",
    22
)

FONT_SM = pygame.font.SysFont(
    "arial",
    16
)

FONT_BIG = pygame.font.SysFont(
    "arial",
    40,
    bold=True
)

FONT_HUGE = pygame.font.SysFont(
    "arial",
    52,
    bold=True
)

FONT_Q = pygame.font.SysFont(
    "arial",
    28,
    bold=True
)


# =========================================================
# ФАКУЛЬТЕТЫ
# =========================================================

COLORS = {
    "Гриффиндор": (
        155,
        45,
        48
    ),

    "Когтевран": (
        0,
        47,
        85
    ),

    "Пуффендуй": (
        251,
        236,
        93
    ),
}


START_FILES = {
    "Гриффиндор":
        "Gryffindor.png",

    "Когтевран":
        "Ravenclaw.png",

    "Пуффендуй":
        "Hufflepuff.png",
}


# =========================================================
# ИГРОКИ
# =========================================================

players = [
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


game = GameState(
    players
)


# =========================================================
# СОСТОЯНИЯ
# =========================================================

# TURN
# QUESTION
# RESULT
# ACTION
# TARGET

STATE = "TURN"

message = (
    "Игрок 1: нажмите «СДЕЛАТЬ ХОД»"
)

pending_action = None
pending_event = None
last_result = None


# =========================================================
# МАРШРУТЫ
# =========================================================

def build_paths():

    center = (
        660,
        390
    )


    starts = [
        (
            120,
            150
        ),

        (
            120,
            650
        ),

        (
            1180,
            650
        ),
    ]


    bends = [
        [
            (220, 150),
            (300, 220),
            (360, 300),
            (430, 310),
            (500, 360),
            (560, 360),
        ],

        [
            (220, 650),
            (280, 580),
            (360, 540),
            (430, 500),
            (500, 450),
            (560, 430),
        ],

        [
            (1080, 650),
            (1000, 580),
            (920, 540),
            (850, 500),
            (790, 450),
            (730, 430),
        ],
    ]


    paths = []


    for player_index in range(3):

        anchors = (
            [starts[player_index]]
            + bends[player_index]
            + [center]
        )


        segment_lengths = [
            math.dist(
                point_a,
                point_b
            )
            for point_a, point_b
            in zip(
                anchors,
                anchors[1:]
            )
        ]


        total_length = sum(
            segment_lengths
        )


        cumulative = [
            0
        ]


        current_length = 0


        for length in segment_lengths:

            current_length += length

            cumulative.append(
                current_length
            )


        points = []


        for step in range(
            PATH_LENGTH + 1
        ):

            target_distance = (
                total_length
                * step
                / PATH_LENGTH
            )


            segment = 0


            while (
                segment
                < len(segment_lengths) - 1
                and target_distance
                > cumulative[segment + 1]
            ):

                segment += 1


            point_a = anchors[
                segment
            ]

            point_b = anchors[
                segment + 1
            ]


            local = (
                target_distance
                - cumulative[segment]
            ) / (
                segment_lengths[segment]
                or 1
            )


            x = int(
                point_a[0]
                + (
                    point_b[0]
                    - point_a[0]
                )
                * local
            )


            y = int(
                point_a[1]
                + (
                    point_b[1]
                    - point_a[1]
                )
                * local
            )


            points.append(
                (
                    x,
                    y
                )
            )


        paths.append(
            points
        )


    return paths


PATHS = build_paths()


# =========================================================
# ФОН
# =========================================================

BACKGROUND = pygame.image.load(
    ASSETS / "opf.jpg"
).convert()


BACKGROUND = pygame.transform.scale(
    BACKGROUND,
    (
        WIDTH,
        HEIGHT
    )
)


# =========================================================
# КУБОК
# =========================================================

CUP_SIZE = 55


CUP_IMG = pygame.image.load(
    ASSETS / "cup.png"
).convert_alpha()


CUP_IMG = pygame.transform.smoothscale(
    CUP_IMG,
    (
        CUP_SIZE,
        CUP_SIZE
    )
)


CUP_RECT = CUP_IMG.get_rect(
    center=(
        660,
        390
    )
)


# =========================================================
# ИЗОБРАЖЕНИЯ ФАКУЛЬТЕТОВ
# =========================================================

START_SIZE = 70

START_IMGS = {}


for faculty, filename in START_FILES.items():

    image = pygame.image.load(
        ASSETS / filename
    ).convert_alpha()


    START_IMGS[
        faculty
    ] = pygame.transform.smoothscale(
        image,
        (
            START_SIZE,
            START_SIZE
        )
    )


TOKEN_SIZE = 40


TOKEN_IMGS = {
    faculty:
        pygame.transform.smoothscale(
            START_IMGS[faculty],
            (
                TOKEN_SIZE,
                TOKEN_SIZE
            )
        )

    for faculty
    in COLORS
}


# =========================================================
# КНОПКИ
# =========================================================

def draw_button(
    rect,
    text,
    enabled=True,
    font=FONT_SM
):

    if enabled:

        color = (
            120,
            85,
            53
        )

    else:

        color = (
            48,
            50,
            56
        )


    mouse = pygame.mouse.get_pos()


    if (
        enabled
        and rect.collidepoint(mouse)
    ):

        color = (
            100,
            118,
            155
        )


    pygame.draw.rect(
        screen,
        color,
        rect,
        border_radius=9
    )


    pygame.draw.rect(
        screen,
        (
            210,
            190,
            130
        ),
        rect,
        2,
        border_radius=9
    )


    if enabled:

        text_color = (
            245,
            245,
            245
        )

    else:

        text_color = (
            130,
            130,
            130
        )


    surface = font.render(
        text,
        True,
        text_color
    )


    screen.blit(
        surface,
        surface.get_rect(
            center=rect.center
        )
    )


# =========================================================
# ТЕКСТ
# =========================================================

def wrap_text(
    text,
    font,
    max_width
):

    words = text.split()

    lines = []

    line = ""


    for word in words:

        candidate = (
            word
            if not line
            else line + " " + word
        )


        if (
            font.size(candidate)[0]
            <= max_width
        ):

            line = candidate

        else:

            if line:

                lines.append(
                    line
                )

            line = word


    if line:

        lines.append(
            line
        )


    return lines


def draw_centered_multiline(
    text,
    font,
    color,
    rect,
    gap=8
):

    lines = wrap_text(
        text,
        font,
        rect.width - 20
    )


    total_height = (
        len(lines)
        * font.get_height()
        + max(
            0,
            len(lines) - 1
        )
        * gap
    )


    y = (
        rect.centery
        - total_height // 2
    )


    for line in lines:

        surface = font.render(
            line,
            True,
            color
        )


        screen.blit(
            surface,
            surface.get_rect(
                center=(
                    rect.centerx,
                    y
                    + font.get_height()
                    // 2
                )
            )
        )


        y += (
            font.get_height()
            + gap
        )


# =========================================================
# ФОРМАТ ИЗМЕНЕНИЙ
# =========================================================

def format_delta(
    delta
):

    names = {
        "hp": "HP",
        "rating": "Рейтинг",
        "potions": "Зелья",
        "galleons": "Галлеоны",
        "scrolls": "Свитки",
    }


    parts = []


    for key, value in delta.items():

        name = names.get(
            key,
            key
        )


        if value > 0:

            sign = "+"

        else:

            sign = ""


        parts.append(
            f"{name}: {sign}{value}"
        )


    return ", ".join(
        parts
    )


# =========================================================
# ЛАБИРИНТ
# =========================================================

def draw_maze():

    screen.blit(
        BACKGROUND,
        (
            0,
            0
        )
    )


    for i, points in enumerate(
        PATHS
    ):

        color = COLORS[
            players[i].faculty
        ]


        pygame.draw.lines(
            screen,
            (
                80,
                40,
                50
            ),
            False,
            points,
            12
        )


        pygame.draw.lines(
            screen,
            color,
            False,
            points,
            4
        )


        for index, point in enumerate(
            points
        ):

            if (
                index
                in EVENT_STEPS
            ):

                pygame.draw.circle(
                    screen,
                    (
                        220,
                        178,
                        70
                    ),
                    point,
                    16
                )


                pygame.draw.circle(
                    screen,
                    (
                        255,
                        235,
                        160
                    ),
                    point,
                    16,
                    3
                )


                question_mark = FONT_SM.render(
                    "?",
                    True,
                    (
                        35,
                        35,
                        35
                    )
                )


                screen.blit(
                    question_mark,
                    question_mark.get_rect(
                        center=point
                    )
                )


            else:

                pygame.draw.circle(
                    screen,
                    (
                        120,
                        85,
                        53
                    ),
                    point,
                    10
                )


                pygame.draw.circle(
                    screen,
                    (
                        53,
                        23,
                        12
                    ),
                    point,
                    10,
                    2
                )


    # КУБОК

    pygame.draw.circle(
        screen,
        (
            120,
            85,
            53
        ),
        (
            660,
            390
        ),
        CUP_SIZE // 2 + 6
    )


    pygame.draw.circle(
        screen,
        (
            53,
            23,
            12
        ),
        (
            660,
            390
        ),
        CUP_SIZE // 2 + 6,
        4
    )


    screen.blit(
        CUP_IMG,
        CUP_RECT
    )


    # СТАРТЫ

    starts = [
        PATHS[i][0]
        for i
        in range(3)
    ]


    for i, start in enumerate(
        starts
    ):

        image = START_IMGS[
            players[i].faculty
        ]


        screen.blit(
            image,
            image.get_rect(
                center=start
            )
        )


        label = FONT_SM.render(
            f"СТАРТ {i + 1}",
            True,
            (
                245,
                245,
                245
            )
        )


        screen.blit(
            label,
            (
                start[0] - 32,

                start[1]
                - START_SIZE // 2
                - 22
            )
        )


# =========================================================
# ИГРОКИ
# =========================================================

def draw_players():

    for i, player in enumerate(
        players
    ):

        position = PATHS[i][
            player.position
        ]


        image = TOKEN_IMGS[
            player.faculty
        ]


        screen.blit(
            image,
            image.get_rect(
                center=position
            )
        )


        number = FONT_SM.render(
            str(i + 1),
            True,
            "white"
        )


        screen.blit(
            number,
            number.get_rect(
                center=position
            )
        )


# =========================================================
# ПАНЕЛЬ ИГРОКОВ
# =========================================================

def draw_panel():

    pygame.draw.rect(
        screen,
        (
            31,
            13,
            7
        ),
        (
            1030,
            10,
            360,
            260
        ),
        border_radius=12
    )


    for i, player in enumerate(
        players
    ):

        y = (
            25
            + i * 78
        )


        active = (
            i
            == game.current
        )


        if active:

            border = (
                235,
                205,
                120
            )

        else:

            border = (
                80,
                86,
                96
            )


        pygame.draw.rect(
            screen,
            border,
            (
                1040,
                y,
                340,
                68
            ),
            2,
            border_radius=8
        )


        name_text = (
            f"{player.name} / "
            f"{player.faculty}"
        )


        if not player.alive:

            name_text += (
                " — ВЫБЫЛ"
            )


        screen.blit(
            FONT_SM.render(
                name_text,
                True,
                (
                    245,
                    245,
                    240
                )
            ),
            (
                1050,
                y + 7
            )
        )


        screen.blit(
            FONT_SM.render(
                (
                    f"HP {player.hp}  "
                    f"Рейтинг {player.rating}  "
                    f"Путь "
                    f"{player.position}/"
                    f"{PATH_LENGTH}"
                ),
                True,
                (
                    225,
                    225,
                    225
                )
            ),
            (
                1050,
                y + 29
            )
        )


        screen.blit(
            FONT_SM.render(
                (
                    f"Зелья {player.potions}  "
                    f"Галлеоны "
                    f"{player.galleons}  "
                    f"Свитки "
                    f"{player.scrolls}"
                ),
                True,
                (
                    205,
                    205,
                    205
                )
            ),
            (
                1050,
                y + 49
            )
        )


# =========================================================
# ВОПРОС
# =========================================================

def draw_question_overlay():

    event_id = (
        pending_event
    )


    question = QUESTIONS[
        event_id
    ]


    event_data = EVENTS[
        event_id
    ]


    overlay = pygame.Surface(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.SRCALPHA
    )


    overlay.fill(
        (
            0,
            0,
            0,
            205
        )
    )


    screen.blit(
        overlay,
        (
            0,
            0
        )
    )


    card = pygame.Rect(
        175,
        90,
        1050,
        650
    )


    pygame.draw.rect(
        screen,
        (
            20,
            28,
            48
        ),
        card,
        border_radius=16
    )


    pygame.draw.rect(
        screen,
        (
            230,
            195,
            105
        ),
        card,
        4,
        border_radius=16
    )


    # Название события.
    # Никаких E1/E2 сверху нет.

    title = FONT_BIG.render(
        event_data["name"],
        True,
        (
            247,
            226,
            165
        )
    )


    screen.blit(
        title,
        title.get_rect(
            center=(
                card.centerx,
                135
            )
        )
    )


    question_rect = pygame.Rect(
        235,
        180,
        930,
        190
    )


    draw_centered_multiline(
        question["question"],
        FONT_Q,
        (
            245,
            245,
            245
        ),
        question_rect,
        10
    )


    answer_rects = []


    for i, option in enumerate(
        question["options"]
    ):

        row, column = divmod(
            i,
            2
        )


        rect = pygame.Rect(
            250
            + column * 470,

            410
            + row * 100,

            430,
            72
        )


        draw_button(
            rect,
            option,
            True,
            FONT
        )


        answer_rects.append(
            rect
        )


    hint = FONT_SM.render(
        (
            "Правильный ответ = хороший исход, "
            "ошибка = плохой исход."
        ),
        True,
        (
            200,
            205,
            215
        )
    )


    screen.blit(
        hint,
        hint.get_rect(
            center=(
                card.centerx,
                650
            )
        )
    )


    return answer_rects


# =========================================================
# РЕЗУЛЬТАТ
# =========================================================

def draw_result_overlay():

    correct, outcome, delta = (
        last_result
    )


    event_data = EVENTS[
        pending_event
    ]


    overlay = pygame.Surface(
        (
            WIDTH,
            HEIGHT
        ),
        pygame.SRCALPHA
    )


    overlay.fill(
        (
            0,
            0,
            0,
            205
        )
    )


    screen.blit(
        overlay,
        (
            0,
            0
        )
    )


    card = pygame.Rect(
        260,
        180,
        880,
        430
    )


    pygame.draw.rect(
        screen,
        (
            20,
            28,
            48
        ),
        card,
        border_radius=16
    )


    if correct:

        border = (
            74,
            190,
            120
        )

        head = (
            "ПРАВИЛЬНО"
        )

    else:

        border = (
            210,
            78,
            78
        )

        head = (
            "НЕПРАВИЛЬНО"
        )


    pygame.draw.rect(
        screen,
        border,
        card,
        4,
        border_radius=16
    )


    screen.blit(
        FONT_HUGE.render(
            head,
            True,
            border
        ),
        (
            card.x + 60,
            card.y + 45
        )
    )


    screen.blit(
        FONT_BIG.render(
            event_data["name"],
            True,
            (
                245,
                245,
                245
            )
        ),
        (
            card.x + 60,
            card.y + 125
        )
    )


    if outcome == "good":

        outcome_text = (
            "Хороший"
        )

    else:

        outcome_text = (
            "Плохой"
        )


    screen.blit(
        FONT.render(
            f"Исход: {outcome_text}",
            True,
            (
                220,
                220,
                220
            )
        ),
        (
            card.x + 60,
            card.y + 190
        )
    )


    changes_text = (
        format_delta(
            delta
        )
    )


    screen.blit(
        FONT.render(
            f"Изменения: {changes_text}",
            True,
            (
                220,
                220,
                220
            )
        ),
        (
            card.x + 60,
            card.y + 230
        )
    )


    continue_button = pygame.Rect(
        card.centerx - 180,
        card.bottom - 95,
        360,
        55
    )


    draw_button(
        continue_button,
        "ПЕРЕЙТИ К ДЕЙСТВИЮ",
        True,
        FONT
    )


    return continue_button


# =========================================================
# КНОПКИ ДЕЙСТВИЙ
# =========================================================

def action_buttons():

    rects = {}


    x_start = 30
    y_start = 735


    actor = players[
        game.current
    ]


    for i, (
        action_id,
        action
    ) in enumerate(
        ACTIONS.items()
    ):

        rect = pygame.Rect(
            x_start
            + i * 160,

            y_start,

            145,
            48
        )


        enabled = game.can_pay(
            actor,
            action["cost"]
        )


        # Тут специально НЕТ A1/A2/A3.
        # Показывается только название.

        draw_button(
            rect,
            action["name"],
            enabled
        )


        rects[
            action_id
        ] = (
            rect,
            enabled
        )


    return rects


# =========================================================
# ГЛАВНЫЙ ЦИКЛ
# =========================================================

while True:

    clicked = None


    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            pygame.quit()

            sys.exit()


        if (
            event.type
            == pygame.MOUSEBUTTONDOWN
            and event.button == 1
        ):

            clicked = event.pos


    # -----------------------------------------------------
    # ОСНОВНОЙ ЭКРАН
    # -----------------------------------------------------

    draw_maze()

    draw_players()

    draw_panel()


    screen.blit(
        FONT_BIG.render(
            "Кубок Огня",
            True,
            (
                246,
                232,
                190
            )
        ),
        (
            573,
            25
        )
    )


    screen.blit(
        FONT.render(
            message,
            True,
            (
                245,
                245,
                245
            )
        ),
        (
            20,
            20
        )
    )


    current = players[
        game.current
    ]


    winner = game.winner()


    # =====================================================
    # ПОБЕДИТЕЛЬ
    # =====================================================

    if winner:

        overlay = pygame.Surface(
            (
                WIDTH,
                HEIGHT
            ),
            pygame.SRCALPHA
        )


        overlay.fill(
            (
                0,
                0,
                0,
                190
            )
        )


        screen.blit(
            overlay,
            (
                0,
                0
            )
        )


        text = FONT_HUGE.render(
            f"Победил {winner.name}",
            True,
            (
                250,
                220,
                110
            )
        )


        screen.blit(
            text,
            text.get_rect(
                center=(
                    WIDTH // 2,
                    HEIGHT // 2 - 20
                )
            )
        )


        pygame.display.flip()

        clock.tick(
            60
        )

        continue


    # =====================================================
    # ХОД
    # =====================================================

    if STATE == "TURN":

        move_rect = pygame.Rect(
            555,
            581,
            210,
            55
        )


        draw_button(
            move_rect,
            "СДЕЛАТЬ ХОД",
            True,
            FONT
        )


        if (
            clicked
            and move_rect.collidepoint(
                clicked
            )
        ):

            hit_event = (
                game.move_current()
            )


            # Игрок дошёл до Кубка.

            if current.reached_cup:

                message = (
                    f"{current.name} "
                    f"дошёл до Кубка!"
                )


            # Игрок попал на вопрос.

            elif hit_event:

                pending_event = (
                    game.get_current_event_id()
                )


                if (
                    pending_event
                    is not None
                ):

                    STATE = (
                        "QUESTION"
                    )


                    event_name = EVENTS[
                        pending_event
                    ]["name"]


                    message = (
                        f"{current.name}: "
                        f"{event_name}"
                    )


                else:

                    STATE = (
                        "ACTION"
                    )


                    message = (
                        "Для этой клетки "
                        "не найден вопрос."
                    )


            # Обычная клетка.

            else:

                STATE = (
                    "ACTION"
                )


                message = (
                    f"{current.name} "
                    f"прошёл на 1 клетку. "
                    f"Можно применить "
                    f"одно действие."
                )


    # =====================================================
    # ВОПРОС
    # =====================================================

    elif STATE == "QUESTION":

        answer_rects = (
            draw_question_overlay()
        )


        if clicked:

            for index, rect in enumerate(
                answer_rects
            ):

                if rect.collidepoint(
                    clicked
                ):

                    last_result = (
                        game.resolve_question(
                            current,
                            pending_event,
                            index
                        )
                    )


                    STATE = (
                        "RESULT"
                    )


                    break


    # =====================================================
    # РЕЗУЛЬТАТ
    # =====================================================

    elif STATE == "RESULT":

        continue_rect = (
            draw_result_overlay()
        )


        if (
            clicked
            and continue_rect.collidepoint(
                clicked
            )
        ):

            STATE = (
                "ACTION"
            )


            message = (
                "Теперь можно применить "
                "одно управляемое действие."
            )


    # =====================================================
    # ДЕЙСТВИЕ
    # =====================================================

    elif STATE == "ACTION":

        screen.blit(
            FONT_SM.render(
                (
                    "Выберите одно действие "
                    "или пропустите:"
                ),
                True,
                (
                    235,
                    235,
                    235
                )
            ),
            (
                30,
                700
            )
        )


        rects = (
            action_buttons()
        )


        skip_button = pygame.Rect(
            1010,
            735,
            180,
            48
        )


        draw_button(
            skip_button,
            "Пропустить"
        )


        if clicked:

            chosen = None


            for action_id, (
                rect,
                enabled
            ) in rects.items():

                if (
                    enabled
                    and rect.collidepoint(
                        clicked
                    )
                ):

                    chosen = (
                        action_id
                    )

                    break


            # ---------------------------------------------
            # ДЕЙСТВИЕ ВЫБРАНО
            # ---------------------------------------------

            if chosen:

                if ACTIONS[
                    chosen
                ]["target"]:

                    pending_action = (
                        chosen
                    )


                    STATE = (
                        "TARGET"
                    )


                    message = (
                        f"{ACTIONS[chosen]['name']}: "
                        f"выберите цель справа."
                    )


                else:

                    success = (
                        game.perform_action(
                            chosen,
                            current
                        )
                    )


                    if success:

                        game.next_turn()


                        STATE = (
                            "TURN"
                        )


                        message = (
                            f"Действие применено. "
                            f"Ход: "
                            f"{players[game.current].name}."
                        )


                    else:

                        message = (
                            "Не хватает ресурсов."
                        )


            # ---------------------------------------------
            # ПРОПУСК
            # ---------------------------------------------

            elif skip_button.collidepoint(
                clicked
            ):

                game.next_turn()


                STATE = (
                    "TURN"
                )


                message = (
                    f"Действие пропущено. "
                    f"Ход: "
                    f"{players[game.current].name}."
                )


    # =====================================================
    # ВЫБОР ЦЕЛИ
    # =====================================================

    elif STATE == "TARGET":

        candidates = [
            player
            for player in players
            if (
                player is not current
                and player.alive
            )
        ]


        screen.blit(
            FONT.render(
                "Выберите цель:",
                True,
                (
                    245,
                    235,
                    200
                )
            ),
            (
                1030,
                300
            )
        )


        for index, target in enumerate(
            candidates
        ):

            rect = pygame.Rect(
                1035,
                340
                + index * 58,
                300,
                44
            )


            draw_button(
                rect,
                target.name,
                True,
                FONT
            )


            if (
                clicked
                and rect.collidepoint(
                    clicked
                )
            ):

                success = (
                    game.perform_action(
                        pending_action,
                        current,
                        target
                    )
                )


                if success:

                    action_name = ACTIONS[
                        pending_action
                    ]["name"]


                    game.next_turn()


                    STATE = (
                        "TURN"
                    )


                    message = (
                        f"{action_name} "
                        f"применено к "
                        f"{target.name}. "
                        f"Ход: "
                        f"{players[game.current].name}."
                    )


                else:

                    STATE = (
                        "ACTION"
                    )


                    message = (
                        "Действие невозможно "
                        "или не хватает ресурсов."
                    )


                break


    pygame.display.flip()

    clock.tick(
        60
    )