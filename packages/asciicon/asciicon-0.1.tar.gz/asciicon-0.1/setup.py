from setuptools import setup

setup(
    name='asciicon',
    version='0.1',
    py_modules=['asciicon'],
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        asciicon=asciicon:cli
    ''',
)
