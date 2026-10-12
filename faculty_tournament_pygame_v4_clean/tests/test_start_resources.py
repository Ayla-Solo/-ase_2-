import unittest
from game_logic import START_RESOURCES


class TestStartResources(unittest.TestCase):

    def test_start_hp(self):
        self.assertEqual(START_RESOURCES['hp'], 100)

    def test_start_rating(self):
        self.assertEqual(START_RESOURCES['rating'], 0)

    def test_start_potions(self):
        self.assertEqual(START_RESOURCES['potions'], 3)

    def test_start_galleons(self):
        self.assertEqual(START_RESOURCES['galleons'], 10)

    def test_start_scrolls(self):
        self.assertEqual(START_RESOURCES['scrolls'], 1)