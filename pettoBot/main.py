import time
import discord
import random
import mysql.connector
from discord.ui import Button, View
import Personalities, Actions, Food


'''
things to improve:
1. find out how to run two tasks at the same time -> schedule times to reset daily coins and love points
2. set environment variables for database and token
3. fix battle buttons: add timeout, make them available only for the opponent (no one else can press them)
4. extend the program: add food options, more personalities, explore the possibility of having multiple pets
5. draw pictures for pets and bot's profile
6. (if there is a possibility) find a way to modify pictures for commands (add elements, make a gif, etc.)
7. find a better way to store personality comments
'''

# SET VARIABLES

password = input("MYSQL password: ")
token = input("Discord bot token: ")

# CONNECT BOT

bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


# CONNECT MYSQL

con = mysql.connector.connect(host = 'localhost', user = 'root', password = password, database = 'bots')
mycursor = con.cursor()


# INITIALIZE OBJECTS

with open('pettoBot/personalities.txt', 'r') as file:
    count = 0
    for line in file:
        pers = line.split("/")
        count += 1
        if count == 1:
            continue
        personality = Personalities.Personalities(pers[0], pers[1], pers[2], pers[3], pers[4], pers[5], pers[6], pers[7], pers[8], pers[9], pers[10], pers[11], pers[12])
        if count == 2:
            global energetic
            energetic = personality
        elif count == 3:
            global gloomy
            gloomy = personality
        elif count == 4:
            global agressive
            aggressive = personality

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


############ COMMANDS ################

# adopt
@bot.slash_command(description = "Adopts a new pet")
async def adopt(ctx, *, gender):
    owner = ctx.author.id
    
    if (hasAdopted(str(owner))):
        await ctx.respond("PettoBot: Oops! Looks like you already have a pet.")
        return
    
    if gender == 'F':
        gend = "Female"
    elif gender == 'M':
        gend = "Male"
    elif gender == 'N':
        gend = "Neutral"

    personalities = [energetic, gloomy, aggressive]
    personality = random.choice(personalities)
    
    picturelist = open("pettoBot/pictures.txt").readlines()
    picture = random.choice(picturelist)
    
    currenttime = time.localtime()
    adoptiondate = time.strftime("%d-%m-%Y, %H:%M:%S", currenttime)
    
    val = (owner, gend, personality.name, adoptiondate, picture)
    mycursor.execute("insert into petbot (owner, gender, personality, adoption_date, picture) values(%s, %s, %s, %s, %s);", val)
    con.commit()
    
    await ctx.respond(f"PettoBot: Congratulations! You successfully adopted a new pet!\n\nJordy: {personality.adoption}")


# change name
@bot.slash_command(description = "Changes the name of the pet")
async def change_name(ctx, *, name):
    if (len(name) > 100):
        await ctx.respond("PettoBot: Whoops, looks like the name you suggested is too long!")
        return
    
    user = ctx.author.id
    if (not hasAdopted(str(user))):
        ctx.respond("PettoBot: You do not have a pet!")
        return
    mycursor.execute(f"update petbot set name = '{name}' where owner = {user};")
    con.commit()
    
    await ctx.respond("PettoBot: Alright! Your pet's name will now be " + name)
    

