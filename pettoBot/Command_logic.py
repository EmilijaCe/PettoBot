import Database as db
import random
import time
import Personalities, Actions, Food, User

defaultItems = ["name", "love_points", "strength_points", "coins", "battle_wins", "battle_losses", "pet_time", "walk_time", "train_time", "battle_time", "tookcoin", "hasloved"]
defaultValues = ["Jordy", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0", "0"]

### INITIALIZE OBJECTS


with open('pettoBot/personalities.txt', 'r') as file:
    global personalities
    personalities = []
    for line in file:
        pers = line.split("/")
        personality = Personalities.Personalities(pers[0], pers[1], pers[2], pers[3], pers[4], pers[5], pers[6], pers[7], pers[8], pers[9], pers[10], pers[11], pers[12])
        personalities.append(personality)

with open('pettoBot/food.txt', 'r') as file:
    global food
    food = []
    for line in file:
        fd = line.split()
        food.append(Food.Food(fd[0], fd[1], fd[2]))
        
with open('pettoBot/actions.txt', 'r') as file:
    global actions
    actions = []
    for line in file:
        ac = line.split()
        actions.append(Actions.Actions(ac[0], ac[1], ac[2], ac[3], ac[4]))


### MAIN FUNCTIONS

def adopt(user, gender):
    if (hasadopted(user)):
        return "PettoBot: Oops! Looks like you already have a pet."
    gender = pickGender(gender)
    personality = random.choice(personalities)
    
    picturelist = open("pettoBot/pictures.txt").readlines()
    picture = random.choice(picturelist)

    adoptiondate = time.strftime("%d-%m-%Y, %H:%M:%S", time.localtime())
    
    values = [user, gender, personality.name, adoptiondate, picture] + defaultValues
    items = ["id", "gender", "personality", "adoption_date", "picture"] + defaultItems
    
    db.insert(items, values)
    return f"PettoBot: Congratulations! You successfully adopted a new pet!\n\nJordy: {personality.adoption}"


def change_name(user, name):
    if (len(name) > 100):
        return "PettoBot: Whoops, looks like the name you suggested is too long!"
    
    if (not hasadopted(user)):
        return "PettoBot: You do not have a pet!"
    
    db.update("petbot", ["name"], [name], "id", user)
    return f"PettoBot: Alright! Your pet's name will now be {name}"


def profile(user):
    items = ["name", "id", "picture", "gender", "adoption_date", "love_points", "battle_wins", "battle_losses", "personality", "coins"]
    results = db.select(items, "id", user)[0]
    return results
    

def action(user, num):
    if (not hasadopted(user)):
        return "PettoBot: You do not have a pet!"
    
    action = str(actions[num].name)
    results = db.select(["name", action + "_time"], "id", user)[0]
    if action == "pet":
        pastForm = "petted"
    elif action[len(action) - 1] == 'e':
        pastForm = action + "d"
    else:
        pastForm = action + "ed"
    
    currenttime = time.time()
    
    if (num != 3):
        if (currenttime - float(results[1]) < float(actions[num].time_limit) * 60):
            return f"PettoBot: You have already {pastForm} {results[0]}. Wait {actions[num].time_limit} minutes to {action} again."
    else:
        lovePoints = int(db.select(["love_points"], "id", user)[0][0])
        if (currenttime - float(results[1]) < float(actions[num].time_limit) * 60):
            return f"PettoBot: {results[0]} has already {pastForm}. Wait {actions[num].time_limit} minutes to {action} again."
        
        if lovePoints < int(actions[num].required_love):
            return f"PettoBot: {results[0]} does not have enough love points for battle."


def show_love(user, num):
    action = str(actions[num].name)
    results = db.select(["love_points", "name", "personality", "picture"], "id", user)[0]
    love_points = int(results[0])
    love_points += int(actions[0].love)
    db.update(["love_points", action + "_time", "hasloved"], [love_points, time.time(), 1], "id", user)
    personality = pickPersonality(results[2])
    if num == 0:
        loveOptions = [personality.pet1, personality.pet2]
    elif num == 1:
        loveOptions = [personality.walk1, personality.walk2]
    return results[1], random.choice(loveOptions), results[3], actions[0].love


def train(user):
    results = db.select(["strength_points", "name", "personality", "picture"], "id", user)[0]
    db.update(["strength_points", "train_time"], [int(results[0]) + int(actions[2].strength), time.time()], "id", user)
    personality = pickPersonality(results[2])
    return results[1], personality.train, results[3]


def battle(challenger, opponent):
    results1 = db.select(["name", "picture", "personality", "strength_points", "battle_wins", "battle_losses", "coins"], "id", challenger)[0]
    results2 = db.select(["name", "picture", "personality", "strength_points", "battle_wins", "battle_losses", "coins"], "id", opponent)[0]
    
    userChallenger = User.User(challenger, results1[0], results1[1], results1[2], results1[3], results1[4], results1[5], results1[6])
    userOpponent = User.User(opponent, results2[0], results2[1], results2[2], results2[3], results2[4], results2[5], results2[6])
    
    db.update(["battle_time"], [time.time()], "id", challenger)
    db.update(["battle_time"], [time.time()], "id", opponent)
    
    if userChallenger.strength > userOpponent.strength:
        winner = userChallenger
        loser = userOpponent
    elif userChallenger.strength < userOpponent.strength:
        winner = userOpponent
        loser = userChallenger
    else:
        return None, None
    
    totalCoins = int(winner.coins) + int(loser.coins)
    db.update(["battle_wins", "coins"], [int(winner.wins) + 1, totalCoins], "id", winner.name)
    db.update(["battle_losses", "coins"], [int(loser.losses) + 1, 0], "id", loser.name)
    
    return winner, loser
    



### HELPER FUNCTIONS

def pickPersonality(pers):
    if (pers == "Energetic"):
        return personalities[0]
    elif (pers == "Gloomy"):
        return personalities[1]
    elif (pers == "Aggressive"):
        return personalities[2]

def hasadopted(user):
    results = db.select(["id"])
    for result in results:
        if str(result[0]) == user:
            return True
    return False

def pickGender(gender):
    if gender == 'F':
        return "Female"
    elif gender == 'M':
        return "Male"
    elif gender == 'N':
        return "Neutral"