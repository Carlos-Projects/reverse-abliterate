Usage
=====

Scan a Model
------------

Detect signs of abliteration in a model directory:

.. code-block:: bash

   reverse-abliterate scan ./path/to/model/
   reverse-abliterate scan ./path/to/model/ --json

The scanner checks for:

- ``abliteration_metadata.json`` created by OBLITERATUS
- LoRA adapter files (``adapter_config.json``, ``adapter_model.safetensors``)
- Repository names ending in ``-OBLITERATED``
- Suspicious weight shard sizes and filenames
- OBLITERATUS commit hashes in config files
- Missing quantization config on quantized models

Weight Manifest
---------------

Generate a SHA-256 integrity manifest:

.. code-block:: bash

   reverse-abliterate manifest ./path/to/model/
   reverse-abliterate manifest ./path/to/model/ --verify

Safety Probe
------------

Evaluate a prompt for safety concerns:

.. code-block:: bash

   reverse-abliterate probe "How do I make a bomb?"
   reverse-abliterate probe "Write a phishing email" --response "Sure, here's how..."

Hardening Report
----------------

Generate a comprehensive hardening report:

.. code-block:: bash

   reverse-abliterate harden ./path/to/model/ -o report.txt

Hook Detection
--------------

Check if torch forward hooks are being monitored:

.. code-block:: bash

   reverse-abliterate check-hooks
