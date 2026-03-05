from tools import configureLogging


def main():
    import sys
    import tkinter as tk

    from gui import GUI, LoginScreen

    # TODO: Add a minimal GUI smoke test that instantiates the app with a mocked DB.
    root = tk.Tk()
    root.withdraw()

    login = LoginScreen(root)
    login.grab_set()
    root.wait_window(login)

    if login.result is None:
        root.destroy()
        sys.exit()
    else:
        conn, user = login.result
        root.deiconify()
        GUI(root, conn, user)
        root.mainloop()

    conn.close()
    sys.exit()


if __name__ == "__main__":
    configureLogging()
    main()