# profile
@bot.slash_command(description = "Shows pet's profile")
async def profile(ctx):
    user = ctx.author.id
    if (not hasAdopted(str(user))):
        await ctx.respond("PettoBot: You do not have a pet!")
        return
    mycursor.execute(f"select name, owner, picture, gender, adoption_date, love_points, battle_wins, battle_losses, personality, coins from petbot where owner = {user};")
    results = mycursor.fetchone()
    
    name = str(results[0])
    id = int(results[1])
    picture = str(results[2])
    gender = str(results[3])
    adoption_date = str(results[4])
    love_points = str(results[5])
    battle_wins = str(results[6])
    battle_losses = str(results[7])
    pers = str(results[8])
    coins = str(results[9])
    
    if (pers == "Energetic"):
        col = discord.Color.yellow()
        personality = energetic
    elif(pers == "Gloomy"):
        col = discord.Color.blue()
        personality = gloomy
    elif (pers == "Aggressive"):
        col = discord.Color.red()
        personality = aggressive
        
    user = ctx.author.name
    
    embed=discord.Embed(title= name + "'s profile", url = None, color=col)
    embed.set_image(url = picture)
    embed.add_field(name = "Owner: " + user, value = "", inline = True)
    embed.add_field(name = "Gender: " + gender, value = "", inline = True)
    embed.add_field(name = "", value = "", inline = False)
    embed.add_field(name = "Personality: " + pers, value = "", inline = True)
    embed.add_field(name = "Adoption date: " + adoption_date[:10], value = "", inline = True)
    embed.add_field(name = "", value = "", inline = False)
    embed.add_field(name = "Coins: " + coins, value = "", inline = True)
    embed.add_field(name = "Love points: " + love_points, value = "", inline = True)
    embed.add_field(name = "", value = "", inline = False)
    embed.add_field(name = "Battle wins: " + battle_wins, value = "", inline = True)
    embed.add_field(name = "Battle losses: " + battle_losses, value = "", inline = True)
    
    await ctx.respond(f"{name}: {personality.profile}")
    await ctx.send(embed=embed)


# pet
@bot.slash_command(description = "Shows love to your pet")
async def pet(ctx):
    user = ctx.author.id
    if (not hasAdopted(str(user))):
        await ctx.respond("PettoBot: You do not have a pet!")
        return
    
    mycursor.execute(f"select love_points, name, pet_time, picture, personality from petbot where owner = {user};")
    results = mycursor.fetchone()
    pet_time = results[2]
    name = results[1]
    pet_time = float(pet_time)
    currenttime = time.time()
    if (currenttime - pet_time < float(actions[0].time_limit) * 60):
        await ctx.respond(f"PettoBot: You have already petted {name}. Wait {actions[0].time_limit} minutes to pet again.")
    else:
        love = results[0]
        pers = results[4]
        picture = results[3]
        personality = pickPersonality(pers)
        
        love = int(love)
        love += int(actions[0].love)
        mycursor.execute(f"update petbot set love_points = {love}, hasloved = 1, pet_time = {currenttime} where owner = {user};")
        con.commit()
        
        petOptions = [personality.pet1, personality.pet2]
        await ctx.respond(f"{name}: {random.choice(petOptions)}")
        await ctx.send(picture)
        await ctx.send(f"\n+{actions[0].love} love points")


# walk
@bot.slash_command(description = "Shows love to your pet")
async def walk(ctx):
    user = ctx.author.id
    if (not hasAdopted(str(user))):
        await ctx.respond("PettoBot: You do not have a pet!")
        return
    
    mycursor.execute(f"select love_points, name, walk_time, picture, personality from petbot where owner = {user};")
    results = mycursor.fetchone()
    walk_time = results[2]
    name = results[1]
    walk_time = float(walk_time)
    currenttime = time.time()
    if (currenttime - walk_time < float(actions[1].time_limit) * 60):
        await ctx.respond(f"PettoBot: You have already gone on a walk with {name}. Wait {actions[1].time_limit} minutes to go again.")
    else:
        love = results[0]
        pers = results[4]
        picture = results[3]
        personality = pickPersonality(pers)
        
        love = int(love)
        love += int(actions[1].love)
        mycursor.execute(f"update petbot set love_points = {love}, walk_time = {currenttime} where owner = {user};")
        con.commit()
        
        walkOptions = [personality.walk1, personality.walk2]
        await ctx.respond(f"{name}: {random.choice(walkOptions)}")
        await ctx.send(picture)
        await ctx.send(f"\n+{actions[1].love} love points")
    
    
