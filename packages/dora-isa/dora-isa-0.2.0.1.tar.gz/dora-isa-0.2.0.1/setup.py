from setuptools import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="dora-isa",
    version="0.2.0.1",
    packages=[
        'dora',
        'dora/interface',
        'dora/template/cp/score',
    ],
    data_files=[
        ('', ['dora/template/Dockerfile']),
        ('', ['dora/template/cp/score/run.sh'])
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