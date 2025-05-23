import discord
from discord.ui import Button, View
import Command_executor

exec = Command_executor.Command_executor()

bot = discord.Bot()

def __init__(command_logic, token, init):
    global cmd
    cmd = command_logic
    global initial
    initial = init
    bot.run(token)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.slash_command(description = "Adopts a new pet")
async def adopt(ctx, *, gender):
    user = str(ctx.author.id)
    #myfunctioncall = lambda: cmd.adopt(user, gender)
    #exec.execute(myfunctioncall, cmd.adopt.__name__)
    await ctx.respond(exec.execute(cmd.adopt, user, gender))
    #await ctx.respond(cmd.adopt(user, gender))


@bot.slash_command(description = "Changes the name of the pet")
async def change_name(ctx, *, name):
    user = str(ctx.author.id)
    #await ctx.respond(cmd.change_name(user, name))
    await ctx.respond(exec.execute(cmd.change_name, user, name))


@bot.slash_command(description = "Shows pet's profile")
async def profile(ctx):
    user = str(ctx.author.id)
    results = exec.execute(cmd.profile, user)
    #results = cmd.profile(user)
    user = ctx.author.name

    embed=discord.Embed(title= results[0] + "'s profile", url = None)
    embed.set_image(url = results[2])
    embed.add_field(name = "Owner: " + user, value = "", inline = True)
    embed.add_field(name = "Gender: " + results[3], value = "", inline = True)
    embed.add_field(name = "", value = "", inline = False)
    embed.add_field(name = "Personality: " + results[8], value = "", inline = True)
    embed.add_field(name = "Adoption date: " + results[4][:10], value = "", inline = True)
    embed.add_field(name = "", value = "", inline = False)
    embed.add_field(name = "Coins: " + str(results[9]), value = "", inline = True)
    embed.add_field(name = "Love points: " + str(results[5]), value = "", inline = True)
    embed.add_field(name = "", value = "", inline = False)
    embed.add_field(name = "Battle wins: " + str(results[6]), value = "", inline = True)
    embed.add_field(name = "Battle losses: " + str(results[7]), value = "", inline = True)
    
    personality = exec.execute(cmd.pickPersonality, results[8])
    #personality = cmd.pickPersonality(results[8])
    
    await ctx.respond(f"{results[0]}: {personality.profile}")
    await ctx.send(embed=embed)


@bot.slash_command(description = "Shows love to your pet")
async def pet(ctx):
    user = str(ctx.author.id)
    action = initial.get_actions()[0]
    response = exec.execute(cmd.action_valid, user, action)
    #response = cmd.action_valid(user, action)
    
    if response != None:
        await ctx.respond(response)
    else:
        name, sentence, picture, points = exec.execute(cmd.show_love, user, action)
        #name, sentence, picture, points = cmd.show_love(user, action)
        await ctx.respond(f"{name}: {sentence}")
        await ctx.send(picture)
        await ctx.send(f"\n+{points} love points")


@bot.slash_command(description = "Shows love to your pet")
async def walk(ctx):
    user = str(ctx.author.id)
    action = initial.get_actions()[1]
    response = exec.execute(cmd.action_valid, user, action)
    #response = cmd.action_valid(user, action)
    if response != None:
        await ctx.respond(response)
    else:
        name, sentence, picture, points = exec.execute(cmd.show_love, user, action)
        #name, sentence, picture, points = cmd.show_love(user, action)
        await ctx.respond(f"{name}: {sentence}")
        await ctx.send(picture)
        await ctx.send(f"\n+{points} love points")


@bot.slash_command(description = "Increases pet's strength")
async def train(ctx):
    user = str(ctx.author.id)
    action = initial.get_actions()[2]
    response = exec.execute(cmd.action_valid, user, action)
    #response = cmd.action_valid(user, action)
    if response != None:
        await ctx.respond(response)
    else:
        name, sentence, picture = exec.execute(cmd.train, user, action)
        #name, sentence, picture = cmd.train(user, action)
        await ctx.respond(f"{name}: {sentence}")
        await ctx.send(picture)
        await ctx.send("\n++strength")
        


@bot.slash_command(description = "Challenges another user to a pet battle")
async def battle(ctx, *, user):
    challenger = str(ctx.author.id)
    opponent = str(user)
    opponent = opponent.replace("<@", "")
    opponent = opponent.replace('>', '')
    
    action = initial.get_actions()[3]
    response = exec.execute(cmd.action_valid, challenger, action)
    #response = cmd.action_valid(challenger, action)
    if response != None:
        await ctx.respond(response)
        return
    response = exec.execute(cmd.action_valid, opponent, action)
    #response = cmd.action_valid(opponent, action)
    if response != None:
        await ctx.respond(response)
        return
    
    async def first_button_callback(interaction):
        buttonDecline.disabled = True
        buttonAccept.disabled = True
        view1 = View()
        view1.add_item(buttonAccept)
        view1.add_item(buttonDecline)
        await interaction.response.edit_message(view = view1)
        await battle_accepted(ctx, challenger, opponent)
    
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
    winner, loser = exec.execute(cmd.battle, challenger, opponent)
    #winner, loser = cmd.battle(challenger, opponent)
    if winner == None and loser == None:
        await ctx.respond("PettoBot: The battle ends with a tie! The coins remain in your pockets")
        return
    else:
        await ctx.send(f"PettoBot: {winner.petname} strikes {loser.petname} with great force!")
        await ctx.send(winner.picture)
        await ctx.send(f"PettoBot: {loser.petname} takes the blow!")
        await ctx.send(loser.picture)
        await ctx.send(f"{winner.petname}: {winner.personality.winning}")
        await ctx.send(f"{loser.petname}: {loser.personality.losing}")
        return
