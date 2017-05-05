# python-oneliner

Module for practical Python one-liners.

## Installation

    pip install -e git+https://github.com/seguri/python-oneliner#egg=oneliner

This will install the module, callable with `python -m oneliner`, and an executable provided by pip in the form of `pyl-<sys.version_info.major>.<sys.version_info.minor>`, eg. `pyl-3.4`

## Usage

This module allows for imports and aliases. Here we import `os.path.abspath` as `a`:

    $ cd /tmp
    $ python -m oneliner -m 'os.path.[abspath=a],datetime.[datetime=dt]' -e "a('.'); dt.now()"
    /private/tmp
    2017-05-05 17:26:56.033563

Equivalent to:

    $ cd /tmp
    $ python -c 'from os.path import abspath as a; print(a("."))'
    /private/tmp

The difference here is that we didn't need to print the expression because we evaluated it with `-e`. Writing it as a statement requires the `-s` switch:

    $ cd /tmp
    $ python -m oneliner -m 'os.path.[abspath=a]' -s 'print(a("."))'
    /private/tmp

`os`, `re` and `sys` are always available. In my case, on Python 3.4.5:

    $ pyl-3.4 -e 'sys.version_info'
    sys.version_info(major=3, minor=4, micro=5, releaselevel='final', serial=0)
    $ pyl-3.4 -e os.pathsep
    :

## Uninstall

    pip uninstall oneliner

## External links

This work is a partial rewrite of [gvalkov/python-oneliner][1] that didn't perform as I expected. I t was also an opportunity to better learn Python's `import` system.


[1]: https://github.com/gvalkov/python-oneliner
