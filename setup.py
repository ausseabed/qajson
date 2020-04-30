from setuptools import setup, find_packages

setup(
    name='ausseabed.qajson',
    version='0.0.1',
    url='https://github.com/ausseabed/qajson',
    author=(
        "Lachlan Hurst;"
        "Giuseppe Masetti(UNH,CCOM);"
        "Tyanne Faulkes(NOAA,OCS)"
    ),
    author_email=(
        "lachlan.hurst@gmail.com;"
        "gmasetti@ccom.unh.edu;"
        "tyanne.faulkes@noaa.gov"
    ),
    description='Description of my package',
    packages=find_packages(),
    install_requires=['jsonschema'],
    tests_require=['pytest'],
)
