python-versify : client to the Bible api platforms python friendly
==================================================================

python-versify is a pure python library wich can find many verses on the bible. The lib relies on Dbt.io for get contents.

Look how python-versify is usefull

```python
from versify.util.Dbt import Dbt

dbt = Dbt(config_path="/path/to/config.ini")

# DBY is the code of Darby
print(dbt.find_verse("DBY", "1 Timothée", 2, 1))

```
Features support
----------------

- Find any verse on the bible
- Find random verse on the bible

Installation
------------

To install python-versify, simple use pip like that:

```bash
pip install python-versify
```

You need a config file for Dbt like : 

```ini
[dbt]
key = yourDbtKey
lang = FRN
```



Documentation
-------------

Documentation is available on []()

How to Contribute
-----------------

1. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
2. Fork the repository on GitHub to start making your changes to the master branch (or branch off of it).
3. Send a pull request and bug the maintainer until it gets merged and published. :) Make sure to add yourself to AUTHORS.
 