#!/usr/bin/env python
""" """

# Standard library modules.

# Third party modules.
import pytest

# Local modules.
import pyxray.descriptor as descriptor
from pyxray.sql.data import SqlDatabase, NotFound
import pyxray.data

# Globals and constants variables.
K = descriptor.AtomicSubshell(1, 0, 1)
L3 = descriptor.AtomicSubshell(2, 1, 3)
L2 = descriptor.AtomicSubshell(2, 1, 1)


@pytest.fixture(scope="session")
def database(builder):
    return SqlDatabase(builder.engine)


@pytest.fixture
def database_real(tmp_path):
    return pyxray.data.database


@pytest.mark.parametrize("element", [118, "Vi", "Vibranium"])
def test_element(database, element):
    assert database.element(element) == descriptor.Element(118)


@pytest.mark.parametrize("reference", ["lee1966", "LEE1966"])
def test_reference(database, reference):
    assert database.element_name(118, "en", reference) == "Vibranium"


@pytest.mark.parametrize("element", ["Al", 13, "Aluminum"])
def test_element_notfound(database, element):
    with pytest.raises(NotFound):
        database.element(element)


@pytest.mark.parametrize("element", [118, "Vi", "Vibranium"])
def test_element_atomic_number(database, element):
    assert database.element_atomic_number(element) == 118


@pytest.mark.parametrize("element", ["Al", 13, "Aluminum"])
def test_element_atomic_number_notfound(database, element):
    with pytest.raises(NotFound):
        database.element_atomic_number(element)


@pytest.mark.parametrize("element", [118, "Vi", "Vibranium"])
def test_element_symbol(database, element):
    assert database.element_symbol(element) == "Vi"


@pytest.mark.parametrize("element", ["Al", 13, "Aluminum"])
def test_element_symbol_notfound(database, element):
    with pytest.raises(NotFound):
        database.element_symbol(element)


@pytest.mark.parametrize("element", [118, "Vi", "Vibranium"])
def test_element_name(database, element):
    assert database.element_name(element, "en") == "Vibranium"
    assert database.element_name(element, "en", "lee1966") == "Vibranium"


@pytest.mark.parametrize("element", ["Al", 13, "Aluminum"])
def test_element_name_notfound(database, element):
    with pytest.raises(NotFound):
        database.element_name(element, "en")


def test_element_name_notfound_wrong_language(database):
    with pytest.raises(NotFound):
        database.element_name(118, "fr")


def test_element_name_notfound_wrong_reference(database):
    with pytest.raises(NotFound):
        database.element_name(118, "en", "doe2016")


def test_element_atomic_weight_no_reference(database):
    # doe2016 (111.1) takes precedence over lee1966 (999.1) because it is newer
    assert database.element_atomic_weight(118) == pytest.approx(111.1, abs=1e-2)


def test_element_atomic_weight_lee1966(database):
    assert database.element_atomic_weight(118, "lee1966") == pytest.approx(
        999.1, abs=1e-2
    )


def test_element_atomic_weight_doe2016(database):
    assert database.element_atomic_weight(118, "doe2016") == pytest.approx(
        111.1, abs=1e-2
    )


@pytest.mark.parametrize("element", [118, "Vi", "Vibranium"])
def test_element_mass_density_kg_per_m3(database, element):
    assert database.element_mass_density_kg_per_m3(element) == pytest.approx(
        999.2, abs=1e-2
    )


@pytest.mark.parametrize("element", [118, "Vi", "Vibranium"])
def test_element_mass_density_g_per_cm3(database, element):
    assert database.element_mass_density_g_per_cm3(element) == pytest.approx(
        0.9992, abs=1e-4
    )


@pytest.mark.parametrize("element,reference", [(118, None), (118, "lee1966")])
def test_element_xray_transitions(database, element, reference):
    transitions = database.element_xray_transitions(element, reference=reference)
    assert len(transitions) == 3

    assert descriptor.XrayTransition(L3, K) in transitions
    assert descriptor.XrayTransition(L2, K) in transitions
    assert descriptor.XrayTransition(2, 1, None, K) in transitions


@pytest.mark.parametrize(
    "xray_transition,expected",
    [
        (descriptor.XrayTransition(L3, K), 1),
        (descriptor.XrayTransition(2, 1, None, K), 2),
    ],
)
def test_element_xray_transitions_with_xray_transition(
    database, xray_transition, expected
):
    transitions = database.element_xray_transitions(118, xray_transition)
    assert len(transitions) == expected


@pytest.mark.parametrize(
    "element, expected",
    [
        (13, 14),
        (6, 2),
        (5, 3),
        (4, 3),
        (3, 2),
    ],
)
def test_element_xray_transitions(database_real, element, expected):
    transitions = database_real.element_xray_transitions(element)
    assert len(transitions) == expected


@pytest.mark.parametrize("element,reference", [(118, "unknown"), (1, None)])
def test_element_xray_transitions_notfound(database, element, reference):
    with pytest.raises(NotFound):
        database.element_xray_transitions(element, reference)


def test_element_xray_transition(database):
    transition = database.element_xray_transition(118, "a")
    assert transition == descriptor.XrayTransition(L3, K)


@pytest.mark.parametrize("element,reference", [(1, "a"), (118, "g")])
def test_element_xray_transition_notfound(database, element, reference):
    with pytest.raises(NotFound):
        database.element_xray_transition(element, reference)


@pytest.mark.parametrize("atomic_shell", [1, "a", "b"])
def test_atomic_shell(database, atomic_shell):
    assert database.atomic_shell(atomic_shell) == descriptor.AtomicShell(1)


