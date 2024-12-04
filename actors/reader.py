import tkinter as tk
import time


class Reader(tk.Tk):

    def __init__(self, name: str, shared_memory):
        super().__init__()
        self.title(name)
        self.geometry("200x100")
        self.name = name
        self.label_line = tk.Label(self, text="Read from shared memory:")
        self.output_line = tk.Label(self, height=3)
        self.read_button = tk.Button(
            self,
            text="Read",
            command=self.__on_read_button_clicked,
        )
        self.shm = shared_memory

    def __on_read_button_clicked(self):
        self.read_button.config(state=tk.DISABLED)
        text = self.shm.read()
        time.sleep(0.3)
        text = text if text else "<<None>>"
        self.output_line.config(text=text)
        self.read_button.config(state=tk.NORMAL)

    def mainloop(self, n=0):
        self.label_line.pack()
        self.output_line.pack()
        self.read_button.pack()
        return super().mainloop(n)
