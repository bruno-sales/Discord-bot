import discord
import sympy
import random
from imgurpython import ImgurClient

# Discord client
client = discord.Client()

# Imgur Client
client_imgur_id = 'My id'
client_imgur_secret = 'My Secret is secret'
client_imgur = ImgurClient(client_imgur_id, client_imgur_secret)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('%juan'):
        await message.channel.send('Juan.')

    if message.content.startswith('%help'):
        await message.channel.send(get_help())

    if message.content.startswith('%parrot'):
        reply = message.content[7:]
        await message.channel.send(reply)

    if message.content.startswith('%calc'):
        equation = message.content[5:]
        try:
            result = calculate(equation)
            await message.channel.send(str(result)+'\nHave you really asked a horse to do math?')
        except:
            await message.channel.send('I cannot do that!\nHave you really asked a horse to do math?')

    if message.content.startswith('%simp'):
        query = message.content[5:]
        img_url = get_random_image(query)
        await message.channel.send(img_url)


def get_help():
    help = '**help**: Haven''t you just done that?\n' \
            '**juan**: Juan?\n' \
            '**parrot**: Repeats what you said. Just because.\n' \
            '**simp**: Grabs a random image from the interwebs.\n' \
            '**calc**: Quick maths.\n'
    return help


def calculate(text):
    return sympy.sympify(text)


def get_random_image(query):
    items = client_imgur.gallery_search(query, advanced=None, sort='time', window='all', page=0)
    total_items = len(items)
    rand_item = items[random.randint(0, total_items - 1)]

    total_images = len(rand_item.images)
    rand_img = rand_item.images[random.randint(0, total_images - 1)]
    return rand_img['link']


client.run('THE ULTIMATE TOKEN')
