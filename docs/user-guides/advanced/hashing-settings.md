# Hashing settings

## Overview

Nemo Guardrails uses hashing mainly for caching purposes. By default, the `md5` hashing algorithm is used. Caching of search queries is disabled by default, but this does not disable it entirely.

## FIPS considerations

In some regulated environments, the `md5` hashing algorithm may not be available (e.g., FIPS-compliant Python). In such cases, `sha256` hashing will be used instead. This default applies across the library unless explicitly overridden.

## Setting hashing algorithm

To explicitly set the hashing algorithm, call the following function before running the Nemo Guardrails library code:

```python
from nemoguardrails.hashing import set_default_hash_algorithm
set_default_hash_algorithm('sha256')
```

## Additional considerations

When caching is enabled and `key_generator` is set in the configuration, it overrides the library default for caching embedding searches.

Example:

```yaml
knowledge_base:
  embedding_search_provider:
    name: default
    parameters:
      embedding_engine: FastEmbed
      embedding_model: all-MiniLM-L6-v2
      use_batching: False
      max_batch_size: 10
      max_batch_hold: 0.01
      search_threshold: None
    cache:
      enabled: True
      key_generator: sha256   # <- Overrides the library default.
      store: filesystem
      store_config: {}
```
