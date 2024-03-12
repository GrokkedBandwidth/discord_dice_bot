import os
import discord
from dotenv import load_dotenv
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

    def clear_dice(self):
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
                label="Dice: d4",
                description="Four sided die",
                value="d4"
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
            discord.SelectOption(label="Modifier: +0", default=True, value="0"),
            discord.SelectOption(label="Modifier: +1", value="1"),
            discord.SelectOption(label="Modifier: +2", value="2"),
            discord.SelectOption(label="Modifier: +3", value="3"),
            discord.SelectOption(label="Modifier: +4", value="4"),
            discord.SelectOption(label="Modifier: +5", value="5"),
            discord.SelectOption(label="Modifier: -5", value="-5"),
            discord.SelectOption(label="Modifier: -4", value="-4"),
            discord.SelectOption(label="Modifier: -3", value="-3"),
            discord.SelectOption(label="Modifier: -2", value="-2"),
            discord.SelectOption(label="Modifier: -1", value="-1"),
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
                    f"{interaction.user.nick} rolled {dice_list} on a d{self.side} with {self.type}\nTotal: {total}"
                )
            else:
                await interaction.response.send_message(
                    f"{interaction.user.nick} rolled {dice_list} on a d{self.side} with {self.type}\nTotal: {mod_total}\n{total} with {symbol}{mod}")
        elif mod == 0:
            await interaction.response.send_message(
                f"{interaction.user.nick} rolled {dice_list} on a d{self.side}\nTotal: {total}")

        else:
            await interaction.response.send_message(
                f"{interaction.user.nick} rolled {dice_list} on a d{self.side}\nTotal: {mod_total}\n{total} with {symbol}{mod}")
        self.clear_dice()


@bot.command()
async def dice(ctx):
    await ctx.send("Choose your dice", view=MyView())

@bot.command()
async def insult(ctx):
    insult = random.choice(insults)
    await ctx.send(f"{ctx.author.nick}: {insult}")

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

bot.run(TOKEN)

