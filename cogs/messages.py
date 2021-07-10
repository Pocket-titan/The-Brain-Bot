import discord
from discord.ext import commands
import json
import requests
import openai
from datetime import date
import random
from debateTopics import debateTopics



def getAnswer(question):
    text = "The Brain is a chatbot that reluctantly answers questions.\nYou: How many pounds are in a kilogram?\nThe Brain: This again? There are 2.2 pounds in a kilogram. Please make a note of this.\nYou: What does HTML stand for?\nThe Brain: Was Google too busy? Hypertext Markup Language. The T is for try to ask better questions in the future.\nYou: When did the first airplane fly?\nThe Brain: On December 17, 1903, Wilbur and Orville Wright made the first flights. I wish they’d come and take me away.\nYou:" + str(
        question) + "\nThe Brain:"
    response = openai.Completion.create(
        engine="curie",
        prompt=text,
        temperature=0.6,
        max_tokens=60,
        top_p=0.3,
        frequency_penalty=0.75,
        presence_penalty=0.5,
        stop=["\n"]
    )
    answer = response["choices"][0]["text"]
    return answer


def getAnswer2(question):
    text = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: " + str(
        question) + "\n AI:",

    response = openai.Completion.create(
        engine="curie-instruct-beta",
        prompt=text,
        temperature=0.75,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )
    answer = response["choices"][0]["text"]
    return answer


def getAnswer3(question):
    text = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: " + str(
        question) + "\n AI:",

    response = openai.Completion.create(
        engine="davinci-instruct-beta",
        prompt=text,
        temperature=0.75,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )
    answer = response["choices"][0]["text"]
    return answer


def getJoke():
    response = requests.get('https://official-joke-api.appspot.com/random_joke')
    joke = json.loads(response.text)
    text = joke['setup'] + " \n " + joke['punchline']
    embed = discord.Embed(title=text, color=0x00ffff)
    return embed


def getProgrammingJoke():
    response = requests.get('https://official-joke-api.appspot.com/jokes/programming/random')
    joke = json.loads(response.text)
    text = joke[0]['setup'] + " \n " + joke[0]['punchline']
    embed = discord.Embed(title=text, color=0x00ffff)
    return embed


def getKnockKnock():
    response = requests.get('https://official-joke-api.appspot.com/jokes/knock-knock/random')
    joke = json.loads(response.text)
    text = joke[0]['setup'] + " \n " + joke[0]['punchline']
    embed = discord.Embed(title=text, color=0x00ffff)
    return embed


def getInsult():
    response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
    insult = json.loads(response.text)
    text = insult['insult']
    while 'testicles' in text or 'Suck' in text or 'chromosomes' in text or 'orangutans' in text or 'abortion' in text or \
            'Tampon' in text or 'reindeer!' in text or 'motherfucker.&quot;\r\n--&gt;' in text or 'jerk off' in text \
            or "amp&" in text or 'booble' in text or 'walt' in text or 'dick,' in text or 'twatface' in text:
        response = requests.get('https://evilinsult.com/generate_insult.php?lang=en&type=json')
        insult = json.loads(response.text)
        text = insult['insult']
    embed = discord.Embed(title=text, color=0x00ffff)
    return embed


def getQuote():
    id = random.randint(1, 583)
    response = requests.get('https://philosophyapi.herokuapp.com/api/ideas/' + str(id))
    json_data = json.loads(response.text)
    quote = '"' + json_data['quote'] + '" \n                           -' + json_data['author']
    while len(quote) >= 256:
        quote = '"' + json_data['quote'] + '" \n                           -' + json_data['author']
    embed = discord.Embed(title=quote, color=0x00ffff)
    return embed


def getAdvice():
    response = requests.get('https://api.adviceslip.com/advice')
    advice = json.loads(response.text)
    text = advice['slip']['advice']
    embed = discord.Embed(title=text, color=0x00ffff)
    return embed


