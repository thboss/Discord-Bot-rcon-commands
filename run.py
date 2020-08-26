from discord.ext import commands
from discord.ext.commands import has_permissions, CheckFailure
import discord
import json
from json.decoder import JSONDecodeError
from util import send_rcon_command

TOKEN = 'xxxxxxxxxxxx'
SERVERS = 'ip:port:rcon_password:server_name--ip:port:rcon_password:server_name'

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





    
    
        
    
        
            
        
            
        
            
            
                
                
                

     
                
            
                

    
    


@bot.command(brief='Live match status')
async def live(ctx):
    """send rcon command 'get5_status' to server and get response"""
    isLive = False
    servers = SERVERS.split('--')

    for i in range(len(servers)):
        server = servers[i].split(':')
        resp = send_rcon_command(server[0], int(server[1]), server[2], 'get5_status')
        if resp is None:
            embed = discord.Embed(title=f'Server **{server[3]}** is down!')
            await ctx.send(embed=embed)
        else:
            try:
                resp = json.loads(resp)
            except JSONDecodeError:
                pass
            else:
                if resp['gamestate']:
                    isLive = True
                    msg = f'**Match ID :** {resp["matchid"]}\n' \
                          f'**Match state :** {resp["gamestate_string"]}\n' \
                          f'**Map :** {resp["maps"]["map0"]}\n' \
                          f'**Score :**'

                    embed = discord.Embed(title=server[3], description=msg)
                    embed.add_field(name=f'{resp["team1"]["name"]}', value=f'{resp["team1"]["current_map_score"]}')
                    embed.add_field(name=f'{resp["team2"]["name"]}', value=f'{resp["team2"]["current_map_score"]}')
                    await ctx.send(embed=embed)

    if not isLive:
        embed = discord.Embed(title='No live matches for now')
        await ctx.send(embed=embed)


@rcon.error
async def rcon_error(ctx, error):
    if isinstance(error, CheckFailure):
        msg = "You don't have permission to use this command!"
        embed = discord.Embed(title=msg)
        await ctx.send(embed=embed)


bot.run(TOKEN)
