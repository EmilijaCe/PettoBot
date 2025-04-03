import random
import time
import User

class Command_logic:

    def __init__(self, defaultItems: list, defaultValues: list, initial, database):
        self.defaultItems = defaultItems
        self.defaultValues = defaultValues
        self.initial = initial
        self.db = database
    
    
    ### MAIN FUNCTIONS

    def adopt(self, user, gender):
        if (self.hasadopted(user)):
            return "PettoBot: Oops! Looks like you already have a pet."
        
        gender = self.pickGender(gender)
        personality = random.choice(self.initial.get_personalities())
        
        picture = random.choice(self.initial.get_pictures())

        adoptiondate = time.strftime("%d-%m-%Y, %H:%M:%S", time.localtime())
        
        values = [user, gender, personality.name, adoptiondate, picture] + self.defaultValues
        items = ["id", "gender", "personality", "adoption_date", "picture"] + self.defaultItems
        
        self.db.insert(items, values)
        return f"PettoBot: Congratulations! You successfully adopted a new pet!\n\nJordy: {personality.adoption}"


    def change_name(self, user, name):
        if (len(name) > 100):
            return "PettoBot: Whoops, looks like the name you suggested is too long!"
        
        if (not self.hasadopted(user)):
            return "PettoBot: You do not have a pet!"
        
        self.db.update(["name"], [name], "id", user)
        return f"PettoBot: Alright! Your pet's name will now be {name}"


    def profile(self, user):
        items = ["name", "id", "picture", "gender", "adoption_date", "love_points", "battle_wins", "battle_losses", "personality", "coins"]
        results = self.db.select(items, "id", user)[0]
        return results
        

    def action_valid(self, user, action):
        if (not self.hasadopted(user)):
            return "PettoBot: You do not have a pet!"
        
        results = self.db.select(["name", action.name + "_time", "love_points"], "id", user)[0]
        pastForm = self.pickPastForm(action)
        
        currenttime = time.time()
        
        if (action.name != "battle"):
            if (currenttime - float(results[1]) < float(action.time_limit) * 60):
                return f"PettoBot: You have already {pastForm} {results[0]}. Wait {action.time_limit} minutes to {action.name} again."
        else:
            lovePoints = int(results[2])
            if (currenttime - float(results[1]) < float(action.time_limit) * 60):
                return f"PettoBot: {results[0]} has already {pastForm}. Wait {action.time_limit} minutes to {action.name} again."
            
            if lovePoints < int(action.required_love):
                return f"PettoBot: {results[0]} does not have enough love points for battle."


    def show_love(self, user, action):
        results = self.db.select(["love_points", "name", "personality", "picture"], "id", user)[0]
        love_points = int(results[0]) + int(action.love)
        self.db.update(["love_points", action.name + "_time", "hasloved"], [love_points, time.time(), 1], "id", user)
        personality = self.pickPersonality(results[2])
        
        if action.name == "pet":
            loveOptions = [personality.pet1, personality.pet2]
        elif action.name == "walk":
            loveOptions = [personality.walk1, personality.walk2]
        
        return results[1], random.choice(loveOptions), results[3], action.love


    def train(self, user, action):
        results = self.db.select(["strength_points", "name", "personality", "picture"], "id", user)[0]
        self.db.update(["strength_points", "train_time"], [int(results[0]) + int(action.strength), time.time()], "id", user)
        personality = self.pickPersonality(results[2])
        
        return results[1], personality.train, results[3]


    def battle(self, challenger, opponent):
        results1 = self.db.select(["name", "picture", "personality", "strength_points", "battle_wins", "battle_losses", "coins"], "id", challenger)[0]
        results2 = self.db.select(["name", "picture", "personality", "strength_points", "battle_wins", "battle_losses", "coins"], "id", opponent)[0]
        
        userChallenger = User.User(challenger, results1[0], results1[1], self.pickPersonality(results1[2]), results1[3], results1[4], results1[5], results1[6])
        userOpponent = User.User(opponent, results2[0], results2[1], self.pickPersonality(results2[2]), results2[3], results2[4], results2[5], results2[6])
        
        self.db.update(["battle_time"], [time.time()], "id", challenger)
        self.db.update(["battle_time"], [time.time()], "id", opponent)
        
        if userChallenger.strength > userOpponent.strength:
            winner = userChallenger
            loser = userOpponent
        elif userChallenger.strength < userOpponent.strength:
            winner = userOpponent
            loser = userChallenger
        else:
            return None, None
        
        totalCoins = int(winner.coins) + int(loser.coins)
        self.db.update(["battle_wins", "coins"], [int(winner.wins) + 1, totalCoins], "id", winner.name)
        self.db.update(["battle_losses", "coins"], [int(loser.losses) + 1, 0], "id", loser.name)
        
        return winner, loser
        



    ### HELPER FUNCTIONS

    def pickPersonality(self, pers):
        personalities = self.initial.get_personalities()
        for personality in personalities:
            if pers == personality.name:
                return personality


    def hasadopted(self, user):
        results = self.db.select(["id"])
        for result in results:
            if str(result[0]) == user:
                return True
        return False

    def pickGender(self, gender):
        if gender == 'F':
            return "Female"
        elif gender == 'M':
            return "Male"
        elif gender == 'N':
            return "Neutral"
    
    def pickPastForm(self, action):
        if action.name == "pet":
            pastForm = action.name + "ted"
        elif action.name[len(action.name) - 1] == 'e':
            pastForm = action.name + "d"
        elif action.name != "":
            pastForm = action.name + "ed"
            
        return pastForm