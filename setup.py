from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='git-repo-sync',
    version='0.1.0',
    description='Sync repositories',
    url='https://gitlab.com/paulgessinger/git-repo-sync',
    license='MIT',

    author='Paul Gessinger',

    author_email='hello@paulgessinger.com',

    packages=find_packages(exclude=[]),
    package_data={
    },

    entry_points = {
        'console_scripts': ["reposync=git_repo_sync.cli:main"]
    },

    install_requires=['PyYAML', 'gitpython', 'schema'],
    tests_require = ['pytest']
)
