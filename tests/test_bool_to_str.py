from unittest import TestCase

from pyamaha import _bool_to_str


class TestBoolToStr(TestCase):

    def test_lower_case_false_is_unaffected(self):
        self.assertEqual(_bool_to_str('false'), 'false')

    def test_lower_case_true_is_unaffected(self):
        self.assertEqual(_bool_to_str('true'), 'true')

    def test_title_case_false_is_made_lower_case(self):
        self.assertEqual(_bool_to_str('False'), 'false')

    def test_title_case_true_is_made_lower_case(self):
        self.assertEqual(_bool_to_str('True'), 'true')

    def test_boolean_false_is_outputted_in_lower_case(self):
        self.assertEqual(_bool_to_str(False), 'false')

    def test_boolean_true_is_outputted_in_lower_case(self):
        self.assertEqual(_bool_to_str(True), 'true')
