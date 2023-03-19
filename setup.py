from setuptools import setup

from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='AgenciBr',
    version='0.1.5',
    license='MIT License',
    author='Thiago Santos',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='tthiagosantos38@gmail.com',
    keywords='Ana, Inemet, Ideam',
    description=u'Package to work with data from brazilian agenci',
    packages=['AgenciBr'],
    install_requires=['matplotlib',"numpy","pandas","requests","datetime","xarray","netCDF4","cfgrib"],)
