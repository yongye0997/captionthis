import tkinter as tk 
from src import pages
from src import socket_client
from PIL import Image, ImageTk


class CaptionThis(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.current_frame = ''
        self.current_image = None

        # where I will stack and switch frames
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in pages.__all__:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("ConnectPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        if self.current_frame != page_name:
            frame = self.frames[page_name]
            frame.tkraise()

            self.current_frame = page_name

    def connect(self, payload):
        '''Connect to the server then start to listen'''

        # connect to the server
        if not socket_client.connect(**payload, error_callback=self.error_handler):
            return

        socket_client.start_listen(self.server_message_handler, self.error_handler)
        
        # redirect client to wait page
        info = "Joining {}:{} as {}".format(*payload.values())
        self.frames["WaitPage"].update_info(info)
        self.show_frame("WaitPage")

    def send(self, cmd, msg):

        if cmd == "caption":
            socket_client.send(f"c {msg}")
        elif cmd == "vote":
            socket_client.send(f"v {msg}")
        elif cmd == "reset":
            socket_client.send("r 0")
        elif cmd == "new":
            socket_client.send("r 1")

    def server_message_handler(self, game: dict):
        '''Handle responses from the server'''
        if not game["ready"]:
            info = f"Waiting for {game['game']['total_players'] - len(game['game']['players'])} more players..."
            self.frames["WaitPage"].update_info(info)
        else:
            
            flag = game["flag"]

            if flag == "quit":
                print("Quitting the game.")
                self.error_handler("The game will hereby suspend since there is not enough player.")

            if flag == "reset":
                self.reset()

                flag = "caption"

            if flag == "done":
                self.show_frame("FinalPage")

                final_page = self.frames["FinalPage"]

                final_page.update_winner(game["game"]["memelords"])

            elif flag == "caption":
                self.show_frame("CaptionPage")

                caption_page = self.frames["CaptionPage"]

                if not caption_page.has_image():
                    caption_page.upload_image(self.create_image(game["game"]["image"]))

                if game["game"]["timer"][0]:
                    caption_page.start_count_down()
                else:
                    caption_page.set_count_down(game["game"]["timer"][1])
                caption_page.update_submission_count(len(game["game"]["captions"]))
            
            elif flag == "vote":
                # stop the countdown in caption page
                self.frames["CaptionPage"].stop_count_down()

                self.show_frame("VotePage")
                
                vote_page = self.frames["VotePage"]
                
                if not vote_page.has_image():
                    vote_page.upload_image(self.create_image(game["game"]["image"]))
                    
                if not vote_page.has_options:
                    vote_page.create_options(game["game"]["captions"])
                    
                vote_page.update_submission_count(game["game"]["votes"])
                
            elif flag == "win":
                self.show_frame("WinPage")
                
                win_page = self.frames["WinPage"]
                
                if not win_page.has_image():
                    win_page.upload_image(self.create_image(game["game"]["image"]))

                win_page.display_caption(game["game"]["win_captions"])
                
                win_page.display_winners(game["game"]["winners"])
                
                # switch to leaderboard page in 5 seconds 
                self.after(5 * 1000, lambda: self.switch_to_leaderboard(game))
    
    def switch_to_leaderboard(self, game):
        self.frames["LeaderboardPage"].add_players(game["game"]["players"])
        self.frames["LeaderboardPage"].update_dashboard(game["game"])
        self.show_frame("LeaderboardPage")

    def create_image(self, source):
        if not self.current_image:
            image = Image.open(f"src\\images\\{source}")
            photo = ImageTk.PhotoImage(image)
            self.current_image = photo
        return self.current_image

    def reset(self):
        for frame in self.frames.values():
            frame.reset()

    def error_handler(self, message):
        '''display error message to wait page and exit'''
        self.frames["WaitPage"].update_info(message)
        self.show_frame("WaitPage")
        # quit after 10 seconds
        self.after(10 * 1000, self.quit)