# daily coins
@bot.slash_command(description = "Collects daily coins")
async def daily(ctx):
    user = ctx.author.id
    if (not hasAdopted(str(user))):
        await ctx.respond("PettoBot: You do not have a pet!")
        return
    mycursor.execute(f"select tookcoin, coins, name, personality from petbot where owner = {user};")
    results = mycursor.fetchone()
    tookcoin = results[0]
    if tookcoin == 1:
        await ctx.respond("PettoBot: You have already collected your daily coins. Come back tomorrow!")
    else:
        coins = results[1]
        name = results[2]
        pers = results[3]
        coins = int(coins)
        coins += 5
        personality = pickPersonality(pers)
        
        mycursor.execute(f"update petbot set coins = {coins}, tookcoin = 1 where owner = {user};")
        con.commit()
        
        await ctx.respond(f"{name}: {personality.coins}\n\n+5 coins")
    
    
# battle
@bot.slash_command(description = "Challenges another user to a pet battle")
async def battle(ctx, *, user):
    owner = ctx.author.id
    opponent = str(user)
    opponent = opponent.replace("<@", "")
    opponent = opponent.replace('>', '')
    if (not hasAdopted(str(owner))):
        await ctx.respond("PettoBot: You do not have a pet!")
        return
    
    if (not hasAdopted(opponent)):
        await ctx.respond("PettoBot: Your opponent does not have a pet!")
        return
    
    mycursor.execute(f"select battle_time, love_points, name from petbot where owner = {owner};")
    result = mycursor.fetchone()
    currenttime = time.time()
    if (currenttime - float(result[0]) < float(actions[3].time_limit) * 60):
        await ctx.respond(f"PettoBot: You have already gone on a battle. Wait {actions[3].time_limit} minutes to battle again.")
        return
    if (int(result[1]) < int(actions[3].required_love)):
        await ctx.respond(f"PettoBot: {result[2]} does not have enough love points for battle.")
        return
    
    mycursor.execute(f"select battle_time, love_points, name from petbot where owner = {opponent};")
    result = mycursor.fetchone()
    currenttime = time.time()
    if (currenttime - float(result[0]) < float(actions[3].time_limit) * 60):
        await ctx.respond(f"PettoBot: Your opponent has already gone on a battle. Wait {actions[3].time_limit} minutes to battle again.")
        return
    if (int(result[1]) < int(actions[3].required_love)):
        await ctx.respond(f"PettoBot: Opponent's pet {result[2]} does not have enough love points for battle.")
        return
    
    async def first_button_callback(interaction):
        buttonDecline.disabled = True
        buttonAccept.disabled = True
        view1 = View()
        view1.add_item(buttonAccept)
        view1.add_item(buttonDecline)
        await interaction.response.edit_message(view = view1)
        await battle_accepted(ctx, owner, opponent)
    
    async def second_button_callback(interaction):
        buttonDecline.disabled = True
        buttonAccept.disabled = True
        view2 = View()
        view2.add_item(buttonAccept)
        view2.add_item(buttonDecline)
        await interaction.response.edit_message(view = view2)
        await ctx.respond("PettoBot: The user declined your challenge!")
    
    buttonAccept = Button(label = "Accept", row = 0, style = discord.ButtonStyle.green)
    buttonDecline = Button(label = "Decline", row = 0, style = discord.ButtonStyle.red)
    
    buttonAccept.callback = first_button_callback
    buttonDecline.callback = second_button_callback
    
    view = View()
    view.add_item(buttonAccept)
    view.add_item(buttonDecline)
    
    await ctx.respond(f"PettoBot: {user}, {ctx.author.mention} challenges you to a pet battle! Press the button if you accept\n", view = view)


