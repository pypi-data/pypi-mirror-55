# `apitest`

This repo contains the python module `apitest`.

## repo structure

```
code/              # source code of apitest
examples/          # examples for the use of apitest
notebooks/         # notebooks with examples and doc
```

## usage

```
import sys
sys.path.append("../code")

from apitest import Property, Properties, Endpoints
from apitest import Component, Instance, ComponentTest
from apitest import rand_str, rand_int

...
```