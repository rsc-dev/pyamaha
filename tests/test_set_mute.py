from unittest import TestCase

from pyamaha import Zone, ZONES

DEFAULT_ZONE = ZONES[0]


class TestSetMute(TestCase):
    expected = Zone.URI['SET_MUTE'].format(host='{host}', zone=DEFAULT_ZONE, enable='false')

    def test_lower_case_strings_are_unaffected(self):
        self.assertEqual(Zone.set_mute(DEFAULT_ZONE, 'false'), self.expected)

    def test_title_case_strings_are_made_lower_case(self):
        self.assertEqual(Zone.set_mute(DEFAULT_ZONE, 'False'), self.expected)

    def booleans_are_outputted_in_lower_case(self):
        self.assertEqual(Zone.set_mute(DEFAULT_ZONE, False), self.expected)
