import random 

class CaptionThisGame: 
    def __init__(self, gameId, total_players=5, game_duration=0, thread_lock=None): 
        self.gameId = gameId 
        self.total_players = total_players 
        self.players = {} 
        self.captions = {} 
        self.timer = game_duration
        self.start_timer = False
        self.winners = [] 
        self.win_captions = [] 
        self.total_votes = 0 
        self.image = self.set_image()
        self.total_games = 0 
        self.ready = False 
        self.flag = "wait" 
        self.lock = thread_lock
        
    def is_ready(self): 
        return self.ready 

    def start_game(self):
        self.ready = True
        self.set_flag("caption")

    def get_gameId(self):
        return self.gameId

    def get_image(self):
        return self.image

    def set_image(self):
        return random.choice(random._os.listdir("images"))

    def get_flag(self): 
        return self.flag 
    
    def set_flag(self, flag): 
        self.flag = flag 
    
    def add_player(self, player_id, player_name): 
        self.players[player_id] = [player_name, 0] 
    
    def get_captions(self):
        return self.captions

    def add_caption(self, playerId, caption): 
        self.captions[playerId] = [caption, 0] 
    
    def all_players_submitted(self): 
        return True if len(self.captions) == len(self.players) else False 
    
    def get_votes(self): 
        return self.total_votes 
    
    def vote_caption(self, voted_player_id): 
        with self.lock:
            self.total_votes += 1 
            self.captions[voted_player_id][1] += 1 
    
    def all_players_voted(self): 
        return True if self.get_votes() == len(self.players) else False 
    
    def calculate_winners(self): 
        if not self.winners: 
            most_votes = 0 
            winners_id = [] 
            win_captions = [] 
            
            for player_id, value in self.captions.items(): 
                if value[1] > most_votes: 
                    most_votes = value[1] 
                    winners_id = [player_id] 
                    win_captions = [value[0]] 
                elif value[1] == most_votes: 
                    winners_id.append(player_id) 
                    win_captions.append(value[0]) 
        
            self.win_captions = win_captions
            
            # add bonus points
            for player in winners_id:
                self.players[player][1] += 1
                self.winners.append(self.players[player][0])
    
    def get_win_captions(self):
        return self.win_captions

    def get_winners(self):
        return self.winners

    def remove_player(self, player_id):
        del self.players[player_id]
        
        if self.captions.get(player_id):
            del self.captions[player_id]

    def is_playable(self):
        return True if len(self.players) > 1 else False

    def reset(self):
        if self.winners:
            self.captions = {}
            self.total_votes = 0
            self.image = self.set_image()
            self.winners = []
            self.set_flag("reset")

    def to_json(self):
        payload = {
            "game_id": self.get_gameId(),
            "flag": self.get_flag(),
            "ready": self.is_ready(),
            "game": {
                "total_players": self.total_players,
                "players": self.players,
                "image": self.get_image(),
                "timer": [self.start_timer, self.timer],
                "captions": self.get_captions(),
                "votes": self.get_votes()
            },
        }
        if self.get_flag() == "final":
            payload["game"]["winners"] = self.get_winners()
            payload["game"]["win_captions"] = self.get_win_captions()

        return payload