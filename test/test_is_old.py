from unittest import TestCase

from packaging.version import Version
from packaging.specifiers import SpecifierSet

from pyrrot import Pyrrot

class TestIsOld(TestCase):

    def setUp(self):
        self.l = Version('2.0.0')

    def test_equals(self):
        specs = SpecifierSet('==1.0.0')
        self.assertTrue(Pyrrot.is_old(self.l, specs))

        latest = Version('1.0.0')
        self.assertFalse(Pyrrot.is_old(latest, specs))

    def test_less_than(self):
        specs = SpecifierSet('<1.0.0')
        self.assertTrue(Pyrrot.is_old(self.l, specs))

        specs = SpecifierSet('<2.0.0')
        self.assertTrue(Pyrrot.is_old(self.l, specs))

        specs = SpecifierSet('<3.0.0')
        self.assertFalse(Pyrrot.is_old(self.l, specs))

    def test_less_or_equal(self):
        specs = SpecifierSet('<=1.0.0')
        self.assertTrue(Pyrrot.is_old(self.l, specs))

        specs = SpecifierSet('<=2.0.0')
        self.assertFalse(Pyrrot.is_old(self.l, specs))

    def test_greaters(self):
        specs = SpecifierSet('>1.0.0')
        self.assertFalse(Pyrrot.is_old(self.l, specs))

        # FIXME: latest is older than our requirements
        specs = SpecifierSet('>2.0.0')
        self.assertFalse(Pyrrot.is_old(self.l, specs))

        specs = SpecifierSet('>=1.0.0')
        self.assertFalse(Pyrrot.is_old(self.l, specs))

        specs = SpecifierSet('>=2.0.0')
        self.assertFalse(Pyrrot.is_old(self.l, specs))
