import discord
import Command_logic as cmd

def __init__(Bot):
    global bot
    bot = Bot


@bot.slash_command(description = "Adopts a new pet")
async def adopt(ctx, *, gender):
    user = ctx.author.id
    await ctx.respond(cmd.adopt(user, gender))


@bot.slash_command(description = "Changes the name of the pet")
async def change_name(ctx, *, name):
    user = ctx.author.id
    await ctx.respond(cmd.change_name(user, name))


@bot.slash_command(description = "Shows pet's profile")
async def profile(ctx):
    user = ctx.author.id
    results = cmd.profile(user)
    
    embed=discord.Embed(title= results[0] + "'s profile", url = None)
    embed.set_image(url = results[2])
    embed.add_field(name = "Owner: " + user, value = "", inline = True)
    embed.add_field(name = "Gender: " + results[3], value = "", inline = True)
    embed.add_field(name = "", value = "", inline = False)
    embed.add_field(name = "Personality: " + results[8], value = "", inline = True)
    embed.add_field(name = "Adoption date: " + results[4][:10], value = "", inline = True)
    embed.add_field(name = "", value = "", inline = False)
    embed.add_field(name = "Coins: " + results[9], value = "", inline = True)
    embed.add_field(name = "Love points: " + results[5], value = "", inline = True)
    embed.add_field(name = "", value = "", inline = False)
    embed.add_field(name = "Battle wins: " + results[6], value = "", inline = True)
    embed.add_field(name = "Battle losses: " + results[7], value = "", inline = True)
    
    await ctx.respond(f"{results[0]}: {results[8].profile}")
    await ctx.send(embed=embed)


@bot.slash_command(description = "Shows love to your pet")
async def pet(ctx):
    user = ctx.author.id
    response = cmd.action(user, 0)
    if response != None:
        await ctx.respond(response)
    else:
        results = cmd.show_love(user, 0)
        await ctx.respond(f"{results[0]}: {results[1]}")
        await ctx.send(results[2])
        await ctx.send(f"\n+{results[3]} love points")


@bot.slash_command(description = "Shows love to your pet")
async def walk(ctx):
    user = ctx.author.id
    response = cmd.action(user, 1)
    if response != None:
        await ctx.respond(response)
    else:
        results = cmd.show_love(user, 1)
        await ctx.respond(f"{results[0]}: {results[1]}")
        await ctx.send(results[2])
        await ctx.send(f"\n+{results[3]} love points")