def getSearch(searchterm):
    response = requests.get('http://philosophyapi.herokuapp.com/api/ideas/?search=' + str(searchterm))
    json_data = json.loads(response.text)
    # print(json_data)
    if json_data['count'] != 0:
        quotelist = json_data['results']
        if len(quotelist) == 1:
            quote = '"' + quotelist[0]['quote'] + '" \n                           -' + quotelist[0]['author']
            while len(quote) >= 256:
                quote = '"' + quotelist[0]['quote'] + '" \n                           -' + quotelist[0]['author']
        else:
            rand = random.randint(0, len(quotelist) - 1)
            quote = '"' + quotelist[rand]['quote'] + '" \n                           -' + quotelist[rand]['author']
            while len(quote) >= 256:
                rand = random.randint(0, len(quotelist) - 1)
                quote = '"' + quotelist[rand]['quote'] + '" \n                           -' + quotelist[rand]['author']
    else:
        quote = "Couldn't find a quote with that search. Try another search term."
    # print(quote)
    embed = discord.Embed(title=quote, color=0x00ffff)
    return embed


def getSearchPhilosopher(philosopher):
    response = requests.get('https://philosophyapi.herokuapp.com/api/philosophers/?search=' + str(philosopher))
    json_data = json.loads(response.text)
    if json_data['count'] != 0:
        quotelist = json_data['results'][0]['ideas']
        name = json_data['results'][0]['name']
        rand = random.randint(1, len(quotelist) - 1)
        quote = '"' + quotelist[rand] + '"\n                         -' + name
    else:
        quote = "Search Term not found. Try a different philosopher."

    embed = discord.Embed(title=quote, color=0x00ffff)
    return embed


def getMathFact():
    response = requests.get('http://numbersapi.com/random/math')
    embed = discord.Embed(title=response.text, color=0x00ffff)
    return embed


def getDateFact():
    today = date.today()
    day = today.day
    month = today.month
    response = requests.get('http://numbersapi.com/' + str(month) + '/' + str(day) + '/date')
    embed = discord.Embed(title=response.text, color=0x00ffff)
    return embed


def getDefinition(search):
    response = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en_US/' + str(search))
    text = json.loads(response.text)
    if len(text) == 3:
        return ["Word not found. Try again."]
    else:
        word = text[0]['word']
        def_list = []
        definitions = text[0]['meanings']
        for i in range(len(definitions)):
            type = definitions[i]['partOfSpeech']
            definition = definitions[i]['definitions'][0]['definition']
            def_list.append([type, definition])
        return [word, def_list]


