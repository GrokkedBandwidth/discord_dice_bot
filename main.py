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

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)

    print(
        f'{bot.user.name} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id}'
    )
@bot.command(name='roll_dice', help='Simulates rolling dice.')
async def roll(ctx,
               number_of_dice: int = commands.parameter(description=""),
               number_of_sides: int = commands.parameter(description="")):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice))


bot.run(TOKEN)
