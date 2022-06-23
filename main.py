import discord
import sympy
import random
import requests
from io import BytesIO
from imgurpython import ImgurClient
from discord.ext import commands

# Discord client
client = commands.Bot(command_prefix="%")

# Imgur Client
client_imgur_id = 'My id'
client_imgur_secret = 'My Secret is secret'
client_imgur = ImgurClient(client_imgur_id, client_imgur_secret)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)


@client.command()
async def juan(ctx):
    await ctx.channel.send('Juan.')


@client.command()
async def parrot(ctx, message):
    await ctx.channel.send(message)


@client.command()
async def helpme(ctx):
    await ctx.channel.send(get_help())


@client.command()
async def calc(ctx, message):
    try:
        result = calculate(message)
        await ctx.channel.send(str(result) + '\nHave you really asked a horse to do math?')
    except:
        await ctx.channel.send('I cannot do that!\nHave you really asked a horse to do math?')


@client.command()
async def simp(ctx, message):
    query = message.replace(" ", "+")
    img_url, found = get_random_image(query, False)
    await ctx.channel.send(img_url)


@client.command(name="ssimp")
async def spoiler_simp(ctx, message):
    query = message.replace(" ", "+")
    img, found = get_random_image(query, True)
    if found:
        await ctx.channel.send(file=discord.File(img, 'SPOILER_spoilerimg.png'))
    else:
        await ctx.channel.send(img)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('What the dog doin?'))


def get_help():
    help = '**helpme**: Haven''t you just done that?\n' \
           '**juan**: Juan?\n' \
           '**parrot**: Repeats what you said. Just because.\n' \
           '**simp**: Grabs a random image from the interwebs.\n' \
           '**ssimp**: Grabs a random image from the interwebs and displays as spoiler.\n' \
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
