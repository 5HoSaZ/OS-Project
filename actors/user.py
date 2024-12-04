import tkinter as tk
import tkinter.scrolledtext as st
from threading import Thread


class User(tk.Tk):
    def __init__(self, name: str, monitor, event):
        super().__init__()
        self.title(name)
        self.name = name
        self.input_line = tk.Entry(self)
        self.scroll_text = st.ScrolledText(
            self,
            width=30,
            height=8,
            font=("Times New Roman", 15),
        )
        self.send_button = tk.Button(
            self,
            text="Send",
            command=self.__on_send_button_clicked,
        )
        self.monitor = monitor
        self.read_event = event
        self.protocol("WM_DELETE_WINDOW", self.__on_closing)

    def event_listener(self):
        while True:
            # Wait for new read event
            self.read_event.wait()
            # Get new message from monitor
            new_msg = self.monitor.shm_read()
            # Log the new message
            self.scroll_text.insert(tk.INSERT, new_msg + "\n")
            self.scroll_text.see(tk.END)
            # Clear the event
            self.read_event.clear()

    def __on_closing(self):
        message = f"{self.name} has exited!"
        print(message)
        self.monitor.user_exit(message)
        self.destroy()

    def __on_send_button_clicked(self):
        if text := self.input_line.get():
            message = f"{self.name}: {text}"
            self.input_line.delete(0, "end")
            self.monitor.shm_write(message)

    def mainloop(self, n=0):
        Thread(target=self.event_listener, daemon=True).start()
        self.scroll_text.pack()
        self.input_line.pack()
        self.send_button.pack()
        return super().mainloop(n)


if __name__ == "__main__":
    u1 = User("User")
    u1.mainloop()
