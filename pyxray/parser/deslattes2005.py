#!/usr/bin/env python
"""
Parser for Elam 2002
"""

# Standard library modules.
import logging

# Third party modules.
import requests


# Local modules.
import pyxray.parser.base as base
from pyxray.descriptor import Reference, Element, XrayTransition
from pyxray.property import (
    AtomicSubshellBindingEnergy,
    XrayTransitionEnergy,
)

# Globals and constants variables.
logger = logging.getLogger(__name__)

DESLATTES2005THEORY = Reference(
    "deslattes2005_theory",
    author="Deslattes, R.D. and Kessler Jr., E.G. and Indelicato, P. and Billy, L. de and Lindroth, E. and Anton, J. "
    "and Coursey, J.S. and Schwab, D.J. and Chang, C. and Sukumar, R. and Olsen, K. and Dragoset, R.A.",
    year="2005",
    title="X-ray Transition Energies (version 1.2)",
    publisher="National Institute of Standards and Technology, Gaithersburg, MD, USA",
    doi="10.18434/T4859Z",
    howpublished="Online",
    url="http://physics.nist.gov/XrayTrans",
)

DESLATTES2005DIRECT = Reference(
    "deslattes2005_direct",
    author="Deslattes, R.D. and Kessler Jr., E.G. and Indelicato, P. and Billy, L. de and Lindroth, E. and Anton, J. "
    "and Coursey, J.S. and Schwab, D.J. and Chang, C. and Sukumar, R. and Olsen, K. and Dragoset, R.A.",
    year="2005",
    title="X-ray Transition Energies (version 1.2)",
    publisher="National Institute of Standards and Technology, Gaithersburg, MD, USA",
    doi="10.18434/T4859Z",
    howpublished="Online",
    url="http://physics.nist.gov/XrayTrans",
)

DESLATTES2005COMBINED = Reference(
    "deslattes2005_combined",
    author="Deslattes, R.D. and Kessler Jr., E.G. and Indelicato, P. and Billy, L. de and Lindroth, E. and Anton, J. "
    "and Coursey, J.S. and Schwab, D.J. and Chang, C. and Sukumar, R. and Olsen, K. and Dragoset, R.A.",
    year="2005",
    title="X-ray Transition Energies (version 1.2)",
    publisher="National Institute of Standards and Technology, Gaithersburg, MD, USA",
    doi="10.18434/T4859Z",
    howpublished="Online",
    url="http://physics.nist.gov/XrayTrans",
)

DESLATTES2005VAPOR = Reference(
    "deslattes2005_vapor",
    author="Deslattes, R.D. and Kessler Jr., E.G. and Indelicato, P. and Billy, L. de and Lindroth, E. and Anton, J. "
    "and Coursey, J.S. and Schwab, D.J. and Chang, C. and Sukumar, R. and Olsen, K. and Dragoset, R.A.",
    year="2005",
    title="X-ray Transition Energies (version 1.2)",
    publisher="National Institute of Standards and Technology, Gaithersburg, MD, USA",
    doi="10.18434/T4859Z",
    howpublished="Online",
    url="http://physics.nist.gov/XrayTrans",
)

_ELEMENT_LOOKUP = {
    "Ne": Element(10),
    "Na": Element(11),
    "Mg": Element(12),
    "Al": Element(13),
    "Si": Element(14),
    "P": Element(15),
    "S": Element(16),
    "Cl": Element(17),
    "Ar": Element(18),
    "K": Element(19),
    "Ca": Element(20),
    "Sc": Element(21),
    "Ti": Element(22),
    "V": Element(23),
    "Cr": Element(24),
    "Mn": Element(25),
    "Fe": Element(26),
    "Co": Element(27),
    "Ni": Element(28),
    "Cu": Element(29),
    "Zn": Element(30),
    "Ga": Element(31),
    "Ge": Element(32),
    "As": Element(33),
    "Se": Element(34),
    "Br": Element(35),
    "Kr": Element(36),
    "Rb": Element(37),
    "Sr": Element(38),
    "Y": Element(39),
    "Zr": Element(40),
    "Nb": Element(41),
    "Mo": Element(42),
    "Tc": Element(43),
    "Ru": Element(44),
    "Rh": Element(45),
    "Pd": Element(46),
    "Ag": Element(47),
    "Cd": Element(48),
    "In": Element(49),
    "Sn": Element(50),
    "Sb": Element(51),
    "Te": Element(52),
    "I": Element(53),
    "Xe": Element(54),
    "Cs": Element(55),
    "Ba": Element(56),
    "La": Element(57),
    "Ce": Element(58),
    "Pr": Element(59),
    "Nd": Element(60),
    "Pm": Element(61),
    "Sm": Element(62),
    "Eu": Element(63),
    "Gd": Element(64),
    "Tb": Element(65),
    "Dy": Element(66),
    "Ho": Element(67),
    "Er": Element(68),
    "Tm": Element(69),
    "Yb": Element(70),
    "Lu": Element(71),
    "Hf": Element(72),
    "Ta": Element(73),
    "W": Element(74),
    "Re": Element(75),
    "Os": Element(76),
    "Ir": Element(77),
    "Pt": Element(78),
    "Au": Element(79),
    "Hg": Element(80),
    "Tl": Element(81),
    "Pb": Element(82),
    "Bi": Element(83),
    "Po": Element(84),
    "At": Element(85),
    "Rn": Element(86),
    "Fr": Element(87),
    "Ra": Element(88),
    "Ac": Element(89),
    "Th": Element(90),
    "Pa": Element(91),
    "U": Element(92),
    "Np": Element(93),
    "Pu": Element(94),
    "Am": Element(95),
    "Cm": Element(96),
    "Bk": Element(97),
    "Cf": Element(98),
    "Es": Element(99),
    "Fm": Element(100),
}

