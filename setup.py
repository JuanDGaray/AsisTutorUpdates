from setuptools import setup, find_packages
from __version__ import __version__

with open('requirements.txt') as f:
    required = f.read().splitlines()


setup(
    name='AsisTutor',
    version=__version__,
    packages=find_packages(),
    install_requires=required,
    entry_points={
        'console_scripts': [
            'AsisTutor=Asistutor.main:main',
        ],
    },
    author='Juan Garay',
    author_email='juandam594@gmail.com',
    description='Descripción de tu aplicación',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/JuanDGaray/AsisTutorUpdates',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)