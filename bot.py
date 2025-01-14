import discord
from discord.ext import commands, tasks
from dotenv import dotenv_values
from main import search_exalted


config = dotenv_values(".env")
TOKEN = config["DISCORD_TOKEN"]
PREFIX = "-"

bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
  print(f'{bot.user} has connected to Discord!')
  await bot.change_presence(activity=discord.Game(name="Path of Exile 2"))

@bot.command(name='price', help='Get the current price of exalted orbs')
async def price(ctx):
    data = search_exalted()
    for item in data:
        await ctx.send(f"{item['currency_name']}: {item['price_value']} Exalted -> {item['exchange_price_value']} {item['currency_name']}")
bot.run(TOKEN)