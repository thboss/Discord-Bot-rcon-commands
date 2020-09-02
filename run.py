from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
import discord
from util import send_rcon_command

TOKEN = 'xxxxxxxxxxxx'
SERVERS = 'ip:port:rcon_password:server_name--ip:port:rcon_password:server_name--...etc'

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print("Connected!")


@bot.command(brief='Send rcon command to server')
@has_permissions(administrator=True)
async def rcon(ctx, *args):
    """send rcon command to csgo server and get response in message"""
    _server = ''
    title = ''
    if len(args) < 2:
        msg = '**Invalid usage:** !rcon <server number> <command1> <command2> ...'
    else:
        try:
            server = SERVERS.split('--')[int(args[0]) - 1].split(':')
            _server = server[3]
        except (IndexError, TypeError, ValueError):
            msg = 'Invalid usage <server number> <command>'
            title = None
        else:
            msg = send_rcon_command(server[0], int(server[1]), server[2],
                                    ' '.join(args[i] for i in range(1, len(args))))
            title = f'Command sent to server {_server}'
            if msg is None:
                msg = f'Server **{server[3]}** is down!'
                title = None

    embed = discord.Embed(title=title, description=msg)
    await ctx.send(embed=embed)


@rcon.error
async def rcon_error(ctx, error):
    if isinstance(error, CheckFailure):
        msg = "You don't have permission to use this command!"
        embed = discord.Embed(title=msg)
        await ctx.send(embed=embed)


bot.run(TOKEN)