class Messages(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def joke(self, ctx):
        await ctx.send(embed=getJoke())

    @commands.command()
    async def programming(self, ctx):
        await ctx.send(embed=getProgrammingJoke())

    @commands.command()
    async def knockknock(self, ctx):
        await ctx.send(embed=getKnockKnock())

    @commands.command()
    async def debatetopic(self,ctx):
        rand = random.randint(1, len(debateTopics))
        # await ctx.send(debateTopics[rand])
        while len(debateTopics[rand]) > 256:
            rand = random.randint(1, len(debateTopics))

        embed = discord.Embed(title=debateTopics[rand], color=0xc203fc)
        embed.add_field(name="It's .debatetopic for more!", value="** **")
        embed.set_footer(
            text="For more info check the Rules and Info channel. \nIf you encouter any issues, DM me or any of the mods!")
        await ctx.send(embed=embed)

    @commands.command()
    async def quote(self,ctx, *, searchterm=None):
        if searchterm == None:
            await ctx.send(embed=getQuote())
        else:
            await ctx.send(embed=getSearch(searchterm))

    @commands.command()
    async def search(self,ctx, *, searchterm):
        await ctx.send(embed=getSearchPhilosopher(searchterm))

    @commands.command()
    async def ask2(self,ctx, *, question: str):
        # if '@everyone' in question or '@here' in question or '@Member':
        answer = getAnswer2(question)
        if '@' in question or '@' in answer:
            await ctx.send("No.")
            return
        await ctx.send(answer)

    @commands.command()
    async def ask(self,ctx, *, question):
        # if '@everyone' in question or '@here' in question:
        answer = getAnswer(question)
        if '@' in question or '@' in answer:
            await ctx.send("No.")
            return
        await ctx.send(answer)

    @commands.command(aliases=['pl'])
    async def poll(self, ctx, *, msg):
        embed = discord.Embed(title=msg, color=ctx.author.color)
        message = await ctx.send(embed=embed)
        await message.add_reaction("<:upvote:837763222513778759>")
        await message.add_reaction("<:downvote:837763222886547486>")

    @commands.command()
    async def makepoll(self, ctx, options: int, messagelink):
        if options > 9:
            await ctx.send("Can only add up to 9 options. Try again with less.")
            return
        try:
            messagelink = messagelink.strip()
            if len(messagelink) == 18:
                try:
                    message = await ctx.fetch_message(int(messagelink))
                except:
                    await ctx.send("Either the message ID is invalid, or you are not in the channel of the message.")
                    return
            else:
                links = messagelink.split('/')
                messageid = int(links[-1])
                channelid = int(links[-2])
                guildid = int(links[-3])

                server = self.client.get_guild(guildid)
                channel = server.get_channel(channelid)
                message = await channel.fetch_message(messageid)
        except:
            await ctx.send("Invalid message link, try again.")
            return

        reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

        for i in range(options):
            await message.add_reaction(reactions[i])

    @commands.command()
    async def advice(self,ctx):
        await ctx.send(embed=getAdvice())

    @commands.command()
    async def insult(self,ctx):
        await ctx.send(embed=getInsult())

    @commands.command()
    async def mathfact(self,ctx):
        await ctx.send(embed=getMathFact())

    @commands.command()
    async def today(self,ctx):
        await ctx.send(embed=getDateFact())

    @commands.command()
    async def define(self,ctx, *, search):
        result = getDefinition(search)
        if len(result) > 1:
            embedVar = discord.Embed(title=result[0], color=0x000000)
            for i in result[1]:
                embedVar.add_field(name=i[0], value=i[1], inline=False)
            await ctx.send(embed=embedVar)
        else:
            await ctx.send(result[0])


    @commands.command()
    async def sep(self,ctx, *, text):
        text = text.strip()
        text = text.replace(" ", "-")
        if '@' in text:
            await ctx.send("No.")
            return
        link = 'https://plato.stanford.edu/entries/' + text
        response = requests.get(link)
        if response.status_code == 404:
            link = " https://plato.stanford.edu/search/searcher.py?query=" + text
        await ctx.send(link)

    @commands.command()
    async def wiki(self,ctx, *, text):
        text = text.strip()
        text = text.replace(" ", "_")
        if '@' in text:
            await ctx.send("No.")
            return
        link = 'https://en.wikipedia.org/wiki/' + text
        response = requests.get(link)
        if response.status_code == 404:
            link = 'https://en.wikipedia.org/w/index.php?search=' + text
        await ctx.send(link)

    @commands.command()
    async def google(self,ctx, *, text):
        text = text.strip()
        text = text.replace(' ', '+')
        if '@' in text:
            await ctx.send("No.")
            return
        text = 'https://www.google.com/search?q=' + text
        await ctx.send(text)

    @commands.command()
    async def ob(self, ctx, *, emotename=None):
        if not emotename == None:
            emotename = emotename.strip()
            observer = self.client.get_guild(737104128777650217)
            if emotename == "list":
                c = 0
                returnt = ''
                line = ''
                for emote in observer.emojis:
                    line = line + " " + emote.name
                    c += 1
                    if c == 3:
                        returnt = returnt + "`" + line + "` \n"
                        line = ''
                        c = 0
                await ctx.send(returnt)
            else:
                for emote in observer.emojis:
                    if emotename == emote.name[3:].lower():
                        await ctx.message.delete()
                        await ctx.send(str(emote))
                        break
        else:
            await ctx.send("Try .ob [emote name] or .ob [list]")


def setup(client):
    client.add_cog(Messages(client))