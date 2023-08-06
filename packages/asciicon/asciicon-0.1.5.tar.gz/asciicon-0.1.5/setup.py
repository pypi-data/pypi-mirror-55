from setuptools import setup

setup(
    name='asciicon',
    version='0.1.5',
    py_modules=['asciicon'],
    include_package_data=True,
    package_data={'': ['*.txt']},
    install_requires=[
        'click',
    ],
    entry_points={
        'console_scripts': ['asciicon = asciicon.cli:start']
      }
)
