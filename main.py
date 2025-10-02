import discord

intents = discord.Intents.all()

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.slash_command(description="Says hello.")
async def hello(ctx):
    await ctx.respond("Hello!")

@bot.slash_command(description="Ping pong!")
async def ping(ctx):
    await ctx.respond('Pong! {0}'.format(round(bot.latency, 1)))

from cogs import money
bot.add_cog(money.Money(bot))

from dotenv import load_dotenv
import os
load_dotenv()

bot.run(os.environ["TOKEN"])
