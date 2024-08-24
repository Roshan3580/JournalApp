# ROSHAN RAJ
# roshar1@uci.edu
# 90439894

# a5.py

import sys
from ui import create_ui
import admin
import tkinter as tk
from Tkinter import MainApp


def main():
    """
    Main function to start PyJournal.

    Displays a welcome message and prompts the user to choose a mode: admin or user.
    If 'admin' is chosen, admin mode is activated.
    If 'user' is chosen, user interface is created.
    'q' quits the program.

    Returns:
        None
    """
    print("Welcome to PyJournal!")
    while True:
        input_admin = input("What mode will you be using? (enter admin, user or q (to quit)): ").strip()
        if input_admin == 'user':
            create_ui()
        elif input_admin == 'admin':
            admin.admin()
        elif input_admin == 'q':
            sys.exit(0)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main = tk.Tk()
    main.title("ICS 32 Distributed Social Messenger")
    main.geometry("720x480")
    main.option_add('*tearOff', False)
    app = MainApp(main)
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    id = main.after(2000, app.check_new)
    print(id)
    main.mainloop()
