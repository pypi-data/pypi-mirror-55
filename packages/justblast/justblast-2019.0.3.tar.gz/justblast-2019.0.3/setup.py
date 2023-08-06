import setuptools
from justblast.__version__ import version
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
setuptools.setup(
    name='justblast',
    version=version,
    packages=setuptools.find_packages() + ['justblast'],
    url='https://github.com/jshleap/justblast',
    license='GNU v3',
    author='jshleap',
    scripts=['bin/justblast'],
    author_email='jshleap@gmail.com',
    description='Simple program to more efficiently run blast in multicore '
                'systems, as well as rough taxonomomic annoation using BASTA '
                'LCA',
    python_requires='>=3.6',
    install_requires=['cycler==0.10.0', 'joblib==0.14.0', 'kiwisolver==1.1.0',
                      'matplotlib==3.1.1', 'numpy==1.17.4', 'pandas==0.25.3',
                      'plyvel==1.1.0', 'pyparsing==2.4.5', 'pytz==2019.3',
                      'python-dateutil==2.8.1', 'six==1.13.0', 'tqdm==4.38.0'],
    dependency_links=['https://github.com/timkahlke/BASTA#BASTA'],
    long_description=long_description,
    long_description_content_type='text/markdown'
)
