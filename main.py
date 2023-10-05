import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import random

with open("insults.csv", mode="r") as file:
    insults = file.readlines()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot()

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")

#### Menu Test

class MyView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.side = 20
        self.number = 1
        self.mod = 0
        self.type = "Regular"

    @discord.ui.select(
        placeholder="Choose a die!",
        row=0,
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Dice: d20",
                description="Twenty sided die",
                default=True,
                value="d20"
            ),
            discord.SelectOption(
                label="Dice: d6",
                description="Six sided die",
                value="d6"
            ),
            discord.SelectOption(
                label="Dice: d8",
                description="Eight sided die",
                value="d8"
            ),
            discord.SelectOption(
                label="Dice: d10",
                description="Ten sided die",
                value="d10"
            ),
            discord.SelectOption(
                label="Dice: d12",
                description="Twelve sided die",
                value="d12"
            ),
            discord.SelectOption(
                label="Dice: d100",
                description="Hundred sided die",
                value="d100"
            ),
        ]
    )
    async def die_callback(self, select, interaction):
        self.side = int(select.values[0][1:])

    @discord.ui.select(
        placeholder="Choose number of dice",
        row=1,
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Number: 1", default=True, value="1"),
            discord.SelectOption(label="Number: 2", value="2"),
            discord.SelectOption(label="Number: 3", value="3"),
            discord.SelectOption(label="Number: 4", value="4"),
            discord.SelectOption(label="Number: 5", value="5"),
            discord.SelectOption(label="Number: 6", value="6"),
            discord.SelectOption(label="Number: 7", value="7"),
            discord.SelectOption(label="Number: 8", value="8"),
            discord.SelectOption(label="Number: 9", value="9"),
            discord.SelectOption(label="Number: 10", value="10"),
        ]
    )
    async def number_callback(self, select, interaction):
        self.number = int(select.values[0])

    @discord.ui.select(
        placeholder="Choose number of dice",
        row=2,
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Modifier: -5", value="-5"),
            discord.SelectOption(label="Modifier: -4", value="-4"),
            discord.SelectOption(label="Modifier: -3", value="-3"),
            discord.SelectOption(label="Modifier: -2", value="-2"),
            discord.SelectOption(label="Modifier: -1", value="-1"),
            discord.SelectOption(label="Modifier: +0", default=True, value="0"),
            discord.SelectOption(label="Modifier: +1", value="1"),
            discord.SelectOption(label="Modifier: +2", value="2"),
            discord.SelectOption(label="Modifier: +3", value="3"),
            discord.SelectOption(label="Modifier: +4", value="4"),
            discord.SelectOption(label="Modifier: +5", value="5"),
            discord.SelectOption(label="Modifier: +6", value="6"),
            discord.SelectOption(label="Modifier: +7", value="7"),
            discord.SelectOption(label="Modifier: +8", value="8"),
            discord.SelectOption(label="Modifier: +9", value="9"),
            discord.SelectOption(label="Modifier: +10", value="10"),
            discord.SelectOption(label="Modifier: +11", value="11"),
            discord.SelectOption(label="Modifier: +12", value="12"),
            discord.SelectOption(label="Modifier: +13", value="13"),
            discord.SelectOption(label="Modifier: +14", value="14"),
            discord.SelectOption(label="Modifier: +15", value="15"),
        ]
    )
    async def modifier_callback(self, select, interaction):
        self.mod = int(select.values[0])

    @discord.ui.select(
        placeholder="Choose number of dice",
        row=3,
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="Type: Regular", default=True, value="Regular"),
            discord.SelectOption(label="Type: Advantage", value="Advantage"),
            discord.SelectOption(label="Type: Disadvantage", value="Disadvantage"),
        ]
    )
    async def roll_type_callback(self, select, interaction):
        self.type = select.values[0]

    @discord.ui.button(label="Roll!", row=4, style=discord.ButtonStyle.primary)
    async def dice_roll_callback(self, button, interaction):
        dice = dice_math(num_side=self.side, num_of_dice=self.number, mod=self.mod, type=self.type)
        dice_list = dice[0]
        total = dice[1]
        mod_total = dice[2]
        mod = dice[3]
        symbol = "+"
        if mod < 0:
            symbol = ""
        if self.type != "Regular":
            if self.mod == 0:
                await interaction.response.send_message(
                    f"{interaction.user.name} rolled {dice_list} on a d{self.side} with {self.type}\nTotal: {total}"
                )
            else:
                await interaction.response.send_message(
                    f"{interaction.user.name} rolled {dice_list} on a d{self.number} with {self.type}\nTotal: {mod_total}\n{total} with {symbol}{mod}")
        elif mod == 0:
            await interaction.response.send_message(
                f"{interaction.user.name} rolled {dice_list} on a d{self.number}\nTotal: {total}")

        else:
            await interaction.response.send_message(
                f"{interaction.user.name} rolled {dice_list} on a d{self.number}\nTotal: {mod_total}\n{total} with {symbol}{mod}")

