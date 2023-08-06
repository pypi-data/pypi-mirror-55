# bzar-python

A python implementation for [the bzar format](https://github.com/gwappa/bzar).

![DOI:10.5281/zenodo.3531852](https://zenodo.org/badge/doi/10.5281/zenodo.3531852.svg)

## Installation

```
pip install bzar
```

Alternatively, you can also clone this repository and perform `pip install .` inside.

## Basic usage

```
import numpy as np
import bzar

orig = np.arange(10).reshape((2,5))
bzar.save('out', orig, dict(desc="test")) # output saved to 'out.bzar', with optional metadata

read, meta = bzar.load('out.bzar', with_metadata=True) # reads the content of file as an array
```

## License

The MIT license
