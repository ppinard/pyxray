""""""

# Standard library modules.

# Third party modules.
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy import Column, Integer, Unicode, String, ForeignKey, Float
from sqlalchemy.orm import relationship, synonym

# Local modules.

# Globals and constants variables.

Base = declarative_base()

#--- Mix-ins

class PrimaryKeyMixin(object):

    id = Column(Integer, primary_key=True)

class ReferenceMixin(object):
    """
    A mixin for models that require a reference.
    """

    @declared_attr
    def reference_id(cls): #@NoSelf
        return Column(Integer, ForeignKey('refs.id'), nullable=False)

    @declared_attr
    def reference(cls): #@NoSelf
        return relationship('Reference')

class NotationMixin(object):

    value = Column(String, nullable=False)
    value_html = Column(String)
    value_latex = Column(String)

    @declared_attr
    def notation_type_id(cls): #@NoSelf
        return Column(Integer, ForeignKey('notation_type.id'), nullable=False)

    @declared_attr
    def notation_type(cls): #@NoSelf
        return relationship('NotationType')

class ElementPropertyMixin(object):
    """
    A mixin for models representing an element property.
    """

    @declared_attr
    def element_id(cls): #@NoSelf
        return Column(Integer, ForeignKey('element.id'), nullable=False)

    @declared_attr
    def element(cls): #@NoSelf
        return relationship('Element')

class AtomicShellPropertyMixin(object):

    @declared_attr
    def atomic_shell_id(cls): #@NoSelf
        return Column(Integer, ForeignKey('atomic_shell.id'), nullable=False)

    @declared_attr
    def atomic_shell(cls): #@NoSelf
        return relationship('AtomicShell')

class AtomicSubshellPropertyMixin(object):

    @declared_attr
    def atomic_subshell_id(cls): #@NoSelf
        return Column(Integer, ForeignKey('atomic_subshell.id'), nullable=False)

    @declared_attr
    def atomic_subshell(cls): #@NoSelf
        return relationship('AtomicSubshell')

class TransitionPropertyMixin(object):

    @declared_attr
    def xray_transition_id(cls): #@NoSelf
        return Column(Integer, ForeignKey('transition.id'), nullable=False)

    @declared_attr
    def xray_transition(cls): #@NoSelf
        return relationship('Transition')

#--- Helper

class Reference(PrimaryKeyMixin, Base):
    """
    Table to store references. 
    The columns are based on BibTeX.
    """

    __tablename__ = 'refs'

    bibtexkey = Column(String(256), nullable=False)
    author = Column(Unicode)
    year = Column(Unicode)
    title = Column(Unicode)
    type = Column(Unicode)
    booktitle = Column(Unicode)
    editor = Column(Unicode)
    pages = Column(Unicode)
    edition = Column(Unicode)
    journal = Column(Unicode)
    school = Column(Unicode)
    address = Column(Unicode)
    url = Column(Unicode)
    note = Column(Unicode)
    number = Column(Unicode)
    series = Column(Unicode)
    volume = Column(Unicode)
    publisher = Column(Unicode)
    organization = Column(Unicode)
    chapter = Column(Unicode)
    howpublished = Column(Unicode)
    doi = Column(Unicode)

    def __repr__(self):
        return '<Reference({0})>'.format(self.bibtexkey)

    def __str__(self):
        return self.bibtexkey

class NotationType(ReferenceMixin, Base):

    __tablename__ = 'notation_type'

    id = Column(Integer, primary_key=True)
    name = Column(String(collation='NOCASE'), nullable=False)

    def __repr__(self):
        return '<NotationType({0})>'.format(self.name)

    def __str__(self):
        return self.name

#--- Element

class Element(PrimaryKeyMixin, Base):

    __tablename__ = 'element'

    z = Column(Integer, nullable=False)
    symbol = Column(String(3, collation='NOCASE'), nullable=False)

    def __repr__(self):
        return '<Element({0})>'.format(self.symbol)

    def __str__(self):
        return self.symbol

class ElementNameProperty(PrimaryKeyMixin,
                          ElementPropertyMixin,
                          ReferenceMixin,
                          Base):
    """
    Table to store the name of each element in different languages.
    """

    __tablename__ = 'element_name'

    name = Column(Unicode(256, collation='NOCASE'), nullable=False)
    language_code = Column(String(2, collation='NOCASE'), nullable=False)

class ElementAtomicWeightProperty(PrimaryKeyMixin,
                                  ElementPropertyMixin,
                                  ReferenceMixin,
                                  Base):
    """
    Table to store the atomic weight of each element.
    """

    __tablename__ = 'element_atomic_weight'

    value = Column(Float, nullable=False)