@bot.command()
async def dice(ctx):
    await ctx.send("Choose your dice", view=MyView())

def generate_dice(num_side, num_dice):
    dice = []
    for num in range(num_dice):
        dice.append(random.choice(range(1, num_side + 1)))
    return dice

def dice_math(num_side, num_of_dice, mod, type):
    if type == "Advantage" or type == "Disadvantage":
        die1 = generate_dice(num_side, 1)[0]
        die2 = generate_dice(num_side, 1)[0]
        if type == "Advantage":
            dice = [die1, die2]
            total = max(die1, die2)
            mod_total = total + mod
        else:
            dice = [die1, die2]
            total = min(die1, die2)
            mod_total = total + mod
        return dice, total, mod_total, mod
    else:
        dice = generate_dice(num_side, num_of_dice)
        total = sum(dice)
        mod_total = total + mod
        return dice, total, mod_total, mod

# Following commands are dice commands that specifically correspond to the most common dice used in TTRPGs
# Each command, if executed with no args, will roll a single dice of its side d# without a modifier
# @bot.command(name='d3',
#              help="!d3 (Rolls 1 d3)\n!d3 2 (Rolls 2 d3)\n!d3 3 5 (Rolls 3 d3 with +5 mod)")
# async def d3(ctx, *args):
#     result = dice_math(3, *args)
#     dice = result[0]
#     total = result[1]
#     mod_total = result[2]
#     modifier = result[3]
#     sign = '+'
#     if modifier < 0:
#         sign = ''
#     if dice[0] == total and total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
#     elif total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
#     else:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')
#
# @bot.command(name='d4',
#              help="!d4 (Rolls 1 d4)\n!d3 2 (Rolls 2 d4)\n!d4 3 5 (Rolls 3 d4 with +5 mod)")
# async def d4(ctx, *args):
#     result = dice_math(4, *args)
#     dice = result[0]
#     total = result[1]
#     mod_total = result[2]
#     modifier = result[3]
#     sign = '+'
#     if modifier < 0:
#         sign = ''
#     if dice[0] == total and total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
#     elif total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
#     else:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')
#
# @bot.command(name='d6',
#              help="!d6 (Rolls 1 d6)\n!d6 2 (Rolls 2 d6)\n!d6 6 5 (Rolls 6 d6 with +5 mod)")
# async def d6(ctx, *args):
#     result = dice_math(6, *args)
#     dice = result[0]
#     total = result[1]
#     mod_total = result[2]
#     modifier = result[3]
#     sign = '+'
#     if modifier < 0:
#         sign = ''
#     if dice[0] == total and total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
#     elif total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
#     else:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')
#
# @bot.command(name='d8',
#              help="!d8 (Rolls 1 d8)\n!d8 2 (Rolls 2 d8)\n!d8 8 5 (Rolls 8 d8 with +5 mod)")
# async def d8(ctx, *args):
#     result = dice_math(8, *args)
#     dice = result[0]
#     total = result[1]
#     mod_total = result[2]
#     modifier = result[3]
#     sign = '+'
#     if modifier < 0:
#         sign = ''
#     if dice[0] == total and total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
#     elif total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
#     else:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')
#
# @bot.command(name='d10',
#              help="!d10 (Rolls 1 d10)\n!d10 2 (Rolls 2 d10)\n!d10 10 5 (Rolls 10 d10 with +5 mod)")
# async def d10(ctx, *args):
#     result = dice_math(10, *args)
#     dice = result[0]
#     total = result[1]
#     mod_total = result[2]
#     modifier = result[3]
#     sign = '+'
#     if modifier < 0:
#         sign = ''
#     if dice[0] == total and total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
#     elif total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
#     else:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')
#
# @bot.command(name='d12',
#              help="!d12 (Rolls 1 d12)\n!d12 2 (Rolls 2 d12)\n!d12 12 5 (Rolls 12 d12 with +5 mod)")
# async def d12(ctx, *args):
#     result = dice_math(12, *args)
#     dice = result[0]
#     total = result[1]
#     mod_total = result[2]
#     modifier = result[3]
#     sign = '+'
#     if modifier < 0:
#         sign = ''
#     if dice[0] == total and total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
#     elif total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
#     else:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')
#
# @bot.command(name='d20',
#              help="!d20 (Rolls 1 d20)\n!d20 2 (Rolls 2 d20)\n!d20 20 5 (Rolls 20 d20 with +5 mod)"
#                   "\n!d20 adv 5 (Rolls 1 d20 with advantage and +5 modifier")
# async def d20(ctx, *args):
#     adv = False
#     dis = False
#     if "adv" in args or "dis" in args:
#
#         if "adv" in args:
#             adv = True
#         elif "dis" in args:
#             dis = True
#         args = [item for item in args if "adv" != item and "dis" != item]
#
#     if adv and dis:
#         adv = False
#         dis = False
#     result = dice_math(20, *args)
#     dice = result[0]
#     total = result[1]
#     mod_total = result[2]
#     modifier = result[3]
#     sign = '+'
#     if modifier < 0:
#         sign = ''
#     if adv:
#         result2 = dice_math(20, *args)
#         dice2 = result2[0]
#         if dice2 > dice:
#             mod_total = result2[2]
#             modifier = result2[3]
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}, {dice2} with advantage\nTotal: '
#                        f'{mod_total} with {sign}{modifier} modifier')
#     elif dis:
#         result2 = dice_math(20, *args)
#         dice2 = result2[0]
#         if dice2 < dice:
#             mod_total = result2[2]
#             modifier = result2[3]
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}, {dice2} with disadvantage\nTotal: '
#                        f'{mod_total} with {sign}{modifier} modifier')
#
#     elif dice[0] == total and total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
#     elif total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
#     else:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')
#
# @bot.command(name='d100',
#              help="!d100 (Rolls 1 d100)\n!d100 2 (Rolls 2 d100)\n!d100 100 5 (Rolls 100 d100 with +5 mod)",)
# async def d100(ctx, *args):
#     result = dice_math(100, *args)
#     dice = result[0]
#     total = result[1]
#     mod_total = result[2]
#     modifier = result[3]
#     sign = '+'
#     if modifier < 0:
#         sign = ''
#     if dice[0] == total and total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}')
#     elif total == mod_total:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {total}')
#     else:
#         await ctx.send(f'{ctx.author.display_name} rolled: {dice}\nTotal: {mod_total} with {sign}{modifier} modifier')
#
# @bot.command(name="insult")
# async def insult(ctx):
#     joke = random.choice(insults)
#     await ctx.send(f'{ctx.author.display_name} says: {joke}')

# @bot.event
# async def on_command_error(ctx, error):
#     if isinstance(error, commands.CommandNotFound):
#         await ctx.send(f'{error}. Type !help for list of commands')

bot.run(TOKEN)

