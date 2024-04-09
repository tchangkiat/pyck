# pyck

Helpers and utilities used for various Python applications.

## Usage

1.  Add `pyck@git+https://github.com/tchangkiat/pyck` in `pyproject.toml` or `requirements.txt`.

2.  Install the dependencies using `pip install .` (if you are using pyproject.toml) or `pip install -r requirements.txt` respectively.

3.  Import the modules and invoke the methods. For example,

    ```python
    from pyck.helpers.logging import Logging
    log = Logging.get_instance()
    log.info("Hello World!")
    ```
