"""
Currently: Simple Window for Manual Debug Feature - adpated from configdialog.py 
Note there is a Vertical Scrolling Window class in configdialog.py that may be useful
Some of the current imports are not used but would be used with a Vertical Scrolling Window 
so they've been left in for conviniance (will likely use a scrolling window for a list of print statements)
"""
from tkinter import (Toplevel, Canvas, TRUE, FALSE,
                     TOP, BOTTOM, RIGHT, LEFT, 
                     BOTH, Y, NW, VERTICAL)
from tkinter.ttk import (Frame, Notebook, Scrollbar, Button)
from idlelib import macosx

class ManualDebug(Toplevel):
    """Opens Manual Print Statement Debug Window to set print statments
        
    *Code Adapted from configdialog.py*
    """

    def __init__(self, parent, title='', *, _htest=False, _utest=False):
        """Show the tabbed dialog for user configuration.

        Args:
            parent - parent of this dialog
            title - string which is the title of this popup dialog
            _htest - bool, change box location when running htest
            _utest - bool, don't wait_window when running unittest
        """
        self._utest = _utest
        self.parent = parent
        Toplevel.__init__(self, parent)
        self.parent = parent
        if _htest:
            parent.instance_dict = {}
        if not _utest:
            self.withdraw()

        self.title(title or 'Print Statement Debugger')
        x = parent.winfo_rootx() + 20
        y = parent.winfo_rooty() + (30 if not _htest else 150)
        self.geometry(f'+{x}+{y}')
        self.create_widgets()
        self.resizable(height=FALSE, width=FALSE)
        self.transient(self.parent)
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        
        if not _utest:
            self.grab_set()
            self.wm_deiconify()
            self.wait_window()
    
    def create_widgets(self):
        """Create and place widgets for tabbed dialog.
        """
        self.frame = frame = Frame(self, padding=5)
        self.frame.grid(sticky="nwes")
        self.note = note = Notebook(frame)

        note.enable_traversal()
        note.pack(side=TOP, expand=TRUE, fill=BOTH)
        self.create_action_buttons().pack(side=BOTTOM)

    def create_action_buttons(self):
        """Return frame of action buttons for dialog.
        """
        if macosx.isAquaTk():
            # Changing the default padding on OSX results in unreadable
            # text in the buttons.
            padding_args = {}
        else:
            padding_args = {'padding': (6, 3)}
        outer = Frame(self.frame, padding=2)
        buttons_frame = Frame(outer, padding=2)
        self.buttons = {}
        for txt, cmd in (
            ('Apply', self.apply),
            ('Cancel', self.cancel)):
            self.buttons[txt] = Button(buttons_frame, text=txt, command=cmd,
                       takefocus=FALSE, **padding_args)
            self.buttons[txt].pack(side=LEFT, padx=5)
        # Add space above buttons.
        Frame(outer, height=2, borderwidth=0).pack(side=TOP)
        buttons_frame.pack(side=BOTTOM)
        return outer

    def apply(self):
        """Apply print statements and close dialog."""
        #add code to apply invisible print statements
        self.destroy()

    def cancel(self):
        """Dismiss config dialog.

        Methods:
            destroy: inherited
        """
        self.destroy()

    def destroy(self):
        self.grab_release()
        super().destroy()

if __name__ == '__main__':
    from unittest import main
    main('idlelib.idle_test.test_configdialog', verbosity=2, exit=False)

    from idlelib.idle_test.htest import run
    run(ManualDebug)
