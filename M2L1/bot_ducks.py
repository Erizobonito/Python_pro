import discord
from discord.ext import commands
import os, random
import requests
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
@bot.event
async def on_ready():
    print(f'Ha iniciado sesión como {bot.user}')
def get_duck_image_url():
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']
@bot.command('duck')
async def duck(ctx):
    '''Cada vez que se llama a la solicitud de pato, el programa llama a la función get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)
@bot.command()
async def mem(ctx):
    img_name = random.choice(os.listdir('images'))
    with open(f'images/{img_name}', 'rb') as f:
        picture = discord.File(f)
 
    await ctx.send(file=picture)


async def gru(ctx):
    protocols = ['http', 'https']
    domains = ['com', 'net', 'org', 'io', 'dev']
    words = ['example', 'test', 'sample', 'demo', 'random']
    
    protocol = random.choice(protocols)
    domain = random.choice(words) + '.' + random.choice(domains)
    path = '/path' + str(random.randint(100, 999))
    
    return f'{protocol}://{domain}{path}'

    print("URL aleatoria:", generate_random_url())


bot.run('MTI5NDcxODM3OTk0MDEyMjc0Ng.GDxDgA.2kvsJeh234b5fvtjaAw19moCluNdSt5ZpEfG4Y')