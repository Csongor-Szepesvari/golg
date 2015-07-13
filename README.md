# golg
Game of Life Game

## How to run
Simply run the `main.py` file contained in the `src` folder. So
```bash
$ python3 src/main.py
```
from the root directory, for example. If the file is set to be executable, one can also simply
```bash
$ ./main.py
```
from the appropriate directory.

## How to test
From the root folder of the project run the desired file as a module. For example, if my project is in a directory called `golg`, and I want to run `board.py` in the test directory (subpackage), I would call, in directory `golg`

```bash
$ python -m test.board 
```

## Notes to self

###### Executing files inside packages
There is some note online about executing python files in packages, and some steps that need to be taken. I found this when setting up intra-package imports. At the moment I have not ran into this issue, but for reference:
http://stackoverflow.com/a/11537218/4172585


