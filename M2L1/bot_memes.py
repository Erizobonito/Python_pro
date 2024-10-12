# This example requires the 'members' and 'message_content' privileged intents to function.

import discord
from discord.ext import commands
import random, os

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', description=description, intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')




@bot.command()
async def meme2(ctx):
    img_name = random.choice(os.listdir('./M2L1/images'))
    with open(f'./M2L1/images/{img_name}', 'rb') as f:
        # ¡Vamos a almacenar el archivo de la biblioteca Discord convertido en esta variable!
        picture = discord.File(f)
    # A continuación, podemos enviar este archivo como parámetro.
    await ctx.send(file=picture)

bot.run('MTI5NDcwMDEwNTYzMDQ4MjQ2Mg.GSy9UU.BmjfdncFJ2cUh_EOTkYw-XUeU7Vju3MwLHvAiM')