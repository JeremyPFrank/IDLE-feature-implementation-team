# Design Document

## Implemtation & Design Decisions

#### Better Stack Traces

- implemented the keybind for clickable stack trace to call `goto_file_line` function and adjusted the function to handle conflicts with the keybinds. We bound the `cntrl-left-click` event to attempt to naviagate to the file and line corresponding to cursor's position in the stack trace. This involved modifying the `goto_file_line` function to check if it was called from the right-click menu or from this keybind which we did by using the `event` parameter. This is becuase we don't want to print an error message every time the user uses these keys as it could get annoying. The left click action is also responsible for positioning the cursor and focusing the window, so we ran into some issues with this dual (now tri) responsibility. By manually refocusing the user and placing the cursor in the proper spot in `goto_file_line` these issues were avoided.

![Image](https://github.com/user-attachments/assets/1d716029-5ebd-4538-a6e7-5c0f55ece79d)

- implemented underlining the line number in error stack traces 

![Image](https://github.com/user-attachments/assets/5c15bf3c-4bcc-4396-af6d-3afa64786c87)

- As for predicting error line, we created a menu option that can take the user to the bottom line in the stack trace (as it is often the source of the error). We felt it may be annoying for experienced programmers, but making it optional may be useful for beginners to help them learn how to read and parse a stack trace. We created a right click menu option allowing the user to call the `predict_error_event` in `pyshell.py` which identifies the current pyshell instance and iterating through the text widget in reverse order, returning and navigating the user to the proper location once the bottom line of the stack trace is reached. If no stack trace exists or another error happens, an error message is displayed to the user.

#### Syntax Errors

- implemented syntax error highlighting and message display using calltips and text tags. Logic is handled in explorer.py when `check_signal_event` is invoked based on the text being modified within a 4-second period. If the code has a syntax error, then `check_syntax` will display a calltip detailing the error message and underline the problematic line.

![Image](https://github.com/user-attachments/assets/cc703593-2036-46bf-b0d6-6d551cda2947)

#### Manual Debugging

- To design the base for the ui window for manual debugging, we based the design off of the settings/config menu which inspired and helped lead us to the best classes and functions to use to cleanly create a new pop-up window. We make use of the `Text` and `Frame` classes to create the widget and allow `ManualDebug` to inheirit from `TopLevel` and `BaseWidget` to make use of the `setup()` and `destory()` functions. More elements of UI and functionality implementation can be found below.

![](debug_window_dia.png)

#### Test Design

## Alternative Approach