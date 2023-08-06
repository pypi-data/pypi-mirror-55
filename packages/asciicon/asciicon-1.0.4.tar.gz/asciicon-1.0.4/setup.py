from setuptools import setup

setup(
    name='asciicon',
    version='1.0.4',
    include_package_data=True,
    packages=['asciicon'],
    install_requires=[
        'click', 'colorama'
    ],
    entry_points={
        'console_scripts': ['asciicon = asciicon.cli:start']
      }
)
