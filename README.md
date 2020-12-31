# vizplugins
official plugins for VizTracer; currently support tracing cpu percentage.

## Install

The prefered way to install VizTracer is via pip

```
pip install vizplugins
```

## Basic Usage

The vizplugin should be used with viztracer.

Assume you have a python script:

```
python3 my_script.py arg1 arg2
```

You can  use VizTracer and the plugin by

```
viztracer --plugin vizplugins.cpu_usage -- my_script.py arg1 arg2
```

which will generate a ```result.html``` file in the directory you run this command, which you can open with Chrome.


## Example

The below image is an example of the resulting html, which is called on an recursively defined fibonacci funtion.

The "cpu_percentage" on the top indicates the corresponding cpu usage at each time period. You can see the details by clicking on one of the periods.

[![example_img](https://github.com/in-the-ocean/vizplugins/blob/readme/img/fib.png)](https://github.com/in-the-ocean/vizplugins/blob/readme/img/fib.png)