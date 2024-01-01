from setuptools import setup
from __version__ import __version__



setup(
    name='AsisTutor',
    version=__version__,
    description='N/A',
    author='Juan David Garay',
    author_email='j.garay@kodland.team',
    packages=['mi_app'],
    install_requires=[
    ],
    entry_points={
        'console_scripts': [
            'mi_app = __main__:main',
        ],
    },
)
