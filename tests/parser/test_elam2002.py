#!/usr/bin/env python
""" """

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
from pyxray.descriptor import AtomicSubshell, XrayTransition
from pyxray.parser.elam2002 import Elam2002Parser

# Globals and constants variables.


def test_elam2002():
    parser = Elam2002Parser()

    props = list(parser)
    assert len(props) == 5237

    assert props[0].element.z == 1  # First element
    assert props[0].value == pytest.approx(1.00790, abs=1e-5)  # Atomic weight
    assert props[1].element.z == 1
    assert props[1].value_kg_per_m3 == pytest.approx(71.0, abs=1e-1)  # Mass density

    assert props[9].element.z == 3
    assert props[9].xray_transition == XrayTransition(2, 0, 1, 1, 0, 1)  # Transition
    assert props[9].value_eV == pytest.approx(49.4000, abs=1e-4)  # Transition energy
    assert props[10].value == pytest.approx(9e-05, abs=1e-5)  # Transition probability

    assert props[5236].element.z == 98  # Last element
    assert props[5236].atomic_subshell == AtomicSubshell(6, 1, 3)  # Subshell
    assert props[5236].value_eV == pytest.approx(
        17.0, abs=1e-1
    )  # Subshell binding energy
