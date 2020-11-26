#!/usr/bin/env python
"""
Parser for the NIST FFAST database compiled by Chantler C. T., et.al.
"""

# Standard library modules.
import logging
import os
import pkgutil

# Third party modules.


# Local modules.
import pyxray.parser.base as base
from pyxray.descriptor import Reference, Element
from pyxray.property import (
    ElementAtomicWeight,
    ElementMassDensity,
    AtomicSubshellBindingEnergy,
)

# Globals and constants variables.
logger = logging.getLogger(__name__)

CHANTLER2005 = Reference(
    "chantler2005",
    author="Chantler, C.T. and Olsen, K. and Dragoset, R.A. and Chang, J. and Kishore, A.R. and Kotochigova, S.A. and "
    "Zucker, D.S.",
    year="2005",
    title="X-Ray Form Factor, Attenuation, and Scattering Tables (version 2.1)",
    publisher="National Institute of Standards and Technology, Gaithersburg, MD, USA",
    doi="10.18434/T4HS32",
    howpublished="Online",
    url="http://physics.nist.gov/ffast",
)

_SUBSHELLS = [
    base.K,
    base.L1,
    base.L2,
    base.L3,
    base.M1,
    base.M2,
    base.M3,
    base.M4,
    base.M5,
    base.N1,
    base.N2,
    base.N3,
    base.N4,
    base.N5,
    base.N6,
    base.N7,
    base.O1,
    base.O2,
    base.O3,
    base.O4,
    base.O5,
    base.P1,
    base.P2,
    base.P3,
]

_NUM_SUBSHELLS = 24


class Chantler2005Parser(base._Parser):
    def __iter__(self):
        relpath = os.path.join("..", "data", "shelldata.csv")
        content = pkgutil.get_data(__name__, relpath).decode("utf8")

        rows = content.splitlines()
        n_rows = len(rows)

        for z in range(1, len(rows)):
            row = [item.strip() for item in rows[z].split(",")]
            element = Element(z)

            prop = ElementAtomicWeight(CHANTLER2005, element, float(row[0]))
            logger.debug(f"Parsed: {prop}")
            yield prop

            prop = ElementMassDensity(CHANTLER2005, element, float(row[2]) * 1e3)
            logger.debug(f"Parsed: {prop}")
            yield prop

            for i in range(_NUM_SUBSHELLS):
                value = row[i + 7]
                if value:
                    prop = AtomicSubshellBindingEnergy(
                        CHANTLER2005, element, _SUBSHELLS[i], float(value)
                    )
                    logger.debug(f"Parsed: {prop}")
                    yield prop

            self.update(int(z / n_rows * 100))
