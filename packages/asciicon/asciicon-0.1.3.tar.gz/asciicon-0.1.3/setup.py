from setuptools import setup

setup(
    name='asciicon',
    version='0.1.3',
    py_modules=['asciicon'],
    include_package_data=True,
    package_data={'asciicon': ['asciicons/icons/*.txt']},
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': ['asciicon = asciicon.cli:start']
      }
)
