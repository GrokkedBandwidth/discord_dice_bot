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
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Redefine help command for clarity of each of the following commands
@bot.command(name='help')
async def help(ctx):
    await ctx.send('List of Commands with Examples:\n'
                   '!roll <# of dice> <# of sides\n'
                   '!rollmod <# of sides> <# of modifier>\n'
                   '!d3 <# of dice> <# of Modifier>\n'
                   '!d4 <# of dice> <# of Modifier>\n'
                   '!d6 <# of dice> <# of Modifier>\n'
                   '!d8 <# of dice> <# of Modifier>\n'
                   '!d10 <# of dice> <# of Modifier>\n'
                   '!d12 <# of dice> <# of Modifier>\n'
                   '!d20 <# of dice> <# of Modifier>\n'
                   '!d20 optional: adv or dis'
                   '!d100 <# of dice> <# of Modifier>\n')
# Deprecated
@bot.command(name='roll',
             help="ex: !roll 1 20 (This rolls 1 d20)\n"
                  "ex: !roll 4 6 3 (This rolls 4d6 with a +7 modifier)")
async def roll(ctx,
               number_of_dice: int = commands.parameter(description="Number of dice you want to roll"),
               number_of_sides: int = commands.parameter(description="Number of sides of the dice being rolled: i.e. 20 = d20"), *args):
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

# Deprecated
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

# Function to be called for generated number of dice and the number of their sides from the !d# commands
def generate_dice(num_side, num_dice):
    dice = []
    for num in range(num_dice):
        dice.append(random.choice(range(1, num_side + 1)))
    return dice

# Function called after dice are generated to add dice together if there is more than one and to add any player
# given modifiers
def dice_math(num_side, *args):
    num_of_dice = 1
    modifier = 0
    if args:
        try:
            num_of_dice = int(args[0])
            try:
                modifier = int(args[1])
            except IndexError or ValueError:
                pass
        except IndexError or ValueError:
            pass
    dice = generate_dice(num_side, num_of_dice)
    total = sum(dice)
    mod_total = total + modifier
    return dice, total, mod_total, modifier

# Following commands are dice commands that specifically correspond to the most common dice used in TTRPGs
# Each command, if executed with no args, will roll a single dice of its side d# without a modifier
@bot.command(name='d3',
             help="!d3 (Rolls 1 d3)\n!d3 2 (Rolls 2 d3)\n!d3 3 5 (Rolls 3 d3 with +5 mod)")
async def d3(ctx, *args):
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

@bot.command(name='d4',
             help="!d4 (Rolls 1 d4)\n!d3 2 (Rolls 2 d4)\n!d4 3 5 (Rolls 3 d4 with +5 mod)")
async def d4(ctx, *args):
    result = dice_math(4, *args)
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
             help="!d6 (Rolls 1 d6)\n!d6 2 (Rolls 2 d6)\n!d6 6 5 (Rolls 6 d6 with +5 mod)")
async def d6(ctx, *args):
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
             help="!d8 (Rolls 1 d8)\n!d8 2 (Rolls 2 d8)\n!d8 8 5 (Rolls 8 d8 with +5 mod)")
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
             help="!d10 (Rolls 1 d10)\n!d10 2 (Rolls 2 d10)\n!d10 10 5 (Rolls 10 d10 with +5 mod)")
async def d10(ctx, *args):
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
             help="!d12 (Rolls 1 d12)\n!d12 2 (Rolls 2 d12)\n!d12 12 5 (Rolls 12 d12 with +5 mod)")
async def d12(ctx, *args):
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
             help="!d20 (Rolls 1 d20)\n!d20 2 (Rolls 2 d20)\n!d20 20 5 (Rolls 20 d20 with +5 mod)"
                  "\n!d20 adv 5 (Rolls 1 d20 with advantage and +5 modifier")
async def d20(ctx, *args):
    adv = False
    dis = False
    if "adv" in args or "dis" in args:
        if "adv" in args:
            adv = True
        elif "dis" in args:
            dis = True
        args = [item for item in args if "adv" != item and "dis" != item]
        if len(args) == 1:
            args.append(args[0])
            args[0] = 1

    if adv and dis:
        adv = False
        dis = False
    result = dice_math(20, *args)
    dice = result[0]
    total = result[1]
    mod_total = result[2]
    modifier = result[3]
    sign = '+'
    if modifier < 0:
        sign = ''
    if adv:
        result2 = dice_math(20, *args)
        dice2 = result2[0]
        if dice2 > dice:
            mod_total = result2[2]
            modifier = result2[3]
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}, {dice2} with advantage\nTotal: '
                       f'{mod_total} with {sign}{modifier} modifier')

    elif dis:
        result2 = dice_math(20, *args)
        dice2 = result2[0]
        if dice2 < dice:
            mod_total = result2[2]
            modifier = result2[3]
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}, {dice2} with disadvantage\nTotal: '
                       f'{mod_total} with {sign}{modifier} modifier')

    elif dice[0] == total and total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
    elif total == mod_total:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
    else:
        await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')

@bot.command(name='d100',
             help="!d100 (Rolls 1 d100)\n!d100 2 (Rolls 2 d100)\n!d100 100 5 (Rolls 100 d100 with +5 mod)",)
async def d100(ctx, *args):
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

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f'{error}. Type !help for list of commands')

bot.run(TOKEN)

