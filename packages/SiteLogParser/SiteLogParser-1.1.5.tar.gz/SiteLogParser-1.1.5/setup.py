# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

import setuptools
import os
#import versioneer

from io import open

here = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

with open(os.path.join(here, 'LICENSE.txt'), encoding='utf-8') as f:
    license_text = f.read()

setuptools.setup(
    name='SiteLogParser',
    version='1.1.5', 
    #version=versioneer.get_version(),
    #cmdclass=versioneer.get_cmdclass(),
    description='Parsing IGS Sitelog files (supports version 2+3)',
    long_description=readme,
    long_description_content_type='text/markdown',
    author='Juergen Fredriksson',
    author_email='juergen.fredriksson@bev.gv.at',
    url='https://gitlab.com/dach.pos/sitelogparser',
    # license=license_text,
    # packages=['sitelog_parser'],
    packages=setuptools.find_packages(exclude=('tests', 'docs', 'env', '.vscode')),
    #package_data={'': ['LICENSE.txt']},
    #package_dir={'sitelogparser': 'src/sitelogparser'},
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, <4',
    keywords='sitelog parser gnss gps galileo beidou glonass',
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Operating System :: POSIX :: Linux",
    ]
)
