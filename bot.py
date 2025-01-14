import discord
from discord.ext import commands, tasks
from dotenv import dotenv_values
from main import search_exalted
import time
from datetime import datetime

config = dotenv_values(".env")
TOKEN = config["DISCORD_TOKEN"]
PREFIX = "-"
CHANNEL_ID = config["DISCORD_CHANNEL_ID"]

bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Path of Exile 2"))
    

@tasks.loop(minutes=60)
async def send_price_updates():
    channel = bot.get_channel(int(CHANNEL_ID))
    if channel is None:
        print("Channel not found")
        return

    data = search_exalted()
    message = ""
    for item in data:
        part = f"<:{item['formatted_currency_name']}:{item['emoji_id']}> **{item['currency_name']}**: <:ExaltedOrb:1328816616854523924> **`{item['price_value']}`** -> <:{item['formatted_currency_name']}:{item['emoji_id']}> **`{item['exchange_price_value']}`**\n"
        if len(message) + len(part) > 2000:
            await channel.send(message)
            message = part
        else:
            message += part

    if message:
        await channel.send(message)
    await channel.send(f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@bot.command(name='start')
async def start(ctx):
    send_price_updates.start()
    await ctx.send("Bot started tracking prices every 1 hour")

@bot.command(name='price')
async def price(ctx):
  await send_price_updates()

bot.run(TOKEN)