class ElementMassDensityProperty(PrimaryKeyMixin,
                                 ElementPropertyMixin,
                                 ReferenceMixin,
                                 Base):
    """
    Table to store the mass density of each element.
    """

    __tablename__ = 'element_mass_density'

    value_kg_per_m3 = Column(Float, nullable=False)

#--- Atomic shell

class AtomicShell(PrimaryKeyMixin, Base):

    __tablename__ = 'atomic_shell'

    principal_quantum_number = Column(Integer, nullable=False)

    n = synonym("principal_quantum_number")

    def __repr__(self):
        return '<AtomicShell({0:d}>'.format(self.n)

    def __str__(self):
        return '{0:d}'.format(self.n)

class AtomicShellNotationProperty(PrimaryKeyMixin,
                                  AtomicShellPropertyMixin,
                                  NotationMixin,
                                  Base):

    __tablename__ = 'atomic_shell_notation'

#--- Atomic subshell

class AtomicSubshell(PrimaryKeyMixin, AtomicShellPropertyMixin, Base):

    __tablename__ = 'atomic_subshell'

    azimuthal_quantum_number = Column(Integer, nullable=False)
    total_angular_momentum_n = Column(Integer, nullable=False)

    @declared_attr
    def total_angular_momentum(self):
        return self.total_angular_momentum_n / 2

    l = synonym("azimuthal_quantum_number")
    j = synonym("total_angular_momentum")
    j_n = synonym("total_angular_momentum_n")

    def __repr__(self):
        return '<AtomicSubshell(n={0:d}, l={1:d}, j={2:d}/2)>'\
                .format(self.atomic_shell.n, self.l, self.j_n)

    def __str__(self):
        return '({0:d},{1:d},{2:d})'\
                .format(self.atomic_shell.n, self.l, self.j_n)

class AtomicSubshellNotationProperty(PrimaryKeyMixin,
                                     AtomicSubshellPropertyMixin,
                                     NotationMixin,
                                     Base):

    __tablename__ = 'atomic_subshell_notation'

class AtomicSubshellEdgeEnergyProperty(PrimaryKeyMixin,
                                       AtomicShellPropertyMixin,
                                       ElementPropertyMixin,
                                       ReferenceMixin,
                                       Base):

    __tablename__ = 'atomic_subshell_edge_energy'

    value_eV = Column(Float, nullable=False)

class AtomicSubshellNaturalWidthProperty(PrimaryKeyMixin,
                                         AtomicShellPropertyMixin,
                                         ElementPropertyMixin,
                                         ReferenceMixin,
                                         Base):

    __tablename__ = 'atomic_subshell_natural_width'

    value_eV = Column(Float, nullable=False)

class AtomicSubshellOccupancyProperty(PrimaryKeyMixin,
                                      AtomicShellPropertyMixin,
                                      ElementPropertyMixin,
                                      ReferenceMixin,
                                      Base):

    __tablename__ = 'atomic_subshell_occupancy'

    value = Column(Integer, nullable=False)

#--- Transition

class Transition(PrimaryKeyMixin, Base):

    __tablename__ = 'transition'

    source_id = Column(Integer, ForeignKey('atomic_subshell.id'), nullable=False)
    source = relationship('AtomicSubshell',
                          foreign_keys=source_id)

    destination_id = Column(Integer, ForeignKey('atomic_subshell.id'), nullable=False)
    destination = relationship('AtomicSubshell',
                               foreign_keys=destination_id)

    secondary_destination_id = Column(Integer, ForeignKey('atomic_subshell.id'))
    secondary_destination = relationship('AtomicSubshell',
                                         foreign_keys=secondary_destination_id)

    def is_radiative(self):
        return self.secondary_destination is None

    def is_nonradiative(self):
        return not self.is_radiative()

    def is_coster_kronig(self):
        return self.source.n == self.destination.n

class TransitionNotationProperty(PrimaryKeyMixin,
                                 TransitionPropertyMixin,
                                 NotationMixin,
                                 Base):

    __tablename__ = 'transition_notation'

class TransitionEnergyProperty(PrimaryKeyMixin,
                               TransitionPropertyMixin,
                               ElementPropertyMixin,
                               ReferenceMixin,
                               Base):

    __tablename__ = 'transition_energy'

    value_eV = Column(Float, nullable=False)

class TransitionProbabilityProperty(PrimaryKeyMixin,
                                    TransitionPropertyMixin,
                                    ElementPropertyMixin,
                                    ReferenceMixin,
                                    Base):

    __tablename__ = 'transition_probability'

    value = Column(Float, nullable=False)
