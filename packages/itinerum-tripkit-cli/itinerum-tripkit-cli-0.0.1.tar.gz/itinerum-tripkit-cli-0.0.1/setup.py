import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='itinerum-tripkit-cli',
    version='0.0.1',
    author='Kyle Fitzsimmons',
    author_email='kafitz22@gmail.com',
    description='A command-line interface for running the itinerum-tripkit library',
    py_modules=['cli'],
    install_requires=[
        'Click',
        'itinerum-tripkit==0.0.4',
    ],
    entry_points='''
        [console_scripts]
        tripkit-cli=tripkit_cli:main
    ''',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/TRIP-Lab/itinerum-tripkit-cli',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',    
)
