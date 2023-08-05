## consolejs

` A console logger / debugger for Python CLI programs`


Currently consolejs only support functions. support for classes will be added later.


### Installation
```shell
$ pip install consolejs

```

### Getting Started

```python

# Create a Conlog from the constructor.
consolejs = Conlog.create("main")

# Set the required logging level
consolejs.level = Conlog.DEBUG

# To use on the `main` module
console = consolejs.get_console()

####  in module2.py

@Conlog.fn
def say_hi(name):
	console = Conlog.get_console("main")
	console.debug("args {name=}")
	print(f"Hi {name}"

```


### How it works.
`console.debug` supports `expr debug` expressions introduced in Python 3.8.
It dynamically rewrites the function in Python 3.8 and uses a beautiful way to support it in < 3.7

See tests/ for samples.

### License
-------

Copyright (c) 2019 Cswl Coldwind 

consolejs is distributed under the terms 

- `MIT License <https://choosealicense.com/licenses/mit>`_ 
 