async def battle_accepted(ctx, challenger, opponent):
    await ctx.respond("PettoBot: Battle starts!")
    mycursor.execute(f"select name, personality, coins, strength_points, picture, battle_wins, battle_losses, battle_time from petbot where owner = {challenger};")
    resultsChallenger = mycursor.fetchone()
    mycursor.execute(f"select name, personality, coins, strength_points, picture, battle_wins, battle_losses, battle_time from petbot where owner = {opponent};")
    resultsOpponent = mycursor.fetchone()
    
    personalityChal = pickPersonality(resultsChallenger[1])
    personalityOpp = pickPersonality(resultsOpponent[1])
    
    strengthChal = int(resultsChallenger[3])
    strengthOpp = int(resultsOpponent[3])
    
    if strengthChal <= strengthOpp:
        await ctx.send(f"PettoBot: {resultsOpponent[0]} strikes {resultsChallenger[0]} with great force!")
        await ctx.send(resultsOpponent[4])
        
    if strengthChal >= strengthOpp:
        await ctx.send(f"PettoBot: {resultsChallenger[0]} strikes {resultsOpponent[0]} with great force!")
        await ctx.send(resultsChallenger[4])
    
    if strengthChal > strengthOpp:
        await ctx.send(f"PettoBot: {resultsOpponent[0]} takes the blow!")
        await ctx.send(resultsOpponent[4])
        winner = "challenger"
    elif strengthChal < strengthOpp:
        await ctx.send(f"PettoBot: {resultsChallenger[0]} takes the blow!")
        await ctx.send(resultsChallenger[4])
        winner = "opponent"
    
    if strengthChal == strengthOpp:
        await ctx.send("PettoBot: The battle ends with a tie! The coins remain in your pockets")
    else:
        if winner == "opponent":
            await ctx.send(f"{resultsOpponent[0]} wins the battle!")
            mycursor.execute(f"update petbot set coins = {int(resultsOpponent[2]) + int(resultsChallenger[2])}, battle_wins = {int(resultsOpponent[5]) + 1} where owner = {opponent};")
            con.commit()
            mycursor.execute(f"update petbot set coins = 0, battle_losses = {int(resultsChallenger[6]) + 1} where owner = {challenger};")
            con.commit()
            await ctx.send(f"{resultsOpponent[0]}: {personalityOpp.winning}")
            await ctx.send(f"{resultsChallenger[0]}: {personalityChal.losing}")
        elif winner == "challenger":
            await ctx.send(f"{resultsChallenger[0]} wins the battle!")
            mycursor.execute(f"update petbot set coins = {int(resultsOpponent[2]) + int(resultsChallenger[2])}, battle_wins = {int(resultsChallenger[5]) + 1} where owner = {challenger};")
            con.commit()
            mycursor.execute(f"update petbot set coins = 0, battle_losses = {int(resultsOpponent[6]) + 1} where owner = {opponent};")
            con.commit()
            await ctx.send(f"{resultsChallenger[0]}: {personalityChal.winning}")
            await ctx.send(f"{resultsOpponent[0]}: {personalityOpp.losing}")

    mycursor.execute(f"update petbot set battle_time = {time.time()} where owner = {challenger};")
    con.commit()
    mycursor.execute(f"update petbot set battle_time = {time.time()} where owner = {opponent};")
    con.commit()
    

# train
@bot.slash_command(description = "Increases pet's strength")
async def train(ctx):
    user = ctx.author.id
    if (not hasAdopted(str(user))):
        await ctx.respond("PettoBot: You do not have a pet!")
        return
    
    mycursor.execute(f"select strength_points, name, training_time, picture, personality from petbot where owner = {user};")
    results = mycursor.fetchone()
    training_time = results[2]
    name = results[1]
    training_time = float(training_time)
    currenttime = time.time()
    if (currenttime - training_time < float(actions[2].time_limit) * 60):
        await ctx.respond(f"PettoBot: You have already trained {name}. Wait {actions[2].time_limit} minutes to train again.")
    else:
        strength = results[0]
        pers = results[4]
        picture = results[3]
        personality = pickPersonality(pers)
        
        strength = int(strength)
        strength += int(actions[2].strength)
        mycursor.execute(f"update petbot set strength_points = {strength}, training_time = {currenttime} where owner = {user};")
        con.commit()
        
        await ctx.respond(f"{name}: {personality.train}")
        await ctx.send(picture)
        await ctx.send("\n++strength")
   
  
# helper methods  

def pickPersonality(pers):
    if (pers == "Energetic"):
        personality = energetic
    elif (pers == "Gloomy"):
        personality = gloomy
    elif (pers == "Aggressive"):
        personality = aggressive
    return personality

def hasAdopted(user):
    mycursor.execute("select owner from petbot;")
    results = mycursor.fetchall()
    for result in results:
        if str(result[0]) == user:
            return True
    return False
   
######################################


# RUN

bot.run(token)

