# Makes a string file path compatible (Windows)


```python
# Tested with:
# Python 3.9.13
# Windows 10


$pip install windows-filepath



import sys
import pandas as pd
import inspect 
from windows_filepath import make_filepath_windows_comp, allow_long_path_windows
# creating some random data 
teststuff = [x + '.png' if ini % 2 == 0 else x for ini, x in enumerate(inspect.getsource(pd).splitlines())]
for _ in teststuff:
    # doesn't check the length, you can change the windows settings by calling allow_long_path_windows()
    # This will set the MAX_PATH to 32,767
    fp = make_filepath_windows_comp(
    filepath=_,
    fillvalue="_", # replacement of any illegal char
    reduce_fillvalue=True, # */<> (illegal chars) -> ____ (replacement) -> _ (reduced replacement)
    remove_backslash_and_col=False, # important for multiple folders
    spaceforbidden=True, # '\s' -> _ 
    other_to_replace=(";", ",", "[", "]", "`", "="), # other chars you don't want in the file path
    slash_to_backslash=True, # replaces / with \\ before doing all the other replacements 
)
    print(_)
    print(fp, end='\n\n')


	
```




