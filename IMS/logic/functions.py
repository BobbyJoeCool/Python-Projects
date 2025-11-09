import tkinter as tk

# commonly used functions
def LimitRefocus(var: tk.StringVar, nextWidget: tk.Widget = None, maxLen: int = 8):
    def _callback(*_):
        value = var.get()
        if len(value) > maxLen:
            var.set(value[:maxLen])
        elif len(value) == maxLen and nextWidget:
            nextWidget.focus_set()

    var.trace_add("write", _callback)

def BindNextFocus(entry: tk.Widget, nextWidget: tk.Widget):
    def _callback(event):
        nextWidget.focus_set()
        return "break"
    entry.bind("<Tab>", _callback)