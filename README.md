# Zenith Greeter

A small, dependency-free Python package demonstrating how to build, test, and publish a reusable class.

## Installation

After the package is published to PyPI:

```bash
python -m pip install zenith-greeter
```

For local development from the project directory:

```bash
python -m pip install -e .
```

## Quick start

```python
from zenith_greeter import Greeter

person = Greeter("Awwal")
print(person.greet())
# Hello, Awwal! Welcome to Python packages.
```

## Customize the greeting

```python
from zenith_greeter import Greeter

person = Greeter(
    name="Ada",
    greeting="Hi",
    welcome_message="Good to see you.",
)
print(person.greet())
# Hi, Ada! Good to see you.
```

A missing or blank name defaults to `there`. The greeting phrase must not be blank. Set `welcome_message=""` to omit the final message. Non-string arguments raise `TypeError` rather than failing later in the program.

## Run the tests

From the project root, install the package in editable mode and run the tests:

```bash
python -m pip install -e .
python -m unittest discover -s tests -v
```

The package uses Python's built-in `unittest` framework and has no runtime dependencies.
