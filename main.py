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
                  "ex: !roll 4 6 3 (This rolls 4d6 with a +7 modifier)")
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

    await ctx.send(f'{ctx.author.display_name} rolled {dice}\n'
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
    await ctx.send(f'{ctx.author.display_name} rolled a {mod_dice}\n {unmod_dice} with {mod_symbol}{mod} modifier')

def generate_dice(num_side, num_dice):
    dice = []
    for num in range(num_dice):
        dice.append(random.choice(range(1, num_side + 1)))
    return dice

def dice_math(num_side, *args):
    num_of_dice = 1
    modifier = 0
    if args:
        try:
            num_of_dice = int(args[0])
            try:
                modifier = int(args[1])
            except IndexError:
                pass
        except IndexError:
            pass
    dice = generate_dice(num_side, num_of_dice)
    total = sum(dice)
    mod_total = total + modifier
    return dice, total, mod_total, modifier

@bot.command(name='d3',
             help="!d3 (Rolls 1 d3)\n!d3 2 (Rolls 2 d3)\n!d3 3 5 (Rolls 3 d3 with +5 mod)")
async def d8(ctx, *args):
    result = dice_math(3, *args)
    dice = result[0]
    total = result[1]
    mod_total = result[2]
    modifier = result[3]
    sign = '+'
    if modifier < 0:
        sign = ''
    if dice[0] == total and total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
    elif total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
    else:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')

@bot.command(name='d6',
             help="!d6")
async def d8(ctx, *args):
    result = dice_math(6, *args)
    dice = result[0]
    total = result[1]
    mod_total = result[2]
    modifier = result[3]
    sign = '+'
    if modifier < 0:
        sign = ''
    if dice[0] == total and total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
    elif total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
    else:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')

@bot.command(name='d8',
             help="!d8")
async def d8(ctx, *args):
    result = dice_math(8, *args)
    dice = result[0]
    total = result[1]
    mod_total = result[2]
    modifier = result[3]
    sign = '+'
    if modifier < 0:
        sign = ''
    if dice[0] == total and total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
    elif total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
    else:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')

@bot.command(name='d10',
             help="!d10")
async def d8(ctx, *args):
    result = dice_math(10, *args)
    dice = result[0]
    total = result[1]
    mod_total = result[2]
    modifier = result[3]
    sign = '+'
    if modifier < 0:
        sign = ''
    if dice[0] == total and total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
    elif total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
    else:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')

@bot.command(name='d12',
             help="!d12")
async def d8(ctx, *args):
    result = dice_math(12, *args)
    dice = result[0]
    total = result[1]
    mod_total = result[2]
    modifier = result[3]
    sign = '+'
    if modifier < 0:
        sign = ''
    if dice[0] == total and total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
    elif total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
    else:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')

@bot.command(name='d20',
             help="!d20")
async def d8(ctx, *args):
    result = dice_math(20, *args)
    dice = result[0]
    total = result[1]
    mod_total = result[2]
    modifier = result[3]
    sign = '+'
    if modifier < 0:
        sign = ''
    if dice[0] == total and total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
    elif total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
    else:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')

@bot.command(name='d100',
             help="!d100")
async def d8(ctx, *args):
    result = dice_math(100, *args)
    dice = result[0]
    total = result[1]
    mod_total = result[2]
    modifier = result[3]
    sign = '+'
    if modifier < 0:
        sign = ''
    if dice[0] == total and total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
    elif total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
    else:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')














bot.run(TOKEN)
