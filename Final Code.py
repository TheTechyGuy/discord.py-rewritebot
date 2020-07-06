import discord
from discord.ext import commands, tasks
import random
from itertools import cycle
import os
from discord.utils import get
import youtube_dl
import praw

status = cycle(['Made By Triplayz', 'Subscribe To Triplayz On YT', 'twitch.tv/xtriplayz'])

client = commands.Bot(command_prefix='_')



reddit = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='')




@client.command()
async def meme(ctx):
    memes_submissions = reddit.subreddit('memes').hot()
    post_to_pick = random.randint(1, 100)
    for i in range(0, post_to_pick):
        submission = next(x for x in memes_submissions if not x.stickied)


    await ctx.send(submission.url)









@client.event
async def on_ready():
    change_status.start()
    print('Bot Is Ready')


@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.event
async def on_member_join(ctx, member):
    await ctx.send(f'{member} has join the server! Hooray!')


@client.event
async def on_member_remove(ctx, member):
    await ctx.send(f'{member} has left the server. Bummer :(')


@client.command()
async def ping(ctx):
    embed = discord.Embed(title="Ping", description="The Ping In Milliseconds")
    embed.add_field(name="The Ping Is", value=f'{round(client.latency * 1000)}ms')
    embed.add_field(name="Made By", value="Triplayz")

    await ctx.send(content=None, embed=embed)


@client.command(aliases=['8ball', '8balls=4men'])
@commands.has_role('Community')
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]

    embed = discord.Embed(title="8ball", description="Ask The Almighty 8ball")
    embed.add_field(name="Question", value=f'{question}')
    embed.add_field(name="Answer", value=f'{random.choice(responses)}')
    embed.add_field(name="Made By", value="Triplayz")


    await ctx.send(content=None, embed=embed)


@client.command()
@commands.has_role('Staff')
async def clear(ctx, amount=5):
    amount = amount + 1
    await ctx.channel.purge(limit=amount)


@client.command()

async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@client.command()
@commands.has_role('Staff')
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)


@client.command()
@commands.has_role('Staff')
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            return


@client.event
async def o(ctx, amount=5):
    await ctx.channel.purge(limit=amount)
    role = discord.utils.get(ctx.guild.roles, name="{Community}")
    await ctx.add_roles(role)


@client.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")


    embed = discord.Embed(title="Glimmer", description="Music Commands")
    embed.add_field(name="Glimmer Has Connected To:", value=f'{channel}')
    embed.add_field(name="Made By", value="Triplayz")

    await ctx.send(content=None, embed=embed)


@client.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")

        embed = discord.Embed(title="Glimmer", description="Music Commands")
        embed.add_field(name="Glimmer Has Left:", value=f'{channel}')
        embed.add_field(name="Made By", value="Triplayz")

        await ctx.send(content=None, embed=embed)

    else:
        print("Bot was told to leave voice channel, but was not in one")
        embed = discord.Embed(title="Glimmer", description="Music Commands")
        embed.add_field(name="Error:", value='I Dont Think I Am In A Voice Channel')
        embed.add_field(name="Made By", value="Triplayz")

        await ctx.send(content=None, embed=embed)


@client.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    embed = discord.Embed(title="Glimmer", description="Music Commands")
    embed.add_field(name="Glimmer Is ", value='Preparing To Play The Song')
    embed.add_field(name="Made By", value="Triplayz")

    await ctx.send(content=None, embed=embed)

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("Song done!"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.1

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")


@client.command()
async def ghelp(ctx):
    embeded = discord.Embed(title="Help on Glimmer", description="The Commands For Glimmer. ")
    embeded.add_field(name="_ping", value="Displays The Ping In Milliseconds")
    embeded.add_field(name="_kick @<username>", value="Kicks The User From The Server. Requires The Glimmer Bot Role")
    embeded.add_field(name="_ban @<username>", value="Bans The User From The Server. Requires The Glimmer Bot Role")
    embeded.add_field(name="_unban <Username>#<Tag>", value="Unbans The User From The Server. Requires The Glimmer Bot Role")
    embeded.add_field(name="_j", value="Tells Glimmer To Join Your Current Channel")
    embeded.add_field(name="_p <song url>", value="Tells Glimmer To Play The Song At The URL")
    embeded.add_field(name="_l", value="Tells Glimmer To Leave The Current Voice Channel")
    embeded.add_field(name="_8ball <Question>", value="Clears The Amount Of Messages You Specified.")
    embeded.add_field(name="_clear <# Of Messages>", value="Clears Messages")
    embeded.add_field(name="_usercount", value="Displays Number Of Users In Server")
    embeded.add_field(name="_meme", value="Posts A Random Meme From The Top Ten Section On Reddit")
    embeded.add_field(name="Made By", value="Triplayz")

    await ctx.send(content=None, embed=embeded)


@client.command()
async def standup(ctx):
    embededed = discord.Embed(title="Glimmer", description="Standup Commands")
    embededed.add_field(name="Glimmer Asks:", value="Hi, What Did You Acomplish Yesterday?")
    gordon = str(input(await ctx.send(content=None, embed=embededed)))
    print(gordon)



@client.event
async def  trisanthfind(message):
    if message.content.find("Trisanth", "trisanth") != -1:
        await message.channel.send("Hi")

@client.command()
async def usercount(ctx):
    id = client.get_guild(725579167009210398)
    embededed = discord.Embed(title="Glimmer", description="Usercount")
    embededed.add_field(name="The Number Of Users In This Server Is:", value=f"""{id.member_count}""")
    embededed.add_field(name="Made By:", value="Triplayz")

    await ctx.send(content=None, embed=embededed)






@client.command(aliases=['8balld'])
@commands.has_role('Leader')
async def _ball(ctx, *, question):
    gordon = ["It is certain.",
    "It is decidedly so.",
    "Without a doubt.",
    "Yes - definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",]
    embed = discord.Embed(title="8ball", description="Ask The Almighty 8ball")
    embed.add_field(name="Question", value=f'{question}')
    embed.add_field(name="Answer", value=f'{random.choice(gordon)}')
    embed.add_field(name="Made By", value="Triplayz")

    await ctx.send(content=None, embed=embed)







client.run('token')
