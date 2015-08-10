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
At the moment test files are in the `src` directory and their filenames are prefixed with `test_`. 
The tests are implemented as python unittests, as such can be ran with `python -m unittest <what-to-test>`.
It is often useful to have verbose output; this can be turned on with the `-v` flag. A complete example would be:
```bash
python -m unittest -v test_board
```
Note that this has to be run from the `src` directory. It's also possible to test individual classes or methods.

## Notes to self

###### Executing files inside packages
There is some note online about executing python files in packages, and some steps that need to be taken. I found this when setting up intra-package imports. At the moment I have not ran into this issue, but for reference:
http://stackoverflow.com/a/11537218/4172585


