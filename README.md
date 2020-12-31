# vizplugins

[![build](https://github.com/gaogaotiantian/vizplugins/workflows/build/badge.svg)](https://github.com/gaogaotiantian/vizplugins/actions?query=workflow%3Abuild)  [![flake8](https://github.com/gaogaotiantian/vizplugins/workflows/lint/badge.svg)](https://github.com/gaogaotiantian/vizplugins/actions?query=workflow%3ALint)  [![readthedocs](https://img.shields.io/readthedocs/vizplugins)](https://vizplugins.readthedocs.io/en/stable/)  [![coverage](https://img.shields.io/codecov/c/github/gaogaotiantian/vizplugins)](https://codecov.io/gh/gaogaotiantian/vizplugins)  [![pypi](https://img.shields.io/pypi/v/vizplugins.svg)](https://pypi.org/project/vizplugins/)  [![support-version](https://img.shields.io/pypi/pyversions/vizplugins)](https://img.shields.io/pypi/pyversions/vizplugins)  [![license](https://img.shields.io/github/license/gaogaotiantian/vizplugins)](https://github.com/gaogaotiantian/vizplugins/blob/master/LICENSE)  [![commit](https://img.shields.io/github/last-commit/gaogaotiantian/vizplugins)](https://github.com/gaogaotiantian/vizplugins/commits/master)

official plugins for VizTracer; currently support tracing cpu usage through psutil.

## Install

The prefered way to install vizplugins is via pip

```
pip install vizplugins
```

## Basic Usage

The vizplugin should be used with viztracer.

You can  use VizTracer and the plugin by

```
viztracer --plugin vizplugins.cpu_usage -- my_script.py arg1 arg2
```

which will generate a ```result.html``` file in the directory you run this command, which you can open with Chrome.


## Example

The below image is an example of the resulting html, which is called on an recursively defined fibonacci funtion.

The "cpu_percentage" on the top indicates the corresponding cpu usage at each time period. You can see the details by clicking on one of the periods.

[![example_img](https://github.com/in-the-ocean/vizplugins/blob/readme/img/fib.png)](https://github.com/in-the-ocean/vizplugins/blob/readme/img/fib.png)