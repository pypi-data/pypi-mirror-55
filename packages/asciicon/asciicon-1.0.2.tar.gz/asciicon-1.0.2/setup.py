from setuptools import setup

setup(
    name='asciicon',
    version='1.0.2',
    include_package_data=True,
    packages=['asciicon'],
    #package_data={'asciicon': ['icons/*.txt']},
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': ['asciicon = asciicon.cli:start']
      }
)
