import discord
from discord.ext import commands
import random,os
import logging
description = description = '''An example bot to showcase the discord.ext.commands extension
module.An example bot to showcase the discord.ext.commands extension
module.description = '''



intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', description=description, intents=intents)

CHANNEL_ID = 1297235593948037241
palabras=[" Los árboles pueden (dormir) por la noche. Durante el día, los árboles expanden sus hojas hacia la luz solar para maximizar la fotosíntesis. Sin embargo, estudios recientes han demostrado que por la noche, muchas especies de árboles bajan ligeramente sus ramas y hojas, como si estuvieran descansando. Este fenómeno es similar a un (ciclo de sueño) en las plantas, aunque no está del todo claro por qué sucede. Se cree que podría estar relacionado con la conservación de energía.",
        "Las plantas pueden comunicarse entre sí. Cuando algunas plantas están siendo atacadas por insectos, liberan sustancias químicas en el aire llamadas compuestos orgánicos volátiles (COV). Estas señales químicas alertan a las plantas cercanas del peligro, lo que provoca que refuercen sus defensas, como producir toxinas para repeler a los insectos. ¡Es una especie de (advertencia) entre plantas!",
        " El océano produce más oxígeno que los bosques El fitoplancton, pequeñas algas presentes en los océanos, son responsables de producir más del 50% del oxígeno que respiramos, superando a los bosques tropicales.",
        " Los plásticos tardan siglos en descomponerse Dependiendo del tipo, los plásticos pueden tardar entre 500 y 1,000 años en descomponerse completamente. Por eso, reducir su uso y reciclar es esencial para el medio ambiente.",
        "Noruega transforma las 300.000 toneladas de basura anuales que no pueden ser recicladas en energía limpia. Los desperdicios no aprovechables se queman a 800 grados. El calor resultante sirve para hacer hervir agua y el vapor que se desprende va a parar a una turbina, cuyo movimiento se transforma en electricidad, almacenable y transportable."]
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        await channel.send('''¡Hola! Estoy listo para ayudarte a aprender sobre el medio ambiente.
                           1.($a_1)_que son islas de basura en el oceano
                           2.($a_2)_que es reutilizar el plastico
                           3.($a_3)_como se puede cuidar el oxigeno en el medio ambiente
                           4.($a_4)_que es el reciclaje y por que es importante
                           5.($a_5)_donde botar los aparatos electronicos dañados
                           6.($dato)_dato curioso''')
@bot.event
async def on_message(message):
    if message.content.startswith('!dato'):
        palabra1 = random.choice(palabras)
        await message.channel.send(palabra1)
    await bot.process_commands(message)

@bot.command("a_1")
async def a_1(ctx):
    await ctx.send(f"Las islas de basura son zonas de los océanos donde se acumulan gran cantidad de desechos sólidos debido a características particulares de las corrientes marinas. El principal componente de estas islas es el plástico, que proviene en su mayor parte de las zonas costeras.")
@bot.command("a_2")
async def a_2(ctx):
    await ctx.send(f"Reutilizar consiste en darle a un material la máxima vida útil. Una de las formas es usar productos que se pueden utilizar muchas veces, como las bolsas de tela para hacer la compra, los tarros de vidrio para guardar conservas, botellas de vidrio para el agua fría de la nevera, etc.")
@bot.command("a_3")
async def a_3(ctx):
    await ctx.send(f"Para cuidar el oxígeno Se necesitan ideas y estas son algunas: 1 Los árboles, liberan oxígeno al realizar la fotosíntesis y eliminan el dióxido de carbono. 2 menos emisiones de fábricas y vehículos que mejoran la calidad del aire, Ambos generan gran parte del oxígeno del planeta. 3 menos combustibles fósiles significa menos dióxido de carbono y más oxígeno limpio.")
@bot.command("a_4")
async def a_4(ctx):
    await ctx.send(f"El reciclaje es el proceso de convertir materiales desechados (como papel, plástico, vidrio y metal) en nuevos productos. En resumen, el reciclaje protege el medio ambiente y promueve un uso más sostenible de los recursos. Porque es importante: Ahorra recursos naturales, Disminuye la contaminación, Ahorra energía y Combate el cambio climático")
@bot.command("a_5")
async def a_5(ctx):
    await ctx.send(f"Los RAEE o basura electrónica pueden contener sustancias peligrosas y gases que agotan la capa de ozono o que afectan al calentamiento global y pueden ser perjudiciales para la salud humana. Por eso, el punto limpio es el mejor lugar para este tipo de residuos domésticos.")
@bot.command("dato")
async def dato(ctx):
    dato = random.choice(palabras)
    await ctx.send(dato)
@bot.command("secreto")
async def secreto(ctx):
    await ctx.send(f'Gracias profe')


bot.run('MTI5NzI1MzUwOTA2MTgwNDA2Mw.G_mkqD.Le70H3zAxCr1IglRWT7DyEezg3cNn5S2aufYOE')