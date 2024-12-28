import Database as db
import random
import time
import Personalities, Actions, Food

### INITIALIZE OBJECTS

def __init__():
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
    
    values = [user, gender, personality.name, adoptiondate, picture]
    items = ["owner", "gender", "personality", "adoption_date", "picture"]
    
    db.insert("petbot", items, values)
    return f"PettoBot: Congratulations! You successfully adopted a new pet!\n\nJordy: {personality.adoption}"


def change_name(user, name):
    if (len(name) > 100):
        return "PettoBot: Whoops, looks like the name you suggested is too long!"
    
    if (not hasadopted(user)):
        return "PettoBot: You do not have a pet!"
    
    db.update("petbot", ["name"], [name], "owner", user)
    return f"PettoBot: Alright! Your pet's name will now be {name}"


def profile(user):
    items = ["name", "owner", "picture", "gender", "adoption_date", "love_points", "battle_wins", "battle_losses", "personality", "coins"]
    results = db.select("petbot", items, "owner", user)
    return results
    

def action(user, num):
    if (not hasadopted(user)):
        return "PettoBot: You do not have a pet!"
    
    action = str(actions[num].name)
    results = db.select("petbot", ["name", action + "_time"], "owner", user)
    
    if action == "pet":
        pastForm = "petted"
    else:
        pastForm = action + "ed"
    
    currenttime = time.time()
    
    if (num != 3):
        if (currenttime - float(results[1]) < float(actions[num].time_limit) * 60):
            return f"PettoBot: You have already {pastForm} {results[0]}. Wait {actions[num].time_limit} minutes to {action} again."
    else:
        lovePoints = int(db.select("petbot", ["love_points"], "owner", user)[0])
        if (currenttime - float(results[1]) < float(actions[num].time_limit) * 60):
            return f"PettoBot: {results[0]} has already {pastForm}. Wait {actions[num].time_limit} minutes to {action} again."
        
        if lovePoints < int(actions[num].required_love):
            return f"PettoBot: {results[0]} does not have enough love points for battle."


def show_love(user, num):
    action = str(actions[num].name)
    results = db.select("petbot", ["love_points", "name", "personality", "picture"], "owner", user)
    love_points = int(results[0])
    love_points += int(actions[0].love)
    db.update("petbot", ["love_points", action + "_time", "hasloved"], [love_points, time.time(), 1], "owner", user)
    personality = pickPersonality(results[2])
    if num == 0:
        loveOptions = [personality.pet1, personality.pet2]
    elif num == 1:
        loveOptions = [personality.walk1, personality.walk2]
    return [results[1], random.choice(loveOptions), results[3], actions[0].love]


def train(user):
    results = db.select("petbot", ["strength_points", "name", "personality", "picture"], "owner", user)
    db.update("petbot", ["strength_points", "train_time"], [int(results[0]) + int(actions[2].strength), time.time()], "owner", user)
    personality = pickPersonality(results[2])
    return [results[1], personality.train, results[3]]


def battle(challenger, opponent):
    challengerStrength = int(db.select("petbot", ["strength_points"], "owner", challenger)[0])
    opponentStrength = int(db.select("petbot", ["strength_points"], "owner", opponent)[0])
    db.update("petbot", ["battle_time"], [time.time()], "owner", challenger)
    db.update("petbot", ["battle_time"], [time.time()], "owner", opponent)
    
    if challengerStrength > opponentStrength:
        return challenger
    elif challengerStrength < opponentStrength:
        return opponent
    else:
        return "tie"

    
def winnerAndLoser(winner, loser):
    winData = db.select("petbot", ["name", "personality", "coins", "picture", "battle_wins"], "owner", winner)
    loseData = db.select("petbot", ["name", "personality", "coins", "picture", "battle_losses"], "owner", loser)
    totalCoins = int(winData[2]) + int(loseData[2])
    db.update("petbot", ["battle_wins", "coins"], [int(winData[4]) + 1, totalCoins], "owner", winner)
    db.update("petbot", ["battle_losses", "coins"], [int(loseData[4]) + 1, 0], "owner", loser)
    return [winData[0], winData[1], winData[3], loseData[0], loseData[1], loseData[3]]
    


### HELPER FUNCTIONS

def pickPersonality(pers, personalities):
    if (pers == "Energetic"):
        return personalities[0]
    elif (pers == "Gloomy"):
        return personalities[1]
    elif (pers == "Aggressive"):
        return personalities[2]

def hasadopted(user):
    results = db.select("petbot", "owner")
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