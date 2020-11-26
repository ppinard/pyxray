#!/usr/bin/env python
"""
Parser for Elam 2002
"""

# Standard library modules.
import logging
import os
import pkgutil

# Third party modules.


# Local modules.
import pyxray.parser.base as base
from pyxray.descriptor import Reference, Element, XrayTransition
from pyxray.property import (
    ElementAtomicWeight,
    ElementMassDensity,
    AtomicSubshellBindingEnergy,
    XrayTransitionEnergy,
    XrayTransitionProbability,
)

# Globals and constants variables.
logger = logging.getLogger(__name__)

ELAM2002 = Reference(
    "elam2002",
    author="Elam, W.T. and Ravel, B.D. and Sieber, J.R.",
    year="2002",
    title="A new atomic database for X-ray spectroscopic calculations",
    journal="Radiation Physics and Chemistry",
    volume="63",
    number="2",
    pages="121-128",
    doi="10.1016/S0969-806X(01)00227-4",
)

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
    "O1": base.O1,
    "O2": base.O2,
    "O3": base.O3,
    "O4": base.O4,
    "O5": base.O5,
    "P1": base.P1,
    "P2": base.P2,
    "P3": base.P3,
}

_TRANSITION_LOOKUP = {
    "Ka1": base.Ka1,
    "Ka2": base.Ka2,
    "Ka3": XrayTransition(base.L1, base.K),
    "Kb1": base.Kb1,
    "Kb2": base.Kb2,
    "Kb3": base.Kb3,
    "Kb4": base.Kb4,
    "Kb5": base.Kb5,
    "La1": base.La1,
    "La2": base.La2,
    "Lb1": base.Lb1,
    "Lb2": base.Lb2,
    "Lb2,15": base.Lb2_15,
    "Lb3": base.Lb3,
    "Lb4": base.Lb4,
    "Lb5": base.Lb5,
    "Lb6": base.Lb6,
    "Lg1": base.Lg1,
    "Lg2": base.Lg2,
    "Lg3": base.Lg3,
    "Lg6": base.Lg6,
    "Ll": base.Ll,
    "Ln": base.Ln,
    "Ma": base.Ma,
    "Mb": base.Mb,
    "Mg": base.Mg,
    "Mz": base.Mz,
}

_MAX_Z = 98


class Elam2002Parser(base._Parser):
    def __iter__(self):
        relpath = os.path.join("..", "data", "ElamDB12.txt")
        content = pkgutil.get_data(__name__, relpath).decode("utf8")

        curr_element = None
        curr_subshell = None
        fluorescence_yield = 0.0
        transition_line_expected = False
        for line in content.splitlines():
            line = line.strip()

            if not line or line[:2] == "//":
                continue

            if transition_line_expected:
                if line.startswith(curr_subshell):
                    yield from Elam2002Parser._transition_line_parser(
                        curr_element, fluorescence_yield, line
                    )
                    continue
                transition_line_expected = False

            if curr_element is not None:
                if line.startswith("Edge"):
                    (
                        curr_subshell,
                        energy_ev,
                        fluorescence_yield,
                    ) = self._extract_edge_data(line)
                    yield from Elam2002Parser._subshell_parser(
                        curr_element, curr_subshell, energy_ev
                    )
                    continue
                if line == "Lines":
                    transition_line_expected = True
                    continue
                if line == "Photo" or line == "Scatter" or line == "EndElement":
                    self.update(int(curr_element.z / _MAX_Z * 100))
                    curr_element = None
                    continue

            if line.startswith("Element"):
                (
                    curr_element,
                    atomic_weight,
                    density_kg_per_m3,
                ) = self._extract_element_data(line)
                if density_kg_per_m3 < 0:
                    print(curr_element.z, density_kg_per_m3)
                yield from Elam2002Parser._element_parser(
                    curr_element, atomic_weight, density_kg_per_m3
                )
                continue

    @staticmethod
    def _extract_element_data(line):
        element_data = line.split()
        element = Element(int(element_data[2]))
        atomic_weight = float(element_data[3])
        density_kg_per_m3 = float(element_data[4]) * 1e3
        return element, atomic_weight, density_kg_per_m3

    @staticmethod
    def _extract_edge_data(line):
        edge_data = line.split()
        return edge_data[1], float(edge_data[2]), float(edge_data[3])

    @staticmethod
    def _element_parser(element, atomic_weight, density_kg_per_m3):
        if atomic_weight > 1e-15:
            prop = ElementAtomicWeight(ELAM2002, element, atomic_weight)
            logger.debug(f"Parsed: {prop}")
            yield prop

        if density_kg_per_m3 > 1e-15:
            prop = ElementMassDensity(ELAM2002, element, density_kg_per_m3)
            logger.debug(f"Parsed: {prop}")
            yield prop

    @staticmethod
    def _subshell_parser(element, subshell, energy_ev):
        prop = AtomicSubshellBindingEnergy(
            ELAM2002, element, _SUBSHELL_LOOKUP[subshell], energy_ev
        )
        logger.debug(f"Parsed: {prop}")
        yield prop

    @staticmethod
    def _transition_line_parser(element, fluorescence_yield, line):
        line_data = line.split()
        transition = _TRANSITION_LOOKUP[line_data[1]]

        energy_ev = float(line_data[2])
        prop = XrayTransitionEnergy(ELAM2002, element, transition, energy_ev)
        logger.debug(f"Parsed: {prop}")
        yield prop

        probability = float(line_data[3]) * fluorescence_yield
        prop = XrayTransitionProbability(ELAM2002, element, transition, probability)
        logger.debug(f"Parsed: {prop}")
        yield prop