@pytest.mark.parametrize("atomic_shell", ["c", 3])
def test_atomic_shell_notfound(database, atomic_shell):
    with pytest.raises(NotFound):
        database.atomic_shell(atomic_shell)


@pytest.mark.parametrize(
    "encoding,expected", [("ascii", "a"), ("utf16", "b"), ("html", "c"), ("latex", "d")]
)
def test_atomic_shell_notation(database, encoding, expected):
    assert database.atomic_shell_notation(1, "mock", encoding) == expected


@pytest.mark.parametrize(
    "atomic_subshell", [descriptor.AtomicSubshell(1, 0, 1), (1, 0, 1), "a", "b"]
)
def test_atomic_subshell(database, atomic_subshell):
    assert database.atomic_subshell(atomic_subshell) == descriptor.AtomicSubshell(
        1, 0, 1
    )


@pytest.mark.parametrize("atomic_subshell", ["c", (3, 3, 3)])
def test_atomic_subshell_notfound(database, atomic_subshell):
    with pytest.raises(NotFound):
        database.atomic_subshell(atomic_subshell)


@pytest.mark.parametrize(
    "encoding,expected", [("ascii", "a"), ("utf16", "b"), ("html", "c"), ("latex", "d")]
)
def testatomic_subshell_notation(database, encoding, expected):
    assert (
        database.atomic_subshell_notation(
            descriptor.AtomicSubshell(1, 0, 1), "mock", encoding
        )
        == expected
    )


@pytest.mark.parametrize(
    "atomic_subshell", [descriptor.AtomicSubshell(1, 0, 1), (1, 0, 1), "a", "b"]
)
def test_atomic_subshell_binding_energy_eV(database, atomic_subshell):
    assert database.atomic_subshell_binding_energy_eV(
        118, atomic_subshell
    ) == pytest.approx(0.1, abs=1e-4)


@pytest.mark.parametrize(
    "atomic_subshell", [descriptor.AtomicSubshell(1, 0, 1), (1, 0, 1), "a", "b"]
)
def testatomic_subshell_radiative_width_eV(database, atomic_subshell):
    assert database.atomic_subshell_radiative_width_eV(
        118, atomic_subshell
    ) == pytest.approx(0.01, abs=1e-4)


@pytest.mark.parametrize(
    "atomic_subshell", [descriptor.AtomicSubshell(1, 0, 1), (1, 0, 1), "a", "b"]
)
def testatomic_subshell_nonradiative_width_eV(database, atomic_subshell):
    assert database.atomic_subshell_nonradiative_width_eV(
        118, atomic_subshell
    ) == pytest.approx(0.001, abs=1e-4)


@pytest.mark.parametrize(
    "atomic_subshell", [descriptor.AtomicSubshell(1, 0, 1), (1, 0, 1), "a", "b"]
)
def testatomic_subshell_occupancy(database, atomic_subshell):
    assert database.atomic_subshell_occupancy(118, atomic_subshell) == 1


@pytest.mark.parametrize(
    "xray_transition",
    ["a", ((2, 1, 3), (1, 0, 1)), (L3, K), descriptor.XrayTransition(L3, K)],
)
def test_xray_transition(database, xray_transition):
    assert database.xray_transition(xray_transition) == descriptor.XrayTransition(L3, K)


@pytest.mark.parametrize(
    "encoding,expected", [("ascii", "a"), ("utf16", "b"), ("html", "c"), ("latex", "d")]
)
def test_xray_transition_notation(database, encoding, expected):
    xray_transition = descriptor.XrayTransition(L3, K)
    assert (
        database.xray_transition_notation(xray_transition, "mock", encoding) == expected
    )


@pytest.mark.parametrize(
    "xray_transition",
    ["a", ((2, 1, 3), (1, 0, 1)), (L3, K), descriptor.XrayTransition(L3, K)],
)
def test_xray_transition_energy_eV_KL3(database, xray_transition):
    assert database.xray_transition_energy_eV(118, xray_transition) == pytest.approx(
        0.2, abs=1e-4
    )


@pytest.mark.parametrize(
    "xray_transition",
    ["e", ((2, 1, 1), (1, 0, 1)), (L2, K), descriptor.XrayTransition(L2, K)],
)
def test_xray_transition_energy_eV_KL2(database, xray_transition):
    assert database.xray_transition_energy_eV(118, xray_transition) == pytest.approx(
        0.4, abs=1e-4
    )


@pytest.mark.parametrize(
    "xray_transition",
    ["a", ((2, 1, 3), (1, 0, 1)), (L3, K), descriptor.XrayTransition(L3, K)],
)
def test_xray_transition_probability(database, xray_transition):
    assert database.xray_transition_probability(118, xray_transition) == pytest.approx(
        0.02, abs=1e-4
    )


@pytest.mark.parametrize(
    "xray_transition",
    ["a", ((2, 1, 3), (1, 0, 1)), (L3, K), descriptor.XrayTransition(L3, K)],
)
def test_xray_transition_relative_weight(database, xray_transition):
    assert database.xray_transition_relative_weight(
        118, xray_transition
    ) == pytest.approx(0.002, abs=1e-4)


def test_xray_line(database):
    xrayline = database.xray_line(118, "aa")

    assert xrayline.element.atomic_number == 118
    assert xrayline.iupac == "Vi bb"
    assert xrayline.siegbahn == "Vi bb"
    assert xrayline.energy_eV == pytest.approx(0.2, abs=1e-3)
