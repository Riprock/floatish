# Floatish

It’s hard to write clear and maintainable tests for code that does
floating point arithmetic. Floatish makes this easier in Python.

```
assert (
    ['test string', 0.1 + 0.2, 4] ==
    ['test string', Floatish(0.3, rel_tol=1e-9), 4]
)
```

The code can be found on GitHub at https://github.com/Riprock/floatish.
You can file bugs with GitHub's issue tracker and contribute to the
project with pull requests. Fergal Hainey can be reached on Twitter
@FerHai for help with using floatish. The project is under the
Apache-2.0 license.


## Installation

Until floatish is released on pypi, you will need to clone the git repo
then do `pip install .`. Alternatively you can do this all in one step
with `pip install git+https://github.com/Riprock/floatish.git`. Floatish
tests run on Python 2.6, 2.7, 3.2, 3.3, 3.4, 3.5, and 3.6. It’s should
be possible for Floatish to work on other Python versions too but those
are the ones that Travis CI supports easily.


## Background

Floating point arithmetic is hard to write good tests for. For example
0.1 + 0.2 isn't 0.3. It's 0.30000000000000004. All the tests you write
involving floating points will require a bit of extra effort.

One way is to compare your number to the closest possible floating point
number. e.g.:

```
assert 0.1 + 0.1 + 0.1 == 0.30000000000000004
```

That's not great because it makes your test harder to understand. Where
is this magic number coming from? It's harder to maintain too as you
will have to find the nearest possible floating point number every time
you change the value. It's also inconsistent because as long as you
don't do any arithmetic floating points mostly act as you would expect.
For example if you pass 0.3 to a function but don’t do any arithmetic
with it this will raise an AssertionError:

```
assert 0.3 == 0.30000000000000004
```

but this works fine:

```
assert 0.3 == 0.3
```

so you will need to change the value you use if you start/stop doing
arithmetic with passed in floats.

Another method is to see if the floats are equal for a given tolerance.
Don't worry, you don't have to do 0.299 < x < 0.301 every time you use
0.3, Python 3.5 has the built in math.isclose function. This way makes
maintaining your tests easier, but still isn't very clear. The best
tests compare with literal values and only have one assertion per test.
If you want to compare against a collection containing a float then you
will need to make multiple assertions to account the for special float
comparison outside of comparing the collection simply with ==.

Floatish solves the problem of easy tolerance based comparisons inside
collections by helping you make an object that will use math.isclose
when you do == with it and a float. Floatish also includes a
reimplementation of math.isclose for Python versions under 3.5.

Instead of writing:

```
from math import isclose
from unittest.mock import ANY

list_under_test = ['hey', 0.1 + 0.2, 2]
assert list_under_test == ['hey', ANY, 2]
assert isclose(list_under_test[1], 0.3, rel_tol=0.000000000000001)
```

You can write:

```
from floatish import Floatish

assert (
	['hey', 0.1 + 0.2, 2] ==
	['hey', Floatish(0.3, rel_tol=1e-15), 2]
)
```


## Contributing

Please feel free to contribute code, documentation, tests, or anything
else to Floatish. I (Fergal Hainey) aim to give feedback on GitHub pull
requests within 2 weeks of them being submitted. I should ask in the
pull request discussion to confirm you are OK with including your
contribution under the current license.

### Running tests

The easiest way to run unit tests and linters is with tox targeting just
the Python 3.6 environment with the command `tox -e py36`. This assumes
you are using Python 3.6 and have installed [tox]. Linters are not run
for other environments because it’s hard to install compatible versions
of the linters and the extra value will be minimal.

To run tests for other versions of Python you can either wait until you
make a pull request and see the results in Travis CI, or you run them
locally with some extra effort. You will need all the tested Python
versions installed. I like to use [pyenv] to make installing and
managing Python versions easier. When using pyenv you also need to make
Python versions active to use them. You can activate multiple versions
so tox can use them with a command like `pyenv shell 3.6.1 2.7.13 2.5.6
2.6.9 3.0.1 3.1.5 3.2.6 3.3.6 3.4.6 3.5.3`. Next make sure you are using
a version of virtualenv less than 14, higher versions are not compatible
with Python 3.2 and tox uses the virtualenv package version you are
currently using to create the test environments. You can downgrade
the virtualenv package with the command `pip install 'virtualenv<14'`
but it’s best to make sure you do that in a virtual env so you only use
an older virtualenv package when you have to. Once you have all the
dependencies you can just run `tox` to run tests for all Python
versions.

[tox]: https://tox.readthedocs.io/en/latest/
[pyenv]: https://github.com/pyenv/pyenv

### Test coverage

There are no requirements for a specific level of test coverage for
contributions to be accepted, but integration with coverage tools is
included to make it easier for authors to write tests for their changes.
After running tox—and if you have [coverage] installed—you can use
`coverage report` or `coverage html` to see if there’s anything you
missed that you think would benefit from test coverage. Coverage for the
latest version on PyPI/the master branch is on [coveralls].

[coverage]: http://coverage.readthedocs.io/en/latest/
[coveralls]: https://coveralls.io/github/Riprock/floatish

### Floatish versioning

Floatish uses [semantic versioning]. Any merges to the master branch
will be deployed to PyPI, assuming the build on Travis CI passes. For
this reason all pull requests should include updating the version in
setup.py by at least a patch version. Updates to the version number are
not made automatically so as to encourage authors to think about the
type of change they are making. Please update the minor version for any
improvements and the major version whenever a change is not backwards
compatible. New major version numbers do not need to be reserved for
milestone releases.

[semantic versioning]: http://semver.org/
