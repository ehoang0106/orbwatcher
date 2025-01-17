import discord
from discord.ext import commands, tasks
from dotenv import dotenv_values
from main import search_prices
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
    send_price_updates.start()
    

@tasks.loop(hours=3)
async def send_price_updates():
  
  channel = bot.get_channel(int(CHANNEL_ID))
  if channel is None:
      print("Channel not found")
      return
  await channel.send("Fetching prices...")
  type = "currency"
  data = search_prices(type)
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

@bot.command(name='start', help="Start tracking prices every 1 hour")
async def start(ctx):
  await ctx.send("Bot started tracking prices every 1 hour")
  send_price_updates.start()
@bot.command(name='stop', help="Stop tracking prices")
async def stop(ctx):
  await ctx.send("Bot stopped tracking prices")
  send_price_updates.stop()

@bot.command(name='price', aliases=['p'], help="Get the latest prices of currency")
async def price(ctx):
  await ctx.send("Fetching prices...")
  type = "currency"
  data = search_prices(type)
  message = ""
  for item in data:
      part = f"<:{item['formatted_currency_name']}:{item['emoji_id']}> **{item['currency_name']}**: <:ExaltedOrb:1328816616854523924> **`{item['price_value']}`** -> <:{item['formatted_currency_name']}:{item['emoji_id']}> **`{item['exchange_price_value']}`**\n"
      if len(message) + len(part) > 2000:
          await ctx.send(message)
          message = part
      else:
          message += part

  if message:
      await ctx.send(message)
  await ctx.send(f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


@bot.command(name='waystones', aliases=['w'], help="Get the latest prices of waystones")
async def price(ctx):
  await ctx.send("Fetching prices...")
  type = "waystones"
  data = search_prices(type)
  message = ""
  for item in data:
      part = f"<:{item['formatted_currency_name']}:{item['emoji_id']}> **{item['currency_name']}**: <:ExaltedOrb:1328816616854523924> **`{item['price_value']}`** -> <:{item['formatted_currency_name']}:{item['emoji_id']}> **`{item['exchange_price_value']}`**\n"
      if len(message) + len(part) > 2000:
          await ctx.send(message)
          message = part
      else:
          message += part

  if message:
      await ctx.send(message)
  await ctx.send(f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Invalid command. Please use **`-help`** for a list of available commands.")

bot.run(TOKEN)