import setuptools

setuptools.setup(
    name='justblast',
    version='2019.0.2',
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
    dependency_links=['https://github.com/timkahlke/BASTA#BASTA']
)
