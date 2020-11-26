#!/usr/bin/env python

# Standard library modules.
from pathlib import Path
import logging

# Third party modules.
from setuptools import setup, find_packages
import setuptools.command.build_py as _build_py

# Local modules.
import versioneer

# Globals and constants variables.
BASEDIR = Path(__file__).parent.resolve()
logger = logging.getLogger("pyxray")


class build_py(_build_py.build_py):
    def run(self):
        # Build SQL database
        import sqlalchemy
        import pyxray.sql.build

        logging.basicConfig()
        logger.setLevel(logging.INFO)

        filepath = BASEDIR.joinpath("pyxray", "data", "pyxray.db").resolve()
        if filepath.exists():
            filepath.unlink()

        engine = sqlalchemy.create_engine("sqlite:///" + str(filepath))
        builder = pyxray.sql.build.SqlDatabaseBuilder(engine)
        builder.build()

        try:
            del self.data_files  # Force reinitialization of files to copy
        except AttributeError:
            pass

        super().run()


with open(BASEDIR.joinpath("README.rst"), "r") as fp:
    LONG_DESCRIPTION = fp.read()

PACKAGES = find_packages()

PACKAGE_DATA = {"pyxray": ["data/pyxray.db"]}

with open(BASEDIR.joinpath("requirements.txt"), "r") as fp:
    INSTALL_REQUIRES = fp.read().splitlines()

EXTRAS_REQUIRE = {}
with open(BASEDIR.joinpath("requirements-dev.txt"), "r") as fp:
    EXTRAS_REQUIRE["dev"] = fp.read().splitlines()
with open(BASEDIR.joinpath("requirements-test.txt"), "r") as fp:
    EXTRAS_REQUIRE["test"] = fp.read().splitlines()

CMDCLASS = versioneer.get_cmdclass()
CMDCLASS["build_py"] = build_py

ENTRY_POINTS = {
    "pyxray.parser": [
        "element symbol = pyxray.parser.notation:ElementSymbolParser",
        "atomic shell notation = pyxray.parser.notation:AtomicShellNotationParser",
        "atomic subshell notation = pyxray.parser.notation:AtomicSubshellNotationParser",
        "generic x-ray transition notation = pyxray.parser.notation:GenericXrayTransitionNotationParser",
        "known x-ray transition notation = pyxray.parser.notation:KnownXrayTransitionNotationParser",
        "series x-ray transition notation = pyxray.parser.notation:SeriesXrayTransitionNotationParser",
        "family x-ray transition notation = pyxray.parser.notation:FamilyXrayTransitionNotationParser",
        "wikipedia element name = pyxray.parser.wikipedia:WikipediaElementNameParser",
        "sargent-welch element atomic weight = pyxray.parser.sargent_welch:SargentWelchElementAtomicWeightParser",
        "sargent-welch element mass density = pyxray.parser.sargent_welch:SargentWelchElementMassDensityParser",
        "perkins1991 = pyxray.parser.perkins1991:Perkins1991Parser",
        "nist atomic weight = pyxray.parser.nist:NISTElementAtomicWeightParser",
        "jeol transition = pyxray.parser.jeol:JEOLTransitionParser",
        "campbell2001 = pyxray.parser.campbell2001:CampbellAtomicSubshellRadiativeWidthParser",
        "dtsa1992 subshell = pyxray.parser.dtsa:DtsaSubshellParser",
        "dtsa1992 transition = pyxray.parser.dtsa:DtsaLineParser",
        "elam2002 = pyxray.parser.elam2002:Elam2002Parser",
        "chantler2005 = pyxray.parser.chantler2005:Chantler2005Parser",
        "deslattes2005 = pyxray.parser.deslattes2005:Deslattes2005Parser",
    ],
}

setup(
    name="pyxray",
    version=versioneer.get_version(),
    url="https://github.com/openmicroanalysis/pyxray",
    author="Philippe T. Pinard",
    author_email="philippe.pinard@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    description="Definitions and properties of X-ray transitions",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    license="MIT license",
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    cmdclass=CMDCLASS,
    entry_points=ENTRY_POINTS,
)
