# !!! WARNING !!! - Chaos ensues

# olc Code Jam 2019 - Theme: Destruction

I mainly use this code jam to get my gears going again, after a while of 
not writing any code. I neither have a lot of spare time during this jam,
nor do I have a clear goal or expectation for the final entry.

I wanted to get more familiar with ``vim`` and ``git``, having started to
use the former only recently and being more used to writing code in IDEs,
 I also feel I don't really know how to use the latter properly. So the
result of this week of coding will be secondary to improving my skills
over all.

# Fight of Life
Inspired by Conways' Game of Life, I wanted to experiment and see what can 
come out of it.

Since I was mostly learning how to write code with ``vim`` as efficiently 
as possible and most of time only had a rough idea of what to do, the 
result isn't shiny or good...

## Install / Run

### Prerequisites
You need [Python](https://www.python.org) 3.6+ and have an environment to 
compile Python packages (-> you need a suitable compiler toolchain and the
Python header files for your Python version and respective OS). Having ``git``
installed also helps and ``pip`` if you haven't already installed it together 
with your Python distribution...

Runtime Binaries of [SDL 2.0](https://www.libsdl.org/download-2.0.php) for 
your OS/Distribution, placed somewhere in your ``PATH``.

*Depending on your preferences, you also may want to setup a fresh ``virtualenv`` to not mess with your global
Python installation*

### Installation with git available

run: ``pip install git+https://github.com/tcdude/destruction.git``

### Installation w/o git
Download the repo and remember where you saved it *(extract/unpack it, if you downloaded as a ZIP...)*
run: ``pip install <path/where/you/saved/it>``

### Run
run: ``python -m destruction.main``


