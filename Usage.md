# Document Your Sources #

To add a documentation string to your Python modules and functions, enclose the documentation in """triple-quotes"""

I have heard that this is the recommended way to document your code and you should be doing this anyway.

Example:

```
def get_dir(treeviewcolumn, cell_renderer, model, iter):
    """Callback to set text property to match treemodel data.
    
    The text may be different or contain extra style information
    but here we are setting it to be the same."""
    val = model.get_value(iter, 0)
    cell_renderer.set_property('text', str(val))
    return
```

# Checkout #

svn checkout https://greenhorn.googlecode.com/svn/trunk/greenhorn

# Browse Documentation #

./greenhorn.py

Displays interactive help for regular Python commands (also known as builtins).

./greenhorn.py gtk

Displays interactive help for the 'gtk' module.

# Search #

To search for an item, type part of its name in the search box and press Enter.

# Greenhorn Interactive #

To use greenhorn's gdir() command interactively:
```
$ PYTHONSTARTUP=imports python

Python 2.7 (r27:82500, Sep 16 2010, 18:02:00) 
Type "help", "copyright", "credits" or "license" for more information.
Type "gdir('module')" for help on 'module'.
>>>
>>>gdir('os')
```

There is a limitation with Python that you can not view `__builtins__`
in interactive mode. The workaround is to execute greenhorn from the shell.

```
execfile('greenhorn.py')
```

# Inspect Source Code #

This program evaluates and displays the output from the dir() command and outputs each functions .doc string when tree items are clicked on. If local modules are imported, a source tab will appear, allowing you to browse source code on that item. For example:

./greenhorn.py self

If you use Greenhorn to inspect itself and search for any of the modules Greenhorn exports, such as entry\_changed\_cb, a source code tab will appear as a child. (Click the arrow and double-click on 'source' to see the listing.)

Source code browsing also works on other modules that have source code available. The Python 'inspect' module is one of them.

./greenhorn.py inspect

This is very handy if you often use bleeding-edge modules for which the documentation changes rapidly or otherwise sucks.