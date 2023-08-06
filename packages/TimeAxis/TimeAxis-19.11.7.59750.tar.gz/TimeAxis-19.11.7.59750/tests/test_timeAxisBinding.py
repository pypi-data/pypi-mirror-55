from unittest import TestCase

from timeaxis import TimeAxisBinding


class TestTimeAxisBinding(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        import os
        os.environ['TZ'] = 'MST'

    def test_repr_01(self):
        self.assertEqual("beginning", repr(TimeAxisBinding.BEGINNING))

    def test_repr_02(self):
        self.assertEqual("end", repr(TimeAxisBinding.END))

    def test_repr_03(self):
        self.assertEqual("middle", repr(TimeAxisBinding.MIDDLE))

    def test_repr_04(self):
        self.assertEqual("custom_fraction", repr(TimeAxisBinding.CUSTOM_FRACTION))

    def test_valueOf_01(self):
        self.assertEqual(
            TimeAxisBinding.BEGINNING,
            TimeAxisBinding.valueOf("beGiNnIng")
        )

    def test_valueOf_02(self):
        with self.assertRaises(ValueError):
            TimeAxisBinding.valueOf("None Existing")

    def test_valueOf_03(self):
        self.assertEqual(
            TimeAxisBinding.BEGINNING,
            TimeAxisBinding.valueOf(TimeAxisBinding.BEGINNING)
        )

    def test_valueOf_04(self):
        with self.assertRaises(TypeError):
            TimeAxisBinding.valueOf({})

    def test_valueOf_05(self):
        self.assertEqual(TimeAxisBinding.BEGINNING, TimeAxisBinding.valueOf(0))

    def test_valueOf_06(self):
        self.assertEqual(TimeAxisBinding.END, TimeAxisBinding.valueOf(1.0))

    def test_valueOf_07(self):
        self.assertEqual(TimeAxisBinding.MIDDLE, TimeAxisBinding.valueOf(0.5))

    def test_valueOf_08(self):
        self.assertEqual(TimeAxisBinding.CUSTOM_FRACTION, TimeAxisBinding.valueOf(0.2))

    def test_valueOf_09(self):
        with self.assertRaises(ValueError):
            TimeAxisBinding.valueOf(10)

    def test_fraction_01(self):
        self.assertEqual(0.0, TimeAxisBinding.BEGINNING.fraction())

    def test_fraction_02(self):
        self.assertEqual(1.0, TimeAxisBinding.END.fraction())

    def test_fraction_03(self):
        self.assertEqual(0.5, TimeAxisBinding.MIDDLE.fraction())

    def test_fraction_04(self):
        self.assertEqual(None, TimeAxisBinding.CUSTOM_FRACTION.fraction())






