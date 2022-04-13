# The Python Interface to LINGO.

This package requires Lingo and a valid license key. Please refer to [Lingo user manual](https://lindo.com/downloads/PDF/LINGO.pdf) for installation instructions, and to learn more about the Lingo modeling language.

## Installation

This python package can be installed with pip. It is assumed 64-bit Lingo 19 is installed on host system.

For administrative users: 

```bash
> pip install lingo_api==19.0
```

For standard (non-administrative) users:

```bash
> pip install lingo_api==19.0 --user
```

## Testing

A quick way to test the installation is to run
```bash
> python -m lingo_test
```

You can also try out the samples by 
```
> cd examples/CHESS
> python chess.py
```

## Possible errors due to misconfiguration

You may get the following error if your LINGO64_19_HOME environment variable is not set up.  

```
Error: Environment variable LINGO64_19_HOME should be set
```

To fix the problem follow these steps

### Using Windows
On the command line for windows 64
```dos
> setx LINGO64_19_HOME "C:\LINGO64_19" 
```
### Using Linux
On the command line

For administrative users:
```     
$ export LINGO64_19_HOME="/opt/lingo19"	
```    
For standard (non-administrative) users:
```    
$ export LINGO64_19_HOME="~/opt/lingo19"	
```   
To have this variable set automatically, add the above line to your `~/.bashrc` or `~/.bash_profile` file.


## How to Build Wheel and Install (for package managers)

To build the python package on any operating system first start by creating a whl file. From the top of the lingoapi-python directory run the command.

```bash
> python -m build
```

If the command is successful a new directory named `dist` is created in the lingoapi-python directory. The new directory will have two files with extension `.whl` and `.tar.gz`. For example, if you built it on Windows using Python 3.10 the new directory will look like this.

```bash
├── dist
│  ├── lingo_api-x.y.z-cp310-cp310-win_amd64.whl
│  └── lingo-x.y.z.tar.gz
```

The package can now be installed locally using the command.
```bash
> pip install dist/*.whl
```