_SUBSHELL_LOOKUP = {
    "K": base.K,
    "L1": base.L1,
    "L2": base.L2,
    "L3": base.L3,
    "M1": base.M1,
    "M2": base.M2,
    "M3": base.M3,
    "M4": base.M4,
    "M5": base.M5,
    "N1": base.N1,
    "N2": base.N2,
    "N3": base.N3,
    "N4": base.N4,
    "N5": base.N5,
    "N6": base.N6,
    "N7": base.N7,
}

_BLEND_LOOKUP = {
    "KL2,3": base.Ka,
    "KM": XrayTransition(3, None, None, base.K),
    "KM2,3": base.Kb1_3,
    "KM4,5": base.Kb5,
    "KN2,3": base.Kb2,
    "KN4,5": base.Kb4,
    "L2,3M1": base.Ll_n,
    "L3M4,5": base.La,
    "L1M2,3": base.Lb3_4,
    "L1N2,3": base.Lg2_3,
    "L3N4,5": base.Lb2_15,
    "L3N6,7": base.Lu,
    "L2N6,7": XrayTransition(4, 3, None, base.L2),
    "L1N4,5": XrayTransition(4, 2, None, base.L1),
    "L1N6,7": XrayTransition(4, 3, None, base.L1),
}

_NUM_ELEMENTS = 91
_URL = "https://physics.nist.gov/cgi-bin/XrayTrans/search.pl?download=tab&element=All&lower=10&upper=1000000&units=eV"

# Column numbers in table
_ELE = 0
_TRANS = 2
_THEORY = 3
_DIRECT = 5
_COMBINED = 7
_VAPOR = 9
_BLEND = 11


class Deslattes2005Parser(base._Parser):
    def __iter__(self):
        r = requests.get(_URL, stream=True)
        r_iter = r.iter_lines()

        # Find the first row and skip the header
        for line in r_iter:
            if line.decode("ascii").startswith("Ele."):
                break

        for line in r_iter:
            row = line.decode("ascii").split("\t")
            element = _ELEMENT_LOOKUP[row[_ELE]]

            transition_str = row[_TRANS]
            if "edge" in transition_str:
                subshell_str = transition_str.split()[0]
                subshell = _SUBSHELL_LOOKUP[subshell_str]

                yield from Deslattes2005Parser._edge_energy_parser(
                    DESLATTES2005THEORY, element, subshell, row[_THEORY]
                )
                yield from Deslattes2005Parser._edge_energy_parser(
                    DESLATTES2005DIRECT, element, subshell, row[_DIRECT]
                )
                yield from Deslattes2005Parser._edge_energy_parser(
                    DESLATTES2005COMBINED, element, subshell, row[_COMBINED]
                )
                yield from Deslattes2005Parser._edge_energy_parser(
                    DESLATTES2005VAPOR, element, subshell, row[_VAPOR]
                )
                if subshell_str == "K":
                    self.update(int((element.z - 9) / _NUM_ELEMENTS * 100))

            else:
                transition = Deslattes2005Parser._get_transition(row[_TRANS])

                blend_str = row[_BLEND]
                blend = _BLEND_LOOKUP[row[_BLEND]] if blend_str else False

                yield from Deslattes2005Parser._transition_energy_parser(
                    DESLATTES2005THEORY, element, transition, row[_THEORY]
                )

                yield from Deslattes2005Parser._transition_energy_parser(
                    DESLATTES2005DIRECT, element, transition, row[_DIRECT]
                )

                # If blend is stipulated (Eg. KL2,3) add the direct measured value also to the blend, but only once
                if blend and (
                    transition_str in blend_str
                    or (blend_str == "KM" and transition_str == "KM1")
                    or (blend_str == "L2,3M1" and transition_str == "L2M1")
                ):
                    yield from Deslattes2005Parser._transition_energy_parser(
                        DESLATTES2005DIRECT, element, blend, row[_DIRECT]
                    )

    @staticmethod
    def _get_transition(transition_str):
        if transition_str[0] == "K":
            return XrayTransition(_SUBSHELL_LOOKUP[transition_str[1:]], base.K)
        return XrayTransition(
            _SUBSHELL_LOOKUP[transition_str[2:]], _SUBSHELL_LOOKUP[transition_str[:2]]
        )

    @staticmethod
    def _transition_energy_parser(reference, element, transition, value_ev_str):
        if value_ev_str:
            prop = XrayTransitionEnergy(
                reference, element, transition, float(value_ev_str)
            )
            logger.debug(f"Parsed: {prop}")
            yield prop

    @staticmethod
    def _edge_energy_parser(reference, element, subshell, value_ev_str):
        if value_ev_str:
            prop = AtomicSubshellBindingEnergy(
                reference, element, subshell, float(value_ev_str)
            )
            logger.debug(f"Parsed: {prop}")
            yield prop
