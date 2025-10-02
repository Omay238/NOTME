import discord

intents = discord.Intents.all()

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.slash_command(description="Says hello.")
async def hello(ctx):
    await ctx.respond("Hello!")

from cogs import money
bot.add_cog(money.Money(bot))

from dotenv import load_dotenv
import os
load_dotenv()

bot.run(os.environ["TOKEN"])
