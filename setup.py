from setuptools import setup

VERSION = '2.0.0'

setup(
    name='AsisTutor',
    version=VERSION,
    description='N/A',
    author='Juan David Garay',
    author_email='j.garay@kodland.team',
    packages=['mi_app'],
    install_requires=[
        # Lista de dependencias si las tienes
    ],
    entry_points={
        'console_scripts': [
            'mi_app = __main__:main',
        ],
    },
    # Otros metadatos...
)
