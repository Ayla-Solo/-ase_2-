import unittest
from game_logic import MAX_HP, Player


class TestPlayer(unittest.TestCase):

    def test_default_resources(self):
        player = Player('Игрок', 'Гриффиндор')
        self.assertEqual(player.hp, 100)
        self.assertEqual(player.rating, 0)
        self.assertEqual(player.potions, 3)
        self.assertEqual(player.galleons, 10)
        self.assertEqual(player.scrolls, 1)

    def test_player_is_alive(self):
        player = Player('Игрок', 'Гриффиндор')
        self.assertTrue(player.alive)

    def test_player_dead_at_zero_hp(self):
        player = Player('Игрок', 'Гриффиндор')
        player.hp = 0
        self.assertFalse(player.alive)

    def test_hp_cannot_go_above_100(self):
        player = Player('Игрок', 'Гриффиндор', hp=95)
        player.change({'hp': 20})
        self.assertEqual(player.hp, MAX_HP)

    def test_hp_cannot_go_below_zero(self):
        player = Player('Игрок', 'Гриффиндор', hp=5)
        player.change({'hp': -50})
        self.assertEqual(player.hp, 0)

    def test_rating_cannot_go_below_zero(self):
        player = Player('Игрок', 'Гриффиндор', rating=3)
        player.change({'rating': -10})
        self.assertEqual(player.rating, 0)

    def test_resources_cannot_go_below_zero(self):
        player = Player(
            'Игрок',
            'Гриффиндор',
            potions=1,
            galleons=2,
            scrolls=1
        )
        player.change({
            'potions': -10,
            'galleons': -10,
            'scrolls': -10
        })
        self.assertEqual(player.potions, 0)
        self.assertEqual(player.galleons, 0)
        self.assertEqual(player.scrolls, 0)