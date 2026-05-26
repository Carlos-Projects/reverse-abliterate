Development
===========

Setup
-----

.. code-block:: bash

   git clone https://github.com/Carlos-Projects/reverse-abliterate.git
   cd reverse-abliterate
   pip install -e .
   pip install pytest ruff mypy pre-commit
   pre-commit install

Running Tests
-------------

.. code-block:: bash

   python -m pytest tests/ -v

Code Style
----------

.. code-block:: bash

   ruff check .
   ruff format .
   mypy src/

Project Structure
-----------------

.. code-block:: text

   reverse-abliterate/
   ├── src/reverse_abliterate/
   │   ├── cli.py        # CLI commands
   │   ├── constants.py  # Detection constants
   │   ├── detect.py     # Scanning logic
   │   └── harden.py     # Hardening features
   ├── tests/
   ├── docs/
   └── pyproject.toml
