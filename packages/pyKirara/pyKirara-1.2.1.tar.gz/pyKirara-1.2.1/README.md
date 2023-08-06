[![Documentation Status](https://readthedocs.org/projects/pykirara/badge/?version=latest)](https://pykirara.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/pyKirara.svg)](https://badge.fury.io/py/pyKirara)
# pyKirara

pyKirara is a Python library for the starlight.kirara REST API

[Basic Documentation](https://pykirara.readthedocs.io/en/latest/)

[Async Port](https://github.com/EthanSk13s/async-kirara)
## Usage

```python
import pyKirara

client = pyKirara.Kirara()
uzuki = client.get_idol(101)

print(f"HI! MY NAME IS {uzuki.conventional}")
print("I'll do my best!")
print(f"I'am {uzuki.age} years old!")

# Returns:
# HI! MY NAME IS Shimamura Uzuki
# I'll do my best!
# I'am 17 years old!
```

## Requirements
- Python 3.5+
- [Requests](https://github.com/kennethreitz/requests) library

## License
[MIT](https://choosealicense.com/licenses/mit/)
