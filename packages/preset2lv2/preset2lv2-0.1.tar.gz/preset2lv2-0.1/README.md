Convert a set of native presets and generate a LV2 bundle containing one or more banks.
It supports several native formats and it's easily extensible.

```
usage: preset2lv2.py [-h] [-b BANK] format path

Convert native presets to LV2.

positional arguments:
  format                Source preset format: synthv1, padthv1, dx7syx
  path                  Source preset dir or filepath

optional arguments:
  -h, --help            show this help message and exit
  -b BANK, --bank BANK  LV2 bank name
```
