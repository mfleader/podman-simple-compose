# podman-simple-compose

You **must** add this directory to the `PYTHONPATH`, so that the [path based import finder](https://docs.python.org/3/reference/import.html#the-path-based-finder) will search this directory for a module named `app`. This allows `alembic/env.py` (and alebmic) to use modules from `app`.

```shell
cd podman-simple-compose
export PYTHONPATH="$(pwd):$PYTHONPATH"
```