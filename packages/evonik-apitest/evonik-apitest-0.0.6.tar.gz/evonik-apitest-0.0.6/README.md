# `apitest`

This repo contains the python module `apitest`.
It is publically available as the package `evonik-apitest`.

## repo structure

```
code/              # source code of apitest
examples/          # examples for the use of apitest
notebooks/         # notebooks with examples and doc
```

## installation

```
pip install evonik-apitest
```

## usage

```
from apitest import Property, Properties, Endpoints
from apitest import Component, Instance, ComponentTest
from apitest.util import rand_str, rand_int
...
```

## build & upload

```
python3 setup.py sdist bdist_wheel --universal
twine upload dist/*
```

## tests

To test the current implementation, execute the following:

```
pytest \
    apitest/component.py \
    apitest/component_test.py \
    apitest/endpoints.py \
    apitest/instance.py \
    apitest/properties.py \
    apitest/property.py \
    apitest/util.py
```