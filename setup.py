from setuptools import setup, find_packages

setup(
    name='klaht',
    version='0.1.0',
    author='A. Santana-Bonilla',
    author_email='k2031560@kcl.ac.uk',
    packages=find_packages(include=['klaht','klaht.*']),
    install_requires=[
        'jinja2',
        'wheel',
    ],
)
