
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

import pyautogui
from pynput import keyboard

pyautogui.PAUSE = 0            
pyautogui.MINIMUM_DURATION = 0 
pyautogui.FAILSAFE = True 


class AutoClicker(threading.Thread):

    def __init__(self, x, y, interval, button_name, follow_cursor, stop_event):
        super().__init__(daemon=True)
        self.x = x
        self.y = y
        self.interval = interval
        self.button_name = button_name
        self.follow_cursor = follow_cursor
        self.stop_event = stop_event

    def run(self):
        try:
            start = time.perf_counter()
            clicks_done = 0
            while not self.stop_event.is_set():
                if self.follow_cursor:
                    self.x, self.y = pyautogui.position()

                pyautogui.click(self.x, self.y, button=self.button_name)
                clicks_done += 1


                next_time = start + clicks_done * self.interval
                sleep_for = next_time - time.perf_counter()
                if sleep_for > 0:
                    time.sleep(sleep_for)
        except Exception as exc:
            messagebox.showerror("Autoclicker error", str(exc))
            self.stop_event.set()



class AutoClickerGUI:
    HOTKEY_START = "<ctrl>+<alt>+s"
    HOTKEY_STOP = "<ctrl>+<alt>+e"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Python Autoclicker")
        self.root.resizable(False, False)

        self.stop_event = threading.Event()
        self.click_thread = None

        self._build_widgets()
        self._setup_hotkeys()


    def _build_widgets(self):
        pad = {"padx": 8, "pady": 4}


        coord_frame = ttk.LabelFrame(self.root, text="Click position (pixels)")
        coord_frame.grid(row=0, column=0, sticky="ew", **pad)
        ttk.Label(coord_frame, text="X:").grid(row=0, column=0, **pad)
        ttk.Label(coord_frame, text="Y:").grid(row=0, column=2, **pad)
        self.entry_x = ttk.Entry(coord_frame, width=8)
        self.entry_y = ttk.Entry(coord_frame, width=8)
        self.entry_x.grid(row=0, column=1, **pad)
        self.entry_y.grid(row=0, column=3, **pad)


        self.follow_var = tk.BooleanVar(value=False)
        follow_cb = ttk.Checkbutton(
            coord_frame,
            text="Click at cursor",
            variable=self.follow_var,
            command=self._toggle_coord_entries,
        )
        follow_cb.grid(row=1, column=0, columnspan=4, sticky="w", **pad)

 
        interval_frame = ttk.Frame(self.root)
        interval_frame.grid(row=1, column=0, sticky="ew", **pad)
        ttk.Label(interval_frame, text="Interval (clicks/second):").grid(
            row=0, column=0, sticky="w", **pad
        )
        self.entry_cps = ttk.Entry(interval_frame, width=8)
        self.entry_cps.insert(0, "5")
        self.entry_cps.grid(row=0, column=1, **pad)

        ttk.Label(interval_frame, text="Button:").grid(row=0, column=2, sticky="w", **pad)
        self.button_var = tk.StringVar(value="left")
        ttk.Combobox(
            interval_frame,
            textvariable=self.button_var,
            values=("left", "right", "middle"),
            width=7,
            state="readonly",
        ).grid(row=0, column=3, **pad)


        btn_frame = ttk.Frame(self.root)
        btn_frame.grid(row=2, column=0, **pad)
        self.btn_start = ttk.Button(btn_frame, text="Start (Ctrl+Alt+S)", command=self.start)
        self.btn_stop = ttk.Button(btn_frame, text="Stop (Ctrl+Alt+E)", command=self.stop, state="disabled")
        self.btn_start.grid(row=0, column=0, **pad)
        self.btn_stop.grid(row=0, column=1, **pad)


        self.status_var = tk.StringVar(value="Inactive")
        self.status_label = ttk.Label(self.root, textvariable=self.status_var, foreground="red")
        self.status_label.grid(row=3, column=0, pady=(2, 8))

    def _toggle_coord_entries(self):
        """Enable / disable X & Y fields if follow-cursor is toggled."""
        state = "disabled" if self.follow_var.get() else "normal"
        self.entry_x.configure(state=state)
        self.entry_y.configure(state=state)

 
    def start(self):
        if self.click_thread and self.click_thread.is_alive():
            return

        follow_cursor = self.follow_var.get()

        try:
            cps = float(self.entry_cps.get())
            if cps <= 0:
                raise ValueError
            if follow_cursor:
                x, y = pyautogui.position()  
            else:
                x = int(self.entry_x.get())
                y = int(self.entry_y.get())
        except ValueError:
            messagebox.showwarning("Invalid input", "Please enter valid numbers.")
            return

        interval = 1.0 / cps
        self.stop_event.clear()
        self.click_thread = AutoClicker(
            x, y, interval, self.button_var.get(), follow_cursor, self.stop_event
        )
        self.click_thread.start()
        self._set_active(True)

    def stop(self):
        self.stop_event.set()
        self._set_active(False)

    def _set_active(self, active: bool):
        self.btn_start["state"] = "disabled" if active else "normal"
        self.btn_stop["state"] = "normal" if active else "disabled"
        self.status_var.set("Active" if active else "Inactive")
        self.status_label.configure(foreground="green" if active else "red")


    def _setup_hotkeys(self):
        def on_activate_start():
            self.root.event_generate("<<StartClicker>>", when="tail")

        def on_activate_stop():
            self.root.event_generate("<<StopClicker>>", when="tail")

        self.root.bind("<<StartClicker>>", lambda e: self.start())
        self.root.bind("<<StopClicker>>", lambda e: self.stop())

        listener = keyboard.GlobalHotKeys(
            {self.HOTKEY_START: on_activate_start, self.HOTKEY_STOP: on_activate_stop}
        )
        listener.daemon = True
        listener.start()


    def run(self):
        self.root.mainloop()
        self.stop_event.set()


if __name__ == "__main__":
    pyautogui.FAILSAFE = True  
    AutoClickerGUI().run()
