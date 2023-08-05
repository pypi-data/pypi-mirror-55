import os
import sys
import codecs
import re

import setuptools


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


dynamic_setup_params = {
    # dynamically generated params
    'version': find_version('cherrypy_ask_sdk', '__init__.py'),
    'install_requires': [
        line.strip() for line in read("requirements.txt").splitlines()
    ],
}

setuptools.setup(**dynamic_setup_params)
