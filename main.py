import discord
from discord.ext import commands
from mcstatus import JavaServer
import subprocess
import asyncio

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"), help_command=None, intents=intents)
server = JavaServer.lookup("YOUR_SERVER_ADRESSE:PORT")

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
    await loading_message.edit(content="Démarrage du serveur Minecraft en cours...")
    loading_state = 0
    moon_emojis = ["□■■■", "■□■■", "■■□■", "■■■□"]  # Liste d'emojis de lune
    while True:
        try:
            if server.ping():
                break  # Sort de la boucle si le serveur répond
        except Exception:
            pass  # Ignore les exceptions de connexion pour continuer à essayer
        
        # Animation de chargement avec l'emoji de lune
        loading_content = f"Chargement en cours {moon_emojis[loading_state]}"
        await loading_message.edit(content=loading_content)
        loading_state = (loading_state + 1) % len(moon_emojis)  # Passage à l'emoji suivant
        await asyncio.sleep(1)  # Augmenter le délai à 1 seconde

    await loading_message.delete()
    await ctx.send("Le serveur Minecraft a été démarré avec succès!")

@bot.command()
async def startserv(ctx):
    loading_message = await ctx.send("Démarrage du serveur en cours...")
    try:
        status = server.status()
        await loading_message.edit(content="Le serveur Minecraft est déjà démarré.")
    except Exception as e:
        await start_server(ctx, loading_message)

@bot.command()
async def stopserv(ctx):
    subprocess.Popen(['pkill', '-f', 'java'])
    
    embed = discord.Embed(
        title="Arrêt du Serveur Minecraft",
        description="Le serveur Minecraft est éteind.",
        color=0xFF0000  # Rouge
    )
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1828/1828778.png")  # Image d'arrêt
    embed.set_footer(text=f"Commande exécutée par {ctx.author}", icon_url=ctx.author.avatar.url)
    
    await ctx.send(embed=embed)


@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Commandes disponibles :",
        description="Voici les commandes que vous pouvez utiliser avec ce bot :",
        color=0xFFFF00
    )
    embed.add_field(name="!ping", value="Renvoie 'Pong!' pour vérifier la latence.", inline=False)
    embed.add_field(name="!startserv", value="Démarre le serveur Minecraft.", inline=False)
    embed.add_field(name="!stopserv", value="Arrête le serveur Minecraft.", inline=False)
    embed.add_field(name="!ip", value="Affiche l'adresse IP du serveur Minecraft.", inline=False)
    embed.add_field(name="!status", value="Affiche le statut du serveur Minecraft et plus d'information si le serveur est en ligne.", inline=False)
    embed.add_field(name="!banana", value="Envoie par défaut un gif de banana mais peut en envoyer jusqu'à 10 !banana 10", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def ip(ctx):
    embed = discord.Embed(
        title="Adresses IP du Serveur Minecraft",
        color=0xFFFF00  # Couleur jaune
    )
    embed.add_field(name="Java Edition", value="YOUR_SERVER_ADRESSE:PORT", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def banana(ctx, n: str = '1'):
    try:
        n = int(n)
        if n < 1:
            raise ValueError
    except ValueError:
        await ctx.send("Veuillez entrer un nombre entier valide entre 1 et 10.")
        return
    
    gif_url = "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExb2lpN2MzMHVwdDZ3Y29tYjhsNjgxY2FqeHFldXU4cDA5ajdjOWJ4MSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/IB9foBA4PVkKA/giphy.gif"
    
    for _ in range(min(n, 10)):  # Limit to 10 GIFs
        await ctx.send(gif_url)


@bot.command()
async def status(ctx):
    server_address = "YOUR_SERVER_ADRESSE:PORT"
    try:
        server = JavaServer.lookup(server_address)
        status = server.status()
        
        # Sample player names (if available)
        player_samples = ', '.join([player.name for player in status.players.sample]) if status.players.sample else "Aucun joueur échantillonné"
        
        # Ping the server for latency
        latency = server.ping()
        
        # Embed message
        embed = discord.Embed(
            title="Informations sur le Serveur Minecraft",
            color=0x00FF00  # Couleur verte
        )
        embed.add_field(name="Latence", value=f"{latency} ms", inline=False)
        embed.add_field(name="Joueurs en ligne", value=f"{status.players.online}/{status.players.max}", inline=False)
        embed.add_field(name="Noms des joueurs (échantillon)", value=player_samples, inline=False)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send("Le serveur Minecraft est hors ligne ou inaccessible pour le moment.")


if __name__ == '__main__':
    bot.run("YOUR_BOT_TOKEN")

