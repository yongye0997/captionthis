import tkinter as tk 

# custom packages
from utils.fonts import LARGE_FONT

class WaitPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.lbl_info = tk.Label(text="", font=LARGE_FONT)
        self.lbl_info.pack(expand=True, fill="both")
    
        btn_next = tk.Button(master=self, text="next", command=lambda: controller.show_frame("CaptionPage"))
        btn_next.pack()

    def update_info(self, text):
        '''update message to display on the page'''
        self.lbl_info["text"] = text