import tkinter as tk


class PromptWindow(object):
    def __init__(self, master):
        self.master = master
        self.win = tk.Toplevel(master)
        self.win.title("Prompt Window")

        # Intercept close window events so that when the user closes this window
        # (via the close widget or the Enter button) the main window reopens
        self.win.protocol("WM_DELETE_WINDOW", self.close)

        frame = tk.Frame(self.win, height=500, padx=20, pady=20)
        frame.pack()

        # Build prompt window labels
        tk.Label(frame, text="Username").grid(row=0)
        tk.Label(frame, text="Password").grid(row=1)

        # Build prompt window entry widgets
        self.username = tk.StringVar()
        tk.Entry(frame, textvariable=self.username).grid(row=0, column=1)

        self.password = tk.StringVar()
        tk.Entry(frame, textvariable=self.password).grid(row=1, column=1)

        # Build enter button
        tk.Button(frame, text="Enter", command=self.close).grid(row=2, column=1)

    def close(self):
        # Close this window
        self.win.destroy()
        # Reopen the main window
        self.master.deiconify()
        self.returnData

    def returnData(self):
        username = self.username.get()
        password = self.password.get()
        return username, password


class MainWindow(object):
    def __init__(self):
        # Create root window
        root = tk.Tk()
        # and make it invisible
        root.withdraw()
        root.title("Main Window")

        # Add some widgets
        tk.Label(root, text="Done").pack()
        tk.Button(root, text="Show data", command=self.show_data).pack()

        # Create prompt window
        self.prompt = PromptWindow(root)

        # Loop forever
        root.mainloop()

    # Display the data gathered by the prompt window
    def show_data(self):
        prompt = self.prompt
        username = prompt.username.get()
        password = prompt.password.get()

        fmt = 'username: {!r}, password: {!r}'
        print(fmt.format(username, password))


MainWindow()
