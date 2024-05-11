#Импортируем библиотеки
import discord
from discord import ui, ButtonStyle, TextStyle
from PIL import Image, ImageDraw


#Создаем модальное окно
class Resize_Modal(ui.Modal, title='Поменять размер'):
    #Берем у user о Высоте 
    field_1 = ui.TextInput(label='Высота')
    #Берем у user о длине
    field_2 = ui.TextInput(label='Длина')



    #Когда нажата 
    async def on_submit(self, interaction: discord.Interaction):
        #Испровляем
        await interaction.message.edit(content=f'Высота: {self.field_1}\n'
                                               f'Длина: {self.field_2}')
        
        #Приврошаем Textinput файл на int
        s1 = str(self.field_1)
        s2 = str(self.field_2)
        h = int(s1)
        w = int(s2)

        #Открываем фото
        img = Image.open('test.jpg')
        #Меняем розмер
        size = (h,w)
        result = img.resize(size)

        #Вставляем воденой знак
        watemark = Image.open('water_m.png')
        size = (100,100)
        watermark = watemark.resize(size)
        position = (img.width - watermark.width, img.height - watermark.height)
        img.paste(watermark, position)
        
        #Сахроняем фото
        result.save('Finish.jpg')
        #Удоляем фото
        img.close()

        #Проверка на нажатие
        if not interaction.response.is_done():
            await interaction.response.defer()

        #Открываем фото
        with open('Finish.jpg', 'rb') as f:
            picture = discord.File(f)
            #Отпровляем
            await interaction.channel.send(file=picture, delete_after=60.0)
            img2 = Image.open("Finish.jpg")
            #Удоляем фото
            img2.close()

#Создаем кнопку
class ResizeButton(ui.Button):

    def __init__(self,
                 label="Поменять размер",
                 style=ButtonStyle.blurple,
                 row=0):
        super().__init__(label=label, style=style, row=row)

    #Когда нажата 
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(Resize_Modal())
        self.style = ButtonStyle.gray

        #Проверка на нажатие
        if not interaction.response.is_done():
            await interaction.response.defer()

#Создаем класс для хронения кнопок
class Resize(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ResizeButton(label='Изменить Размер'))
