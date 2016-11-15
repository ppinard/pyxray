#!/usr/bin/env python
""" """

# Standard library modules.
import unittest
import logging

# Third party modules.

# Local modules.
from pyxray.base import _Database

# Globals and constants variables.

class MockDatabase(_Database):

    def element_atomic_number(self, element):
        pass

    def element_symbol(self, element, reference=None):
        pass

    def element_name(self, element, language='en', reference=None):
        pass

    def element_atomic_weight(self, element, reference=None):
        pass

    def element_mass_density_kg_per_m3(self, element, reference=None):
        pass

    def element_mass_density_g_per_cm3(self, element, reference=None):
        pass

    def atomic_shell_notation(self, atomic_shell, notation, encoding='utf16', reference=None):
        pass

    def atomic_subshell_notation(self, atomic_subshell, notation, encoding='utf16', reference=None):
        pass

    def atomic_subshell_binding_energy_eV(self, element, atomic_subshell, reference=None):
        pass

    def atomic_subshell_radiative_width_eV(self, element, atomic_subshell, reference=None):
        pass

    def atomic_subshell_nonradiative_width_eV(self, element, atomic_subshell, reference=None):
        pass

    def atomic_subshell_occupancy(self, element, atomic_subshell, reference=None):
        pass

    def transition_notation(self, transition, notation, encoding='utf16', reference=None):
        pass

    def transition_energy_eV(self, element, transition, reference=None):
        pass

    def transition_probability(self, element, transition, reference=None):
        pass

    def transition_relative_weight(self, element, transition, reference=None):
        pass

    def transitionset_notation(self, transitionset, notation, encoding='utf16', reference=None):
        pass

    def transitionset_energy_eV(self, element, transitionset, reference=None):
        pass

    def transitionset_relative_weight(self, element, transitionset, reference=None):
        pass

class Test_Database(unittest.TestCase):

    def setUp(self):
        unittest.TestCase.setUp(self)

        self.database = MockDatabase()

    def tearDown(self):
        unittest.TestCase.tearDown(self)

    def testget_default_reference(self):
        self.assertIsNone(self.database.get_default_reference('element_symbol'))
        self.assertRaises(ValueError, self.database.get_default_reference, 'foo')

    def testset_default_reference(self):
        self.database.set_default_reference('element_symbol', 'doe2016')

        self.assertEqual('doe2016', self.database.get_default_reference('element_symbol'))
        self.assertRaises(ValueError, self.database.set_default_reference, 'foo', 'doe2016')

if __name__ == '__main__': #pragma: no cover
    logging.getLogger().setLevel(logging.DEBUG)
    unittest.main()