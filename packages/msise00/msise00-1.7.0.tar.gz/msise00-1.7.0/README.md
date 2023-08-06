[![Zenodo DOI](https://zenodo.org/badge/32971905.svg)](https://zenodo.org/badge/latestdoi/32971905)

[![Actions Status](https://github.com/space-physics/msise00/workflows/ci/badge.svg)](https://github.com/space-physics/msise00/actions)

[![Python versions (PyPI)](https://img.shields.io/pypi/pyversions/msise00.svg)](https://pypi.python.org/pypi/msise00)
[![PyPi Download stats](http://pepy.tech/badge/msise00)](http://pepy.tech/project/msise00)

# MSISE-00 in Python and Matlab

NRL MSISE-00 atmospheric model for Python &ge; 3.6, also accessible via Matlab or GNU Octave.
Valid from altitude z = 0..1000 km.

The plot immediately below shows a slice at 200km on a world-wide grid.
The yellow ball represents the sun footprint on Earth.

![MSIS global time animation](./tests/msise00_demo.gif)

This plot is from [Matlab](./tests/test_msise00_matlab.m) calling MSISE00:

![MSISE00 Matlab](./tests/msis_matlab.png)

## Install

This process is used for the Python and [Matlab](#matlab) access to MSIS.
Any Fortran compiler should work.
Fortran compiler may be installed by

* MacOS / Homebrew: `brew install gcc ninja`
* Linux: `apt install gfortran ninja-build`
* [Windows](https://www.scivision.dev/windows-gcc-gfortran-cmake-make-install/) and extract [ninja](https://github.com/ninja-build/ninja/releases) to your PATH.

Get MSISE00 and install Python package:

```sh
pip install msise00
```


or for the latest development code

```sh
git clone https://github.com/space-physics/msise00

python -m pip install -e msise00
```

### Build on Run

The Fortran code will *automatically compile* on first `import msise00`.
This does not use setuptools and so is OS / Python distribution method agnostic.


## Examples

MSISE00 can be used from the command line, as an imported module, and even from Matlab.

### import module

```python
import msise00
from datetime import datetime

atmos = msise00.run(time=datetime(2013, 3, 31, 12), altkm=150., glat=65., glon=-148.)
```

atmos is an [xarray.Dataset](http://xarray.pydata.org/en/stable/generated/xarray.Dataset.html) containing all the simulation output values.
`atmos` is 4-D: (time, altitude, lat, lon), and indexed like `atmos['N2']`


### Command Line

Write NetCDF4 output (HDF5 compatible) with command line argument `-w filename.nc`.

Simple examples include:

* AltitudeProfile.py
* TimeProfile.py
* Worldgrid.py


* Altitude Profile at a single time:

  ```sh
  python MSISE00.py -t 2017-08-21T20:48 -c 40 -90
  ```
* Alt. profile time-range with hourly time step:

  ```sh
  python MSISE00.py -t 2017-08-21 2017-08-22 -c 40 -90
  ```
* Grid: time,lat,lon: generates the plots in the README:

  ```sh
  python MSISE00.py -t 2016-09-20 2016-09-21
  ```
* single time lat/lon can be plotted:

  ```sh
  python MSISE00.py -t 2017-01-02T12
  ```

### Matlab

Matlab and GNU Octave users use of MSISE00 is demonstrated in
[AltitudeProfile.m](./matlab/AlitudeProfile.m) and
[msise00.m](./matlab/msise00.m).

MSISE00 will **automatically compile** "build on run" on first run from Matlab or Octave.

Optionally, verify Matlab is working by from the top `msise00/` directory in Terminal

```sh
matlab -batch runtests('tests')
```

## Fortran source

The MSISE00 Fortran source code may also be used directly.
We have provided for easy code reuse in
[CMake](./CMakeLists.txt)
and
[Meson](./meson.build)
projects.

## Reference

* Original fortran [code](https://ccmc.gsfc.nasa.gov/pub/modelweb/atmospheric/msis/)
* 1200+ citations 2002 [paper](http://onlinelibrary.wiley.com/doi/10.1029/2002JA009430/pdf)
