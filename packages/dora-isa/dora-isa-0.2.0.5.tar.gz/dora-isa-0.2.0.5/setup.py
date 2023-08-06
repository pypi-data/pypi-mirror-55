import os
import sys
from distutils.sysconfig import get_python_lib
from setuptools import setup, Extension

relative_site_packages = get_python_lib().split(sys.prefix + os.sep)[1]
date_files_relative_path = os.path.join(relative_site_packages, "dora")

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dora-isa",
    version="0.2.0.5",
    packages=[
        'dora',
        'dora/interface',
        'dora/template/cp/score',
    ],
    data_files=[
        (date_files_relative_path + "/template", ['dora/template/Dockerfile']),
        (date_files_relative_path + "/template/cp/score", ['dora/template/cp/score/run.sh'])
    ],
    author="didone",
    url="http://www.compasso.com.br",
    author_email="tiago.didone@compasso.com.br",
    description="SQL Parser for Dora Project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)