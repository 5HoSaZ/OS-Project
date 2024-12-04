import tkinter as tk
import tkinter.scrolledtext as st


class User(tk.Tk):
    def __init__(self, name: str):
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

    def __on_send_button_clicked(self):
        text = self.input_line.get()
        if text:
            message = f"{self.name}: {text}"
            self.scroll_text.insert(tk.INSERT, message + "\n")
            self.input_line.delete(0, "end")

    def mainloop(self, n=0):
        self.scroll_text.pack()
        self.input_line.pack()
        self.send_button.pack()
        return super().mainloop(n)


if __name__ == "__main__":
    u1 = User("User")
    u1.mainloop()
