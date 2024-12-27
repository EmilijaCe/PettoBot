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
    items = ["love_points", "name", action + "_time"]
    results = db.select("petbot", items, "owner", user)
    
    if action == "pet":
        pastForm = "petted"
    else:
        pastForm = action + "ed"
    
    currenttime = time.time()
    if (currenttime - float(results[2]) < float(actions[num].time_limit) * 60):
        return f"PettoBot: You have already {pastForm} {results[1]}. Wait {actions[num].time_limit} minutes to {action} again."
    
    if int(results[0]) < int(actions[num].required_love):
        return f"PettoBot: {results[1]} does not have enough love points for battle."


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