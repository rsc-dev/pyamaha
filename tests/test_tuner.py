from unittest import TestCase

from pyamaha import Tuner, BAND, TUNING, ZONES, PRESET_BAND


class TestTuner(TestCase):
    def test_set_freq(self):
        self.assertEqual(
            Tuner.set_freq(band='common', tuning='up', num=1),
            'http://{host}/YamahaExtendedControl/v1/tuner/setFreq?band=common&tuning=up&num=1')

    def test_recall_preset(self):
        self.assertEqual(
            Tuner.recall_preset(zone='main', band='common', num=1),
            'http://{host}/YamahaExtendedControl/v1/tuner/recallPreset?zone=main&band=common&num=1')

    def test_store_preset(self):
        self.assertEqual(
            Tuner.store_preset(num=1),
            'http://{host}/YamahaExtendedControl/v1/tuner/storePreset?num=1')
