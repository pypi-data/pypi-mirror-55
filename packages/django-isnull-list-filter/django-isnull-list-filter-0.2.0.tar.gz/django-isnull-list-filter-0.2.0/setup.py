#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
from io import open

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Make sure the django.mo file also exists:
try:
    os.chdir('isnull_filter')
    from django.core import management
    management.call_command('compilemessages', stdout=sys.stderr, verbosity=1)
except ImportError:
    if 'sdist' in sys.argv:
        raise
finally:
    os.chdir('..')



def get_version(*file_paths):
    """Retrieves the version from isnull_filter/__init__.py"""
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


version = get_version("isnull_filter", "__init__.py")


if sys.argv[-1] == 'publish':
    try:
        import wheel
        print("Wheel version: ", wheel.__version__)
    except ImportError:
        print('Wheel library missing. Please run "pip install wheel"')
        sys.exit()
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == 'tag':
    print("Tagging the version on git:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-isnull-list-filter',
    version=version,
    description="""Simple list_filter that offers filtering by __isnull.""",
    long_description=readme + '\n\n' + history,
    author='Petr Dlouhý',
    author_email='petr.dlouhy@email.cz',
    url='https://github.com/PetrDlouhy/django-isnull-list-filter',
    packages=[
        'isnull_filter',
    ],
    include_package_data=True,
    install_requires=[],
    license="MIT",
    zip_safe=False,
    keywords='django-isnull-list-filter',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
