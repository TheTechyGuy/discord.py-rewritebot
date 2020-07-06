import discord
from discord.ext import commands, tasks



client = commands.Bot(command_prefix='t!')


@client.command()
async def hi(ctx):
    await ctx.send('Hi, My Name Is Yt Test Bot')



client.run('Token')
