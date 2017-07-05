"""Distribution package setup for floatish."""

from textwrap import dedent

from setuptools import setup

setup(
    name='floatish',
    version='1.0.0',
    description=dedent('''\
        Floatish makes writing clear and maintainable tests for floating
        point artithmetic easier.
    ''').replace('\n', ' ').strip(),
    author='Fergal Hainey',
    author_email='fergal@bfot.co.uk',
    py_modules=[
        'floatish',
        'floatishisclose',
    ],
    url='https://github.com/Riprock/floatish',
    license='Apache-2.0',
)
