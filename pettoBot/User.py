import Command_logic as cmd

class User:
    def __init__(self, name, petname, picture, personality, strength, wins, losses, coins):
        self.name = name
        self.petname = petname
        self.picture = picture
        self.personality = cmd.pickPersonality(personality)
        self.strength = strength
        self.wins = wins
        self.losses = losses
        self.coins = coins
