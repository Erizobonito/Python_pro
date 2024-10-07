import discord
from discord.ext import commands

description = '''An example bot to showcase the discord.ext.commands extension module. There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('!deleteme'):
        msg = await message.channel.send('I will delete myself now...')
        await msg.delete()

    await message.channel.send('Goodbye in 3 seconds...', delete_after=3.0)

@client.event
async def on_message_delete(message):
    msg = f'{message.author} has deleted the message: {message.content}'
    channel = message.channel
    await channel.send(msg)

# Reemplaza 'tu_token_aqui' con tu token real
client.run('MTI5MjE2NTk5MTE3ODA0NzUwOA.GnQFcm.HStUv-RWHaL0CV53gxuR0YgvIb236i7KA5Bd-g')
