from setuptools import setup

setup(
    name='asciicons',
    version='1.0',
    py_modules=['asciicon'],
    include_package_data=True,
    
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        asciicon=asciicon.pray:cli
    ''',
)
