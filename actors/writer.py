import tkinter as tk
import time


class Writer(tk.Tk):

    def __init__(self, name: str, shared_memory):
        super().__init__()
        self.title(name)
        self.geometry("200x100")
        self.name = name
        self.label_line = tk.Label(self, text="Write to shared memory:")
        self.input_line = tk.Entry(self)
        self.write_button = tk.Button(
            self,
            text="Write",
            command=self.__on_write_button_clicked,
        )
        self.shm = shared_memory

    def __on_write_button_clicked(self):
        text = self.input_line.get()
        if text:
            self.write_button.config(state=tk.DISABLED)
            self.input_line.delete(0, "end")
            self.shm.write(text)
            time.sleep(0.3)
            self.write_button.config(state=tk.NORMAL)

    def mainloop(self, n=0):
        self.label_line.pack()
        self.input_line.pack()
        self.write_button.pack()
        return super().mainloop(n)
