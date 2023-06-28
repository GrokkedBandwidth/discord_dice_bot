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

@bot.command(name='roll',
             help="ex: !roll 1 20 (This rolls 1 d20)\n"
                  "ex: !roll 4 6 3 (This rolls 4 d6 with a +7 modifier)")
async def roll(ctx,
               number_of_dice: int = commands.parameter(description="Number of dice you want to roll"),
               number_of_sides: int = commands.parameter(description="Number of sides of the dice being rolled: i.e. 20 = d20",), *args):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    sum_dice = 0
    for die in dice:
        sum_dice += int(die)
    dice = ', '.join(dice)
    modifier = 0
    if args:
        modifier += int(args[0])

    await ctx.send(f'{ctx.author.name} rolled {dice}\n'
                   f'Dice Total: {sum_dice}\n'
                   f'Modified Total: {sum_dice + modifier}')

@bot.command(name='rollmod',
             help="ex: !rollmod 20 3 (This rolls 1 d20 with +3 modifier)")
async def rollmod(ctx,
                  number_of_sides: int = commands.parameter(description="Number of sides of the dice being rolled"),
                  mod: int = commands.parameter(description="Modifier number for the dice being rolled")):
    if mod < 0:
        mod_symbol = ""
    else:
        mod_symbol = "+"
    unmod_dice = str(random.choice(range(1, number_of_sides + 1)))
    mod_dice = int(unmod_dice) + mod
    await ctx.send(f'{ctx.author.name} rolled a {mod_dice}\n {unmod_dice} with {mod_symbol}{mod} modifier')

bot.run(TOKEN)
