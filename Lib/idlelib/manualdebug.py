"""
Currently: Simple Window for Manual Debug Feature - adpated from configdialog.py 
Note there is a Vertical Scrolling Window class in configdialog.py that may be useful
Some of the current imports are not used but would be used with a Vertical Scrolling Window 
so they've been left in for conviniance (will likely use a scrolling window for a list of print statements)
"""
from tkinter import (Toplevel, FALSE, TOP, BOTTOM, LEFT)
from tkinter.ttk import (Frame, Scrollbar, Button)
from idlelib import macosx
from tkinter import Text, END
from tkinter import StringVar, Entry, Label
from idlelib.query import Query

open_manual_debug_windows = set()

class ManualDebug(Toplevel):
    """Opens Manual Print Statement Debug Window to set print statments
        
    *Code Adapted from configdialog.py*
    """

    def __init__(self, parent, title=''):
        """Show the tabbed dialog for user configuration.

        Args:
            parent - parent of this dialog
            title - string which is the title of this popup dialog
        """
        self.parent = parent
        tk_parent = parent.text if hasattr(parent, 'text') else parent
        Toplevel.__init__(self, tk_parent)
        self.parent = parent
        self.title(title or 'Print Statement Debugger')
        x = tk_parent.winfo_rootx() + 20
        y = tk_parent.winfo_rooty() + (150)
        self.geometry(f'+{x}+{y}')
        self.create_widgets()
        self.resizable(height=FALSE, width=FALSE)
        self.protocol("WM_DELETE_WINDOW", self.destroy)
        self.print_statements = {}
        open_manual_debug_windows.add(self)
    
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
            ('Unapply', self.cancel),
            ('See Current Lines', self.show_current)):
            self.buttons[txt] = Button(buttons_frame, text=txt, command=cmd,
                       takefocus=FALSE, **padding_args)
            self.buttons[txt].pack(side=LEFT, padx=5)
        Frame(outer, height=2, borderwidth=0).pack(side=TOP)
        buttons_frame.pack(side=BOTTOM)
        return outer

    def output_message(self, message):
        """Outputs applied/unapplied/current lines message into the output window."""
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, END)
        if message:
            self.output_text.insert(END, message + "\n", "debug_blue")
            self.output_text.see(END)
            self.output_text.config(state="disabled")
            return
        self.output_text.insert(END, "Current Print Statements at Lines:" + "\n", "debug_blue")
        for line in self.print_statements:
            if self.print_statements[line]:
                self.output_text.insert(END, str(line) + ": \"" + self.print_statements[line] + "\"\n", "debug_blue")
        self.output_text.see(END)
        self.output_text.config(state="disabled")

    def print_debug_message(self, msg):
        """Prints a debug message to the debug window"""
        self.output_text.config(state="normal")
        self.output_text.insert(END, msg + "\n", "debug_blue")
        self.output_text.see(END)
        self.output_text.config(state="disabled")

    def check_line(self, lineno):
        """Check for valid line numbers in the debug window text box.
        Text must be a valid line number in the code."""
        max_lines = int(self.parent.text.index('end-1c').split('.')[0])
        if lineno.isdigit() and int(lineno) >= 1 and int(lineno) <= max_lines:
            return True
        return False

    def show_current(self):
        """Call Output_message with 'None' argument which displays full list of print statements"""
        self.output_message(None)

    def apply(self):
        """Apply print statements and display output in the window."""
        line_text = self.line_var.get()
        print_contents = Query(self.frame, "Printed Message", "What would you like to print on line(s) " + line_text + "?").result
        for line in line_text.split(","):
            lineno = line.strip()
            if lineno in self.print_statements and self.print_statements[lineno] != None:
                self.output_message("Statement on line: " + lineno + " already exists")
            elif not self.check_line(lineno):
                self.output_message("Invalid line number: " + lineno)
            else:
                self.print_statements[lineno] = print_contents
                self.output_message(None)

    def cancel(self):
        """Unapply print statements from showing in the debug output."""
        line_text = self.line_var.get()
        for line in line_text.split(","):
            lineno = line.strip()
            if lineno not in self.print_statements:
                self.output_message("No print statment at " + lineno + " to remove")      
            else:
                del self.print_statements[lineno]
                self.output_message(None)

    def destroy(self):
        open_manual_debug_windows.discard(self)
        self.grab_release()
        super().destroy()

if __name__ == '__main__':
    from unittest import main
    main('idlelib.idle_test.test_configdialog', verbosity=2, exit=False)

    from idlelib.idle_test.htest import run
    run(ManualDebug)