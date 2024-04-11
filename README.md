# pyck

This package contains helpers and utilities to promote code reusability across multiple Python applications.

## Usage

1.  Add `pyck@git+https://github.com/tchangkiat/pyck` in `pyproject.toml` or `requirements.txt`.

2.  Install the dependencies using `pip install -e .` (if you are using pyproject.toml) or `pip install -r requirements.txt` respectively. Alternaticely, run `pip install --upgrade --force-reinstall pyck@git+https://github.com/tchangkiat/pyck` to re-install this package in the application's virtual environment.

3.  Import the modules and invoke the methods. For example,

    ```python
    from pyck.helpers.logging import Logging
    log = Logging.get_instance()
    log.info("Hello World!")
    ```
