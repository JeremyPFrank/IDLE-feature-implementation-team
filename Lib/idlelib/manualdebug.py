"""
Currently: Simple Window for Manual Debug Feature - adpated from configdialog.py 
Note there is a Vertical Scrolling Window class in configdialog.py that may be useful
Some of the current imports are not used but would be used with a Vertical Scrolling Window 
so they've been left in for conviniance (will likely use a scrolling window for a list of print statements)
"""
from tkinter import (Toplevel, Canvas, TRUE, FALSE,
                     TOP, BOTTOM, RIGHT, LEFT, 
                     BOTH, Y, NW, VERTICAL, X)
from tkinter.ttk import (Frame, Notebook, Scrollbar, Button)
from idlelib import macosx
from tkinter import Text, END
from tkinter import StringVar, Entry, Label

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
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        
        if not _utest:
            self.wm_deiconify()
    
    def create_widgets(self):
        """Create and place widgets for the dialog and the large output for prints.
        """
        self.frame = frame = Frame(self, padding=5)
        self.frame.grid(sticky="nwes")

        self.output_text = Text(frame, height=15, width=60, wrap="word", state="disabled")
        self.output_text.grid(row=0, column=0, columnspan=2, sticky="nwes", padx=4, pady=4)
        self.output_text.tag_configure("debug_blue", foreground="blue")
        scrollbar = Scrollbar(frame, command=self.output_text.yview)
        scrollbar.grid(row=0, column=2, sticky="ns")
        self.output_text['yscrollcommand'] = scrollbar.set
        self.create_action_buttons().grid(row=1, column=0, columnspan=3, sticky="ew", pady=(8, 0))
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

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

        self.line_var = getattr(self, "line_var", StringVar(self))
        line_frame = Frame(outer)
        Label(line_frame, text="Comma-separated debug lines:").pack(side=LEFT)
        self.line_entry = Entry(line_frame, textvariable=self.line_var, width=20)
        self.line_entry.pack(side=LEFT)
        line_frame.pack(side=TOP, pady=4)
        buttons_frame = Frame(outer, padding=2)
        self.buttons = {}
        for txt, cmd in (
            ('Apply', self.apply),
            ('Unapply', self.cancel)):
            self.buttons[txt] = Button(buttons_frame, text=txt, command=cmd,
                       takefocus=FALSE, **padding_args)
            self.buttons[txt].pack(side=LEFT, padx=5)
        # Add space above buttons.
        Frame(outer, height=2, borderwidth=0).pack(side=TOP)
        buttons_frame.pack(side=BOTTOM)
        return outer

    def output_message(self, message):
        """Insert message into the output window."""
        self.output_text.config(state="normal")
        self.output_text.insert(END, message + "\n", "debug_blue")
        self.output_text.see(END)
        self.output_text.config(state="disabled")

    def check_line(self, lineno):
        """Check for valid line numbers in the debug window text box.
        Text must be a valid line number in the code."""
        max_lines = int(self.parent.index('end-1c').split('.')[0])
        print(max_lines)  # Debugging line, can be removed later)
        if lineno.isdigit() and int(lineno) >= 1 and int(lineno) <= max_lines:
            return True
        return False

    def apply(self):
        """Apply print statements and display output in the window."""
        line_text = self.line_var.get()
        for line in line_text.split(","):
            lineno = line.strip()
            if self.check_line(lineno):
                self.output_message("Line "+ lineno + ": applied!")
            else:
                self.output_message("Invalid line number: " + lineno)

    def cancel(self):
        """Unapply print statements from showing in the debug output."""
        line_text = self.line_var.get()
        for line in line_text.split(","):
            lineno = line.strip()
            if self.check_line(lineno):
                self.output_message("Line "+ lineno + ": unapplied!")
            else:
                self.output_message("Invalid line number: " + lineno)

    def destroy(self):
        self.grab_release()
        super().destroy()

if __name__ == '__main__':
    from unittest import main
    main('idlelib.idle_test.test_configdialog', verbosity=2, exit=False)

    from idlelib.idle_test.htest import run
    run(ManualDebug)
