# Cactus Test Definitions

This repository contains YAML test procedure definitions for use with the CSIP-AUS Client Test Harness.

This repository also provides Python dataclasses to make it easier for Python code to work with these definitions. In addition, there are also helper functions for creating valid instances of these dataclasses directly from the YAML test procedure definition files.

## Testing

This repository also contains a small number of tests that verify that test definitions can be sucessfully converted to their equivalent python dataclasses.

First install the development and testing dependencies with,

```sh
python -m pip install --editable .[dev,test]
```

Once installed, run the tests with,

```sh
pytest
```
