# Gravitational Wave utilities in Python
The `gravtools` module is a complementary module to the existing, well-written libraries
[pycbc](https://pycbc.org/) and [gwpy](https://gwpy.github.io/). This package began as a few simple utilities, such as constants
and date conversion helper functions.

[![Build Status](https://travis-ci.com/JWKennington/gravtools.svg?branch=master)](https://travis-ci.com/JWKennington/gravtools) 

## Useful Constants
The `gravtools` package includes some human-readable, enumerated constants for key components of 
the `PyCBC` module structure, such as Detector names and Merger parameter names. This is made 
necessary since `PyCBC` often relies on a lazy-loading pattern for attributes, using the `setattr` 
function to assign attributes to primary classes like `Merger`. Unfortunately, this makes these 
attributes uninspectable by most IDEs. Also the names of these attributes are occasionally less-than-legible.  

```python
>>> from gravtools import MergerParameters, Observatory
>>> Observatory.LIGOHanford
'H1'

>>> MergerParameters.RadiatedEnergy, MergerParameters.FinalSpin
('E_rad', 'a_final')
```

## Time Conversion
Gravitational wave data uses GPS time format, which is a float number of seconds since the
GPS era. The `time` module in `gravtools` contains a utility function to convert
from GPS time to the builtin `datetime`.

```python
>>> from gravtools import time
>>> time.gps_to_datetime(1187529241)
datetime.datetime(2017, 8, 23, 13, 14, 20)
```

## Merger Formatting
The `Merger` class in the `PyCBC` module doesn't have a clean repr by default. The `merger` module
in the `gravtools` package includes formatting utilities for `Merger` objects, mostly for quick
inspection and display purposes (for example, in a Jupyter notebook).

```python
>>> from gravtools import merger
>>> from pycbc import catalog
>>> m = catalog.Merger('GW150914')
>>> merger.summary(m)
'Merger[GW150914](Mass1=35.6, Mass2=30.6, FinalSpin=0.69)'
``` 

The parameters displayed are configurable as well, using the `parameters` argument

```python
>>> merger.summary(m, parameters=[MergerParameters.Redshift])
'Merger[GW150914](Redshift=0.09)'
```
