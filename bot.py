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

bot = commands.Bot(command_prefix=PREFIX, help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name="Path of Exile 2 | -help"))
    #send_price_updates.start()
    

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
  
  
async def get_price(ctx, type):
  await ctx.send("Fetching prices...")
  data = search_prices(type)
  message = ""
  for item in data:
      part = f"<:{item['formatted_currency_name']}:{item['emoji_id']}> **{item['currency_name']}**: <:ExaltedOrb:1328816616854523924> **`{item['price_value']}`** -> <:{item['formatted_currency_name']}:{item['emoji_id']}> **`{item['exchange_price_value']}`**\n"
      
      if item['emoji_id'] is None:
        part = f"**{item['currency_name']}**: <:ExaltedOrb:1328816616854523924> **`{item['price_value']}`** -> **`{item['exchange_price_value']}`**\n"
        
      
      if len(message) + len(part) > 2000:
          await ctx.send(message)
          message = part
      else:
          message += part

  if message:
      await ctx.send(message)
  await ctx.send(f"Last update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
  
@bot.command(name='price', aliases=['p'], help="Get the latest prices of currency")
async def price_currency(ctx, type="currency"):
  await get_price(ctx, type)
  
@bot.command(name='waystones', aliases=['w'], help="Get the latest prices of waystones")
async def price_waystones(ctx, type="waystones"):
  await get_price(ctx, type)

@bot.command(name='runes', aliases=['r'], help="Get the latest prices of runes")
async def price_runes(ctx, type="runes"):
  await get_price(ctx, type)

@bot.command(name='essences', aliases=['e'], help="Get the latest prices of essences")
async def price_essences(ctx, type="essences"):
  await get_price(ctx, type)

@bot.command(name='gems', aliases=['g'], help="Get the latest prices of gems")
async def price_gems(ctx, type="gems"):
  await get_price(ctx, type)

@bot.command(name='uniques', aliases=['u'], help="Get the latest prices of uniques")
async def price_uniques(ctx, type="uniques"):
  await get_price(ctx, type)

@bot.command(name='fragments', aliases=['f'], help="Get the latest prices of fragments")
async def price_fragments(ctx, type="fragments"):
  await get_price(ctx, type)
  
@bot.command(name='soulcores', aliases=['s'], help="Get the latest prices of soul cores")
async def price_soulcores(ctx, type="soulcores"):
  await get_price(ctx, type)
  
@bot.command(name='breachcatalysts', aliases=['b'], help="Get the latest prices of breach catalysts")
async def price_breachcatalysts(ctx, type="breachcatalysts"):
  await get_price(ctx, type)

@bot.command(name='expedition', aliases=['ex'], help="Get the latest prices of expedition")
async def price_expedition(ctx, type="expedition"):
  await get_price(ctx, type)

@bot.command(name='ritualomens', aliases=['ro'], help="Get the latest prices of ritual omens")
async def price_ritualomens(ctx, type="ritualomens"):
  await get_price(ctx, type)
  
@bot.command(name='deliriumdistillations', aliases=['dd'], help="Get the latest prices of delirium distillations")
async def price_deliriumdistillations(ctx, type="deliriumdistillations"):
  await get_price(ctx, type)
  
@bot.command(name='help', alias=['h'], help="List all available commands")
async def help(ctx):
  message = """
  **`-price`** or **`-p`** - Get the latest prices of currency
  **`-waystones`** or **`-w`** - Get the latest prices of waystones
  **`-runes`** or **`-r`** - Get the latest prices of runes
  **`-essences`** or **`-e`** - Get the latest prices of essences
  **`-gems`** or **`-g`** - Get the latest prices of gems
  **`-uniques`** or **`-u`** - Get the latest prices of uniques
  **`-fragments`** or **`-f`** - Get the latest prices of fragments
  **`-soulcores`** or **`-s`** - Get the latest prices of soul cores
  **`-breachcatalysts`** or **`-b`** - Get the latest prices of breach catalysts
  **`-expedition`** or **`-ex`** - Get the latest prices of expedition
  **`-ritualomens`** or **`-ro`** - Get the latest prices of ritual omens
  **`-deliriumdistillations`** or **`-dd`** - Get the latest prices of delirium distillations
  **`-start`** - Start tracking prices every 3 hours
  **`-stop`** - Stop tracking prices
  """
  await ctx.send(message)  
  
  
@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send("❌ Invalid command. Please use **`-help`** for a list of available commands.")

bot.run(TOKEN)