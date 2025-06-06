"Test pyshell, coverage 12%."
# Plus coverage of test_warning.  Was 20% with test_openshell.

from idlelib import pyshell
from idlelib.pyshell import PyShell 
import unittest
from test.support import requires
from tkinter import Tk
from unittest import mock
import idlelib.pyshell as pyshell_mod


class FunctionTest(unittest.TestCase):
    # Test stand-alone module level non-gui functions.

    def test_restart_line_wide(self):
        eq = self.assertEqual
        for file, mul, extra in (('', 22, ''), ('finame', 21, '=')):
            width = 60
            bar = mul * '='
            with self.subTest(file=file, bar=bar):
                file = file or 'Shell'
                line = pyshell.restart_line(width, file)
                eq(len(line), width)
                eq(line, f"{bar+extra} RESTART: {file} {bar}")

    def test_restart_line_narrow(self):
        expect, taglen = "= RESTART: Shell", 16
        for width in (taglen-1, taglen, taglen+1):
            with self.subTest(width=width):
                self.assertEqual(pyshell.restart_line(width, ''), expect)
        self.assertEqual(pyshell.restart_line(taglen+2, ''), expect+' =')


class PyShellFileListTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        requires('gui')
        cls.root = Tk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        #cls.root.update_idletasks()
##        for id in cls.root.tk.call('after', 'info'):
##            cls.root.after_cancel(id)  # Need for EditorWindow.
        cls.root.destroy()
        del cls.root

    def test_init(self):
        psfl = pyshell.PyShellFileList(self.root)
        self.assertEqual(psfl.EditorWindow, pyshell.PyShellEditorWindow)
        self.assertIsNone(psfl.pyshell)

# The following sometimes causes 'invalid command name "109734456recolorize"'.
# Uncommenting after_cancel above prevents this, but results in
# TclError: bad window path name ".!listedtoplevel.!frame.text"
# which is normally prevented by after_cancel.
##    def test_openshell(self):
##        pyshell.use_subprocess = False
##        ps = pyshell.PyShellFileList(self.root).open_shell()
##        self.assertIsInstance(ps, pyshell.PyShell)


class PyShellRemoveLastNewlineAndSurroundingWhitespaceTest(unittest.TestCase):
    regexp = pyshell.PyShell._last_newline_re

    def all_removed(self, text):
        self.assertEqual('', self.regexp.sub('', text))

    def none_removed(self, text):
        self.assertEqual(text, self.regexp.sub('', text))

    def check_result(self, text, expected):
        self.assertEqual(expected, self.regexp.sub('', text))

    def test_empty(self):
        self.all_removed('')

    def test_newline(self):
        self.all_removed('\n')

    def test_whitespace_no_newline(self):
        self.all_removed(' ')
        self.all_removed('  ')
        self.all_removed('   ')
        self.all_removed(' ' * 20)
        self.all_removed('\t')
        self.all_removed('\t\t')
        self.all_removed('\t\t\t')
        self.all_removed('\t' * 20)
        self.all_removed('\t ')
        self.all_removed(' \t')
        self.all_removed(' \t \t ')
        self.all_removed('\t \t \t')

    def test_newline_with_whitespace(self):
        self.all_removed(' \n')
        self.all_removed('\t\n')
        self.all_removed(' \t\n')
        self.all_removed('\t \n')
        self.all_removed('\n ')
        self.all_removed('\n\t')
        self.all_removed('\n \t')
        self.all_removed('\n\t ')
        self.all_removed(' \n ')
        self.all_removed('\t\n ')
        self.all_removed(' \n\t')
        self.all_removed('\t\n\t')
        self.all_removed('\t \t \t\n')
        self.all_removed(' \t \t \n')
        self.all_removed('\n\t \t \t')
        self.all_removed('\n \t \t ')

    def test_multiple_newlines(self):
        self.check_result('\n\n', '\n')
        self.check_result('\n' * 5, '\n' * 4)
        self.check_result('\n' * 5 + '\t', '\n' * 4)
        self.check_result('\n' * 20, '\n' * 19)
        self.check_result('\n' * 20 + ' ', '\n' * 19)
        self.check_result(' \n \n ', ' \n')
        self.check_result(' \n\n ', ' \n')
        self.check_result(' \n\n', ' \n')
        self.check_result('\t\n\n', '\t\n')
        self.check_result('\n\n ', '\n')
        self.check_result('\n\n\t', '\n')
        self.check_result(' \n \n ', ' \n')
        self.check_result('\t\n\t\n\t', '\t\n')

    def test_non_whitespace(self):
        self.none_removed('a')
        self.check_result('a\n', 'a')
        self.check_result('a\n ', 'a')
        self.check_result('a \n ', 'a')
        self.check_result('a \n\t', 'a')
        self.none_removed('-')
        self.check_result('-\n', '-')
        self.none_removed('.')
        self.check_result('.\n', '.')

    def test_unsupported_whitespace(self):
        self.none_removed('\v')
        self.none_removed('\n\v')
        self.check_result('\v\n', '\v')
        self.none_removed(' \n\v')
        self.check_result('\v\n ', '\v')


class WriteMethodTest(unittest.TestCase):
    def setUp(self):
        self.shell = PyShell.__new__(PyShell)
        self.shell.text = mock.Mock()
        self.shell.canceled = False
        
    def test_write_normal_line(self):
        line = 'This is a normal line of text.\n'
        result = self.shell.write(line)
        # Should insert the line with no special tags
        self.shell.text.insert.assert_any_call('iomark', line, ())
        self.shell.text.see.assert_called_with('end')
        self.assertEqual(result, len(line))
        
    def test_write_empty_line(self):
        line = '\n'
        result = self.shell.write(line)
        self.shell.text.insert.assert_any_call('iomark', line, ())
        self.shell.text.see.assert_called_with('end')
        self.assertEqual(result, len(line))
        
    def test_write_canceled(self):
        self.shell.canceled = True
        # Should reset canceled and raise KeyboardInterrupt
        with mock.patch.object(pyshell_mod, 'use_subprocess', False):
            with self.assertRaises(KeyboardInterrupt):
                self.shell.write('test\n')
        self.assertFalse(self.shell.canceled)    
        
    def test_write_traceback_line(self):
        # Simulate a traceback line
        line = '  File "foo.py", line 42, in <module>\n'
        result = self.shell.write(line)
        file_part = '  File "foo.py", '
        line_part = 'line 42'
        context_part = ', in <module>\n'
        self.shell.text.insert.assert_any_call('iomark', file_part, ())
        self.shell.text.insert.assert_any_call(f'iomark + {len(file_part)}c', line_part, ('traceback_lineno',))
        self.shell.text.insert.assert_any_call(f'iomark + {len(file_part) + len(line_part)}c', context_part, ())
        self.shell.text.see.assert_called_with('end')
        self.assertEqual(result, len(line))

        


if __name__ == '__main__':
    unittest.main(verbosity=2)
