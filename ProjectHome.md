## Browse module documentation and source code ##

It was fun to develop this, but I discovered that my pydoc wasn't working because of a bug https://bugzilla.redhat.com/show_bug.cgi?id=443246

Once I got pydoc working I no longer needed this tool. It could be a useful demo for somebody wanting to use the treeview widget, however.

![http://thenerdshow.com/images/greenhorn_ss.png](http://thenerdshow.com/images/greenhorn_ss.png)

Aiming to be a graphical interface for Python's help() and dir() commands, Greenhorn queries internal documentation and source code (which is usually more up-to-date than traditional documentation).

Displays a tree diagram of classes, modules and functions in a window. Clicking on individual modules displays `.__doc__` strings and sub-modules or functions. Source code can also be browsed, if available, using Python inspect. Development version supports syntax highlighting.

Brought to you by [The Nerd Show](http://thenerdshow.com)