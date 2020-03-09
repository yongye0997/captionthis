import tkinter as tk
from PIL import Image, ImageTk
from utils.fonts import *


class CaptionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        display_container = tk.Frame(master=self)
        display_container.pack(fill="both", expand=True)
        display_container.rowconfigure(0, minsize=200, weight=1)
        display_container.columnconfigure(0, weight=1)

        info_container = tk.Frame(master=display_container)
        info_container.grid(row=0, column=0, sticky="nsew")
        info_container.rowconfigure(0, weight=1)
        info_container.columnconfigure(0, minsize=200, weight=1)

        self.image = tk.Label(master=info_container, image=None, text="Image Here")
        self.image.grid(row=0, column=0, sticky="nsew")

        count_container = tk.Frame(master=info_container)
        count_container.grid(row=0, column=1, sticky="nsew")
        count_container.rowconfigure(0, weight=1)
        count_container.columnconfigure(0, weight=1)

        self.submissions = tk.Label(master=count_container, text="0 caption", font=LARGE_FONT)
        self.submissions.grid(row=0, column=0, sticky="nsew", padx=20)

        self.count_down = tk.Label(master=count_container, text="60 seconds", font=LARGE_FONT)
        self.count_down.grid(row=1, column=0, sticky="nsew", padx=20)

        submit_container = tk.Frame(master=display_container)
        submit_container.grid(row=2, column=0, sticky="nsew", pady=50)
        submit_container.rowconfigure(0, weight=1)
        submit_container.columnconfigure(0, minsize=100, weight=1)

        self.ent_submit = tk.Entry(master=submit_container)
        self.ent_submit.grid(row=0, column=0, sticky="ew", padx=10)

        self.btn_submit = tk.Button(master=submit_container, text="Submit", command=self.submit, )
        self.btn_submit.grid(row=0, column=1, sticky="ew", padx=10, ipadx=50, ipady=10)

    def has_image(self):
        return self.image["image"]

    def create_image(self, source):
        image = Image.open(f"images\\{source}")
        photo = ImageTk.PhotoImage(image)
        self.image.configure(image=photo)
        self.image.image = photo

    def update_submission_count(self, total_submissions):
        self.submissions.configure(text=f"{total_submissions} caption")

    def submit(self):
        caption = self.ent_submit.get()

        # controller.send("caption", caption)

        self.ent_submit.delete(0, tk.END)
        self.ent_submit.configure(state="disabled")
        self.btn_submit.configure(state="disabled")