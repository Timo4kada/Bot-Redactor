#Импорт библиотек
from config import TOKEN
from discord import Intents
from discord.ext import commands
from PIL import Image
import requests
from ui_model import *


q2 = 0

bot = commands.Bot(command_prefix="!", intents=Intents.all())


#Создание команд:
@bot.command()
#Команда для открытие фото
async def open_image(ctx):
    global q2
    try:
        q2 = 0
        q = ctx.message.attachments
        img = Image.open(requests.get(q[0].url, stream=True).raw)
        img.save("test.jpg")
        if q2 != 3:
            await ctx.channel.send('Фото принято!', delete_after=10.0)
            q2 = 1
    except:
        q2 = 3
        await ctx.channel.send('Вы не отправили фото!', delete_after=10.0)

    


@bot.command()
#Команда для изменения размера
async def resize(ctx):
    global q2
    if q2 == 1:
        with open('test.jpg', 'rb') as f:
            picture = discord.File(f)
            #Отпровляем фото на дискорд
            await ctx.channel.send(file=picture, delete_after=60.0)
            #Отпровляем кнопку для изменения
            await ctx.message.channel.send("", view=Resize(),delete_after=60.0)

#Команда для изменения цвета
@bot.command()
async def make_gray(ctx):
    global q2
    if q2 == 1:
        #Изменяем цвет
        img = Image.open('test.jpg').convert('L')
        #Вставляем воденой знак
        watemark = Image.open('water_m.png')
        size = (100,100)
        watermark = watemark.resize(size)
        position = (img.width - watermark.width, img.height - watermark.height)
        img.paste(watermark, position)
        img.save('gray.jpg')
        #Отпровляем фото на дискорд
        await ctx.channel.send(file=discord.File('gray.jpg'), delete_after=60.0)

#Команда для видио
@bot.command()
async def help_vidio(ctx):
    #Отпровляем видио
    await ctx.channel.send(file=discord.File("gatebook.mp4"), delete_after=60.0)

bot.run(TOKEN)