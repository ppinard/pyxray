#!/usr/bin/env python
""" """

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
from pyxray.descriptor import AtomicSubshell
from pyxray.parser.chantler2005 import Chantler2005Parser

# Globals and constants variables.


def test_chantler2005():
    parser = Chantler2005Parser()

    props = list(parser)
    assert len(props) == 1435

    assert props[0].element.z == 1  # First element
    assert props[0].value == pytest.approx(1.008, abs=1e-3)  # Atomic weight
    assert props[1].element.z == 1
    assert props[1].value_kg_per_m3 == pytest.approx(0.08987, abs=1e-5)  # Mass density

    assert props[1434].element.z == 92  # Last element
    assert props[1434].atomic_subshell == AtomicSubshell(6, 1, 3)  # Subshell
    assert props[1434].value_eV == pytest.approx(
        32.3, abs=1e-4
    )  # Subshell binding energy
