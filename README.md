## LiMe-Appy

This is a Python library and minimalistic command line utility to test and access the LibreMesh api which was initially developed for the [LiMe App](https://github.com/libremesh/lime-app).

### Testing

To use this tool and run it's tests you need access to a router with LibreMesh installed. The tool will try to access thisnode.info by default and run it's tests and commands against the api exposed by the node in that address.

To run the tests just execute:

```
python3 tests.py
```

### Accessing the api

To access a specific method execute:

```
python3 lime.py [method_name]
```

For example:

```
python3 lime.py get_hostname
```

will return the node hostname.


The code in lime.py should be self explanatory.
