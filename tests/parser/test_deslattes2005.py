#!/usr/bin/env python
""" """

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
from pyxray.descriptor import AtomicSubshell, XrayTransition
from pyxray.parser.deslattes2005 import Deslattes2005Parser

# Globals and constants variables.


def test_deslattes2005():
    parser = Deslattes2005Parser()

    props = list(parser)
    assert len(props) == 7300

    assert props[0].element.z == 10  # First element
    assert props[0].atomic_subshell == AtomicSubshell(2, 1, 3)  # Subshell
    assert props[0].value_eV == pytest.approx(
        21.55, abs=1e-2
    )  # Subshell binding energy

    assert props[4].element.z == 11
    assert props[4].xray_transition == XrayTransition(3, 0, 1, 2, 1, 3)  # Transition
    assert props[4].value_eV == pytest.approx(31.09, abs=1e-4)  # Transition energy

    assert props[7299].element.z == 100  # Last element
    assert props[7299].atomic_subshell == AtomicSubshell(1, 0, 1)  # Subshell
    assert props[7299].value_eV == pytest.approx(
        141930.4, abs=1e-1
    )  # Subshell binding energy
