#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
"""
    Greenhorn:  Interactive help GUI
    Copyright (C) 2010 Henry Kroll III, http://www.thenerdshow.com

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import sys,inspect

#~ global modules
import gtk

(Jump, Search, Help) = range(3)

def get_dir(treeviewcolumn, cell_renderer, model, iter):
    """Callback to set text property to match treemodel data.
    
    The text may be different or contain extra style information
    but here we are setting it to be the same."""
    val = model.get_value(iter, 0)
    cell_renderer.set_property('text', str(val))
    return

def filter_it(a,b):
    """return a filtering of a on list b"""
    return filter(lambda x:x in eval(a),b)
        
class gdir(gtk.Window):
    def run(self):
        """rum method to start the main loop"""
        gtk.main()
    
    def func_cb(self, model, path, iter, user_data=None):
        """Function callback that iterates over each row in tree.
        
        Here we are using it to implement a partial match search."""
        val = model.get_value(iter, 0)
        if (user_data in val) and (val not in self.found):
            #~ print 'found',val
            self.found.append(val)
            sel=self.treeview.get_selection()
            sel.select_iter(iter)
            self.treeview.scroll_to_cell(path)
            self.treeview.set_cursor(path)
            return True
        else:
            return False
    
    def entry_changed_cb(self,editable, user_data=None):
        """Called when the gtk.Entry editable changes.
        
        Clears recent searches so we can search again."""
        self.found=[]
        
    def entry_activate_cb(self,entry,user_data=None):
        """Called when search button or Enter is pressed."""
        entry=self.entry1
        text = entry.get_text()
        if user_data==Help:
            os.popen('devhelp -s '+text)
            return
        model=self.treeview.get_model()
        model.foreach(self.func_cb,text)
        
    def populate_branch(self,iter,dirarg):
        """Populate the next branch with items.
        
        Called when somebody clicks to expand the list."""
        i=iter
        e=dir(eval(dirarg))
        dummy=self.treestore.iter_children(iter)
        for key in e:
            i=self.treestore.append(iter, [key])
            self.treestore.append(i,['source'])
        if dummy:
            self.treestore.remove(dummy)
        return i
    
    def get_dot_name(self, treeview, iter, model):
        """builds a class.method name from treeveiw items"""
        dotname=model.get_value(iter,0)
        parent=iter
        while 1:
            parent=model.iter_parent(parent)
            if not parent:
                break
            dotname=model.get_value(parent,0)+'.'+dotname
        if self.dirarg=='':
            return dotname
        else:
            return self.dirarg+'.'+dotname
    
    def row_expanded_cb(self, treeview, iter, path):
        """activated when the user expands an arrow in the treeview
        either by pressing shift-right arrow or clicking on it"""
        model = treeview.get_model()
        val=model.get_value(iter,0)
        dotname=self.get_dot_name(treeview,iter,model)
        functype=str(type(eval(dotname))).split("'")[1]
        t=['function','instancemethod']
        print (dotname,functype)
        if path not in self.expanded and not functype in t:
            self.expanded.append(path)
            self.populate_branch(iter,dotname)
        
    def row_activated_cb(self, treeview, path, column):
        """activated when user clicks on an item in the treeview"""
        model = treeview.get_model()
        iter  = model.get_iter(path)
        val=model.get_value(iter,0)
        dotname=self.get_dot_name(treeview,iter,model)
        if val=='source':
            text=inspect.getsource(eval(dotname[:dotname.rindex('.')]))
        else:
            t=''
            try:
                t=str(type(eval(dotname))).split("'")[1]
            except:
                pass
            print (dotname,t)
            text=eval(dotname).__doc__
            if not text:
                text=t
        self.text.set_text( text )

        
    def __init__(self,dirarg='__builtins__'):
        """Initialization begins here"""
        #~ print (dir(eval(dirarg)))
        if len(sys.argv)>1:
            dirarg=sys.argv[-1]
        self.dirarg=dirarg
        if ('_' not in dirarg) and (dirarg != 'self'):
            exec 'import '+dirarg in globals()
        # keep track of which nodes were expanded
        # so we don't expand them again
        self.expanded=[]
        self.found=[]
        gtk.Window.__init__(self)
        self.set_title("Greenhorn "+dirarg)
        self.set_icon_from_file('greenhorn.png')
        self.treestore = gtk.TreeStore(object)
        
        self.treeview = gtk.TreeView(self.treestore)
        cell = gtk.CellRendererText()
        tvcolumn = gtk.TreeViewColumn('Object ID', cell)
        self.treeview.append_column(tvcolumn)
        self.entry1=gtk.Entry(50)
        #~ self.treeview.set_search_column(0)
        self.treeview.set_enable_search(False)
        
        scroll1 = gtk.ScrolledWindow()
        scroll1.set_property("hscrollbar-policy",gtk.POLICY_NEVER)
        scroll1.add(self.treeview)
        
        self.text=gtk.TextBuffer()
        self.textview=gtk.TextView(self.text)
        self.text.set_text('Double-click an item on the left for help.')
        
        scroll2 = gtk.ScrolledWindow()
        scroll2.set_property("hscrollbar-policy",gtk.POLICY_NEVER)
        scroll2.add(self.textview)
        
        self.button_search=gtk.Button(label=None,stock=gtk.STOCK_JUMP_TO)
        self.button_help=gtk.Button(label=None,stock=gtk.STOCK_HELP)
        
        vbox1=gtk.VBox()
        hbox1=gtk.HBox()
        hbox2=gtk.HBox()
        
        hbox1.pack_start(vbox1)
        hbox1.pack_start(scroll2)
        vbox1.pack_start(hbox2,False)
        hbox2.pack_start(self.entry1,False)
        hbox2.pack_start(self.button_search,False,False)
        hbox2.pack_start(self.button_help,False,False)
        vbox1.pack_start(scroll1)        
        self.add(hbox1)
              
        #~ set callback funcs
        tvcolumn.set_cell_data_func(cell, get_dir, data=None)
        self.treeview.connect('row-activated', self.row_activated_cb)
        self.treeview.connect('row-expanded', self.row_expanded_cb)
        self.entry1.connect('activate',self.entry_activate_cb,Jump)
        self.button_search.connect('clicked',self.entry_activate_cb,Search)
        self.button_help.connect('clicked',self.entry_activate_cb,Help)
        self.entry1.connect('changed',self.entry_changed_cb)
        self.connect('destroy', lambda w: gtk.main_quit())

        self.populate_branch(None,dirarg)
        self.window1=self
        self.set_property("default-height",600)
        self.show_all()

if __name__ == "__main__":
    gdir().run()
else:
    print("""Type greenhorn.gdir('module') for help on 'module'.
    or use 'from greenhorn import gdir'""")
