import discord
import random
from discord.ext import commands, tasks



client = commands.Bot(command_prefix='t!')


@client.command()
async def hi(ctx):
    await ctx.send('Hi, My Name Is Yt Test Bot')

@client.command()
async def ping(ctx):
    await ctx.send(f'The Ping For Me Is {round(client.latency * 1000)}ms')

@client.command(aliases=['8ball'])
async def eightball(ctx, *, question):
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
    await ctx.send(f'Question : {question}  ;  Answer:  {random.choice(responses)}')





client.run('NzI5NDg5NjYwMzc5OTIyNTc0.XwP-mQ.3mukMfzuQ71jm1Jgj4nVfXN-L1E')
