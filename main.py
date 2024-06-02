import discord
from discord.ext import commands
from mcstatus import JavaServer
import subprocess
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), help_command=None, intents=intents)
server = JavaServer.lookup("Your_server_adresse")
target_channel_id = YOUR_TARGET_CHANNEL_ID_HERE

@bot.event
async def on_ready():
    print("Bot is ready")

@bot.event
async def on_message(message):
    print(f"{message.author} in {message.channel} said: {message.content}")
    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

async def start_server(ctx, loading_message):
    subprocess.Popen(['/bin/bash', 'start_server.sh'])
    await loading_message.edit(content="Starting the Minecraft server...")
    loading_state = 0
    moon_emojis = ["□■■■", "■□■■", "■■□■", "■■■□"]  # Moon emojis list
    while True:
        try:
            if server.ping():
                break
        except Exception:
            pass
        
        loading_content = f"Loading {moon_emojis[loading_state]}"
        await loading_message.edit(content=loading_content)
        loading_state = (loading_state + 1) % len(moon_emojis)
        await asyncio.sleep(1)

    await loading_message.delete()
    await ctx.send("The Minecraft server has started successfully!")

@bot.command()
async def startserv(ctx):
    loading_message = await ctx.send("Starting the server...")
    try:
        status = server.status()
        await loading_message.edit(content="The Minecraft server is already started.")
    except Exception as e:
        await start_server(ctx, loading_message)

@bot.command()
async def stopserv(ctx):
    subprocess.Popen(['pkill', '-f', 'java'])
    
    embed = discord.Embed(
        title="Minecraft Server Shutdown",
        description="The Minecraft server is now offline.",
        color=0xFF0000
    )
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1828/1828778.png")
    embed.set_footer(text=f"Command executed by {ctx.author}", icon_url=ctx.author.avatar.url)
    
    await ctx.send(embed=embed)

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Available Commands:",
        description="Here are the commands you can use with this bot:",
        color=0xFFFF00
    )
    embed.add_field(name="!ping", value="Check latency with 'Pong!'", inline=False)
    embed.add_field(name="!startserv", value="Start the Minecraft server.", inline=False)
    embed.add_field(name="!stopserv", value="Stop the Minecraft server.", inline=False)
    embed.add_field(name="!ip", value="Display the Minecraft server IP address.", inline=False)
    embed.add_field(name="!status", value="Display the Minecraft server status and additional information if the server is online.", inline=False)
    embed.add_field(name="!banana", value="Send a banana GIF by default, but can send up to 10 with '!banana 10'.", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ip(ctx):
    embed = discord.Embed(
        title="Minecraft Server IP Addresses",
        color=0xFFFF00
    )
    embed.add_field(name="Java Edition", value="Your_server_adresse", inline=False)
    embed.add_field(name="Bedrock Edition", value="Your_server_adresse", inline=False)
    embed.add_field(name="Port", value="Your_server_port", inline=False)
    await ctx.send(embed=embed)

@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down the bot...")
    await bot.close()

@bot.command()
async def banana(ctx, n: str = '1'):
    try:
        n = int(n)
        if n < 1:
            raise ValueError
    except ValueError:
        await ctx.send("Please enter a valid integer between 1 and 10.")
        return
    
    gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2lpN2MzMHVwdDZ3Y29tYjhsNjgxY2FqeHFldXU4cDA5ajdjOWJ4MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/IB9foBA4PVkKA/giphy.gif"
    
    for _ in range(min(n, 10)):
        await ctx.send(gif_url)

@bot.command()
async def info(ctx):
    server_address = "Your_server_adresse"
    try:
        server = JavaServer.lookup(server_address)
        status = server.status()
        
        player_samples = ', '.join([player.name for player in status.players.sample]) if status.players.sample else "No sampled players"
        
        latency = server.ping()
        
        embed = discord.Embed(
            title="Minecraft Server Information",
            color=0x00FF00
        )
        embed.add_field(name="Latency", value=f"{latency} ms", inline=False)
        embed.add_field(name="Players Online",
        value=f"{status.players.online}/{status.players.max}", inline=False)
        embed.add_field(name="Player Names (Sample)", value=player_samples, inline=False)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("The Minecraft server is currently offline or unreachable.")

if __name__ == '__main__':
    bot.run("YOUR_BOT_TOKEN_HERE")
