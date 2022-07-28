# The Python Interface to LINGO.

This package requires Lingo and a valid license key. Please refer to the [Lingo user manual](https://lindo.com/downloads/PDF/LINGO.pdf) for installation instructions, and to learn more about the Lingo modeling language.

## Installation For LINGO 20

This python package can be installed with pip. It is assumed Lingo 20 is installed on host system.

For administrative users: 

```bash
> pip install lingo_api
```

For standard (non-administrative) users:

```bash
> pip install lingo_api --user
```

## Installation For LINGO 19

This python package can be installed with pip. It is assumed Lingo 19 is installed on host system.

For administrative users: 

```bash
> pip install lingo_api==19.0.6
```

For standard (non-administrative) users:

```bash
> pip install lingo_api==19.0.6 --user
```



## Testing

A quick way to test the installation is to run
```bash
> python -m lingo_test
```

It is also good to test the LINGO API on one of the included examples.
```
> cd examples/CHESS
> python chess.py
```

## Possible errors due to misconfiguration

If the user does not have the correct LINGO environment variable set, they will not be able to load
the lingo_api library instead they will receive an error message. 

To fix the problem follow these steps

### Using Windows
On the command line depending on the users LINGO installation:

LINGO 20 on windows 64-bit  
```dos
> setx LINGO64_20_HOME "C:\path\to\LINGO64_20" 
```
LINGO 20 on windows 32-bit 
```dos
> setx LINGO_20_HOME "C:\path\to\LINGO20" 
```


LINGO 19 on windows 64-bit 
```dos
> setx LINGO64_19_HOME "C:\path\to\LINGO64_19"
```
LINGO 19 on windows 32-bit  
```dos
> setx LINGO_19_HOME "C:\path\to\LINGO19"
```

### Using Linux
On the command line depending on the users LINGO installation:

LINGO 20
For administrative users:
```    
$ export LINGO64_20_HOME="/opt/lingo20"	
```    
For standard (non-administrative) users:
```    
$ export LINGO64_20_HOME="~/lingo20"	
```   

LINGO 19
```    
$ export LINGO64_19_HOME="/opt/lingo19"	
```    
For standard (non-administrative) users:
```    
$ export LINGO64_19_HOME="~/lingo19"	
```   


To have this variable set automatically, add the above line to the `~/.bashrc` or `~/.bash_profile` file.


## How to Build Wheel and Install (for package managers)

To build the python package on any operating system first start by creating a whl file. From the top of the lingoapi-python directory run the command.

```bash
> python -m build
```

If the command is successful a new directory named `dist` is created in the lingoapi-python directory. The new directory will have two files with extension `.whl` and `.tar.gz`. For example, if the LINGO API is built it on Windows using Python 3.10 the new directory will look like this.

```bash
├── dist
│  ├── lingo_api-x.y.z-cp310-cp310-win_amd64.whl
│  └── lingo-x.y.z.tar.gz
```

The package can now be installed locally using the command.
```bash
> pip install dist/*.whl
```