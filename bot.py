import discord
from discord.ext import commands, tasks
import random
import openai
from dotenv import load_dotenv
import os
import asyncio

from cogs.messages import getDateFact, getQuote, getAdvice
from databaselayer import *
# from debateTopics import debateTopics


# get bot token and openai apikey
load_dotenv()
openai.api_key = os.getenv('APIKEY')
bot_token = os.getenv('TOKEN')


# with open('token.json') as json_file:
#     data = json.load(json_file)
#
# openai.api_key = data['APIKEY']


# todolist = []

intents = discord.Intents().default()
intents.members = True
client = commands.Bot(command_prefix='.', help_command=None, intents=intents)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('with ideas'))
    print("I am alive.")
    waterreminder.start()
    vccheck.start()
    # await asyncio.sleep(1800)
    # debatetopicloop.start()


# @client.command()
# async def test(ctx):
#     c = client.get_channel(831215253076574219)
#     embed = discord.Embed(title= ":heart: Love Island Role!",colour=0xff0000)
#     await c.send(embed=embed)


@tasks.loop(minutes=1)
async def vccheck():
    vat = client.get_guild(831211215375433728)
    vc_channels = vat.voice_channels
    for channel in vc_channels:
        if channel.id == 835061032073297920:
            continue
        for member in channel.members:
            ammount = 20
            if member.voice.self_deaf:
                ammount = 5
            addBal(member.id, ammount)


@tasks.loop(minutes=60)
async def waterreminder():
    general = client.get_channel(831211215878488078)
    embed = getDateFact()
    embed.add_field(name="This is your hourly reminder to go drink some water!", value="** **")
    embed.set_footer(
        text="For more info check the Rules and Info channel. \nIf you encouter any issues, DM me or any of the mods!")
    await general.send(embed=embed)

# @tasks.loop(minutes=60)
# async def debatetopicloop():
#     await client.wait_until_ready()
#     general = client.get_channel(831211215878488078)
#     rand = random.randint(1, len(debateTopics))
#     while len(debateTopics[rand]) > 250:
#         rand = random.randint(1, len(debateTopics))
#
#     embed = discord.Embed(title=debateTopics[rand], color=0xc203fc)
#     embed.add_field(name="It's .debatetopic for more!", value="** **")
#
#     embed.set_footer(
#         text="For more info check the Rules and Info channel. \nIf you encouter any issues, DM me or any of the mods!")
#     await general.send(embed=embed)


@client.command()
@commands.has_any_role(835623182484373535,835400292979179530)
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send("done")


@client.command()
@commands.has_any_role(835623182484373535,835400292979179530)
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send("Done")


@client.command()
@commands.has_any_role(835623182484373535,835400292979179530)
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send("Done")


@client.command()
@commands.has_any_role(835623182484373535, 835400292979179530)
async def loadall(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.load_extension(f"cogs.{filename[:-3]}")
            print(f"{filename} has been loaded.")
    await ctx.send("Done.")


@client.command()
@commands.has_any_role(835623182484373535, 835400292979179530)
async def unloadall(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            client.unload_extension(f"cogs.{filename[:-3]}")
            print(f"{filename} has been unloaded.")
    await ctx.send("Done.")


@client.command()
@commands.has_any_role(835623182484373535, 835400292979179530)
async def cogstatus(ctx):
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                client.load_extension(f"cogs.{filename[:-3]}")
            except commands.ExtensionAlreadyLoaded:
                await ctx.send(f"{filename} is loaded")
            except commands.ExtensionNotFound:
                await ctx.send(f"{filename} not found")
            else:
                await ctx.send(f"{filename} is unloaded")
                client.unload_extension(f"cogs.{filename[:-3]}")

    await ctx.send("Done.")


@client.command()
@commands.has_any_role(835623182484373535, 835400292979179530)
async def coglist(ctx):
    embed = discord.Embed(title="List of Cogs",color=0x00ffff)
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            embed.add_field(name=filename, value="** **", inline=True)
    await ctx.send(embed=embed)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.CommandOnCooldown):
        if error.retry_after < 60:
            await ctx.send(f'This command is on cooldown, you can use it in {round(error.retry_after, 1)} seconds')
        elif error.retry_after > 3600:
            timeleft = (error.retry_after / 60) / 60
            await ctx.send(f'This command is on cooldown, you can use it in {round(timeleft, 1)} hour(s).')
        else:
            timeleft = error.retry_after / 60
            await ctx.send(f'This command is on cooldown, you can use it in {round(timeleft, 1)} minute(s)')

    elif isinstance(error,commands.MissingPermissions):
        await ctx.send("You do not have the permissions to use that command.")
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("You are missing a required argument, please try again.")
    elif isinstance(error,commands.MemberNotFound):
        await ctx.send("Member was not found, please try again.")
    elif isinstance(error,commands.ChannelNotFound):
        await ctx.send("The channel could not be found or does not exist, please try again.")
    elif isinstance(error,commands.BadArgument):
        await ctx.send("One of the arguments failed. Please try again.\n P.S. If a member is a required argument, you must **mention** them with @.")
    elif isinstance(error,commands.TooManyArguments):
        await ctx.send("You have added too many arguments, please try again.")
    elif isinstance(error,commands.MissingRole):
        await ctx.send("You do not have the roles required for that command, please try again.")

    elif isinstance(error,commands.CommandInvokeError):
        if "(error code: 40032)" in str(error.original):
            await ctx.send("User was not connected to voice.")
        else:
            await ctx.send(f"Command raised an exception: {error.original}")


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content == "!d bump":
        def check(m):
            return m.author == client.get_user(302050872383242240)

        reply = await client.wait_for('message', check=check)
        embed = reply.embeds[0]
        if "Bump done" in embed.description:
            await message.channel.send("Thanks for bumping the server! We really appreciate the support!\n Here's 1000 Brain Cells for the effort!")
            addBal(message.author.id, 1000)
            await asyncio.sleep(7200)
            await message.channel.send("Time for a bump!")
        # await message.channel.send("TRUE")
        # else:
        #     await message.channel.send("FALSE")
        # await message.channel.send(embed=embed)
        # await message.channel.send(f"title = {embed.title} \n description = {embed.description}")

    try:
        rand = random.randint(1, 2)
        if rand == 2:
            addBal(message.author.id, 1)
    except:
        pass

    # Processing the message so commands will work
    await client.process_commands(message)


@client.event
async def on_member_remove(member):
    deleteUser(member.id)

# @client.event
# async def on_member_join(member):
#     createUser(member.id)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")
        print(f"{filename} has been loaded.")


# data['TOKEN']
client.run(bot_token)