# Design Document

## Implemtation

#### Better Stack Traces

- implemented the keybind for clickable stack trace to call `goto_file_line` function and adjusted the function to handle conflicts with the keybinds.

![Image](https://github.com/user-attachments/assets/1d716029-5ebd-4538-a6e7-5c0f55ece79d)

- implemented underlining the line number in error stack traces 

![Image](https://github.com/user-attachments/assets/5c15bf3c-4bcc-4396-af6d-3afa64786c87)

- As for predicting error line, we plan to create a menu option that can take the user to the bottom line in the stack trace (as it is often the source of the error). We felt it may be annoying for experienced programmers, but making it optional may be useful for beginners to help them learn how to read and parse a stack trace. 

#### Syntax Errors

- implemented syntax error highlighting and message display using calltips and text tags. Logic is handled in explorer.py when `check_signal_event` is invoked based on the text being modified within a 4-second period. If the code has a syntax error, then `check_syntax` will display a calltip detailing the error message and underline the problematic line.

![Image](https://github.com/user-attachments/assets/cc703593-2036-46bf-b0d6-6d551cda2947)

#### Manual Debugging

#### Test Design

## Design Decisions

## Alternative Approach