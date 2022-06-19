import discord
import sympy
import random
import requests
from io import BytesIO
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
            await message.channel.send(str(result) + '\nHave you really asked a horse to do math?')
        except:
            await message.channel.send('I cannot do that!\nHave you really asked a horse to do math?')

    if message.content.startswith('%simp'):
        query = message.content[5:].replace(" ", "+")
        img_url, found = get_random_image(query, False)
        await message.channel.send(img_url)

    if message.content.startswith('%ssimp'):
        query = message.content[6:].replace(" ", "+")
        img, found = get_random_image(query, True)
        if found:
            await message.channel.send(file=discord.File(img, 'SPOILER_spoilerimg.png'))
        else:
            await message.channel.send(img)


def get_help():
    help = '**help**: Haven''t you just done that?\n' \
           '**juan**: Juan?\n' \
           '**parrot**: Repeats what you said. Just because.\n' \
           '**simp**: Grabs a random image from the interwebs.\n' \
           '**ssimp**: Grabs a random image from the interwebs and displays as a spoiler.\n' \
           '**calc**: Quick maths.\n'
    return help


def calculate(text):
    return sympy.sympify(text)


def get_random_image(query, spoiler):
    items = client_imgur.gallery_search(query, advanced=None, sort='time', window='all', page=0)
    total_items = len(items)
    not_found_images = 'Juan is sad because he could not deliver you nothing.'

    if total_items > 0:
        rand_item = items[random.randint(0, total_items - 1)]
        total_images = len(rand_item.images)

        if total_images > 0:
            rand_img = rand_item.images[random.randint(0, total_images - 1)]
            if not spoiler:
                return rand_img['link'], True
            else:
                response = requests.get(rand_img['link'])
                return BytesIO(response.content), True
        else:
            return not_found_images, False

    else:
        return not_found_images, False


client.run('THE ULTIMATE TOKEN')
