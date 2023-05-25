import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# @bot.event
# async def on_ready():
    # guild = discord.utils.get(bot.guilds, name=GUILD)
    # print(
    #     f'{bot.user.name} is connected to the following guild:\n'
    #     f'{guild.name}(id: {guild.id}'
    # )
@bot.command(name='roll',
             help="ex: !roll 1 20 (This rolls 1 d20)")
async def roll(ctx,
               number_of_dice: int = commands.parameter(description="Number of dice you want to roll"),
               number_of_sides: int = commands.parameter(description="Number of sides of the dice being rolled: i.e. 20 = d20")):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))

@bot.command(name='rollmod',
             help="ex: !rollmod 20 3 (This rolls 1 d20 with +3 modifier")
async def rollmod(ctx,
                  number_of_sides: int = commands.parameter(description="Number of sides of the dice being rolled"),
                  mod: int = commands.parameter(description="Modifier number for the dice being rolled")):
    if mod < 0:
        mod_symbol = ""
    else:
        mod_symbol = "+"
    unmod_dice = str(random.choice(range(1, number_of_sides + 1)))
    mod_dice = int(unmod_dice) + mod
    await ctx.send(f'Roll: {unmod_dice}\n {mod_dice} with {mod_symbol}{mod}')



bot.run(TOKEN)
