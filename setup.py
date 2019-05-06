#!/usr/bin/env python
#
# Copyright (c) Konstantin Taletskiy
# Distributed under the terms of the MIT License.

from setuptools import find_packages, setup

# obtain version of SoS
with open('src/sos_java/_version.py') as version:
    for line in version:
        if line.startswith('__version__'):
            __version__ = eval(line.split('=')[1])
            break

setup(name = "sos-java",
    version = __version__,
    description = 'SoS Notebook extension for Java',
    author = 'Konstantin Taletskiy',
    url = 'https://github.com/LabShare/sos-java',
    author_email = 'konstantin.taletskiy@axleinfo.com',
    maintainer = 'Konstantin Taletskiy',
    maintainer_email = 'konstantin.taletskiy@axleinfo.com',
    license = 'MIT',
    include_package_data = True,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        ],
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    install_requires=[
          'sos>=0.18.0',
          'sos-notebook>=0.18.0'
      ],
    entry_points= '''
[sos_languages]
Java = sos_java.kernel:sos_java
'''
)
