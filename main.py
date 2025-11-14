import os
import random
import discord
from upstash_redis import Redis
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

redis = Redis.from_env()
if redis.ping() == "PONG":
        print("Redis is running!", flush=True)

@bot.tree.command(name="click", description="Get 1 point")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@discord.app_commands.allowed_installs(guilds=True, users=True)
async def click(interaction: discord.Interaction):
    points = redis.get(str(interaction.user.id))
    if (points == None):
        points = 0
        
    redis.set(str(interaction.user.id), str(int(points) + 1))

    await interaction.response.send_message(f"Click! You now have {str(int(points) + 1)} points!", ephemeral=True)

@bot.tree.command(name="minus_one_point", description="Why does this exist? The real question is why should it NOT exist?")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@discord.app_commands.allowed_installs(guilds=True, users=True)
async def minus_one_point(interaction: discord.Interaction):
    points = redis.get(str(interaction.user.id))
    if (points == None):
        points = -1
        
    redis.set(str(interaction.user.id), str(int(points) - 1))

    await interaction.response.send_message(f"You clicked the -1 point button! You now have {str(int(points) - 1)} points!", ephemeral=True)


@bot.tree.command(name="reset_points", description="Set your points to 0")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@discord.app_commands.allowed_installs(guilds=True, users=True)
async def reset_points(interaction: discord.Interaction):
    redis.delete(str(interaction.user.id))
    await interaction.response.send_message(f"You deleted your points :( why", ephemeral=True)


prefixes = ["", "Wow!", "Amazing!", "How?", "no."]
suffixes = ["", "I didn't know it was possible!", "That's crazy!", "That's crazy! Crazy? I was crazy once? They locked me in a room. A Ronny room. A Ronny room with Ronnyies (and rats). Ronnies? Ronnies make me ok im not typing more of this", "This user should probably touch grass...", "This user should DEFINITELY touch grass!", "pretty cool i guess.", "67 mustard mangos hahahaha", "If you think this is fun, try the real game on Steam! no this isnt an ad this is a joke obviously *nervous laugh*", "jk this user only has negative one because he's bad at video games :("]

@bot.tree.command(name="brag", description="Publicly show how many points you have")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@discord.app_commands.allowed_installs(guilds=True, users=True)
async def brag(interaction: discord.Interaction):
    points = redis.get(str(interaction.user.id))
    if (points == None):
        await interaction.response.send_message(f"lmao {interaction.user.mention} has 0 points and decided to show it off why", ephemeral=False)
    else:
        await interaction.response.send_message(f"{random.choice(prefixes)} {interaction.user.mention} has {points} points! {random.choice(suffixes)}", ephemeral=False)


@bot.tree.command(name="admin_abuse", description="Publicly show how many points you have... to @everyone")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@discord.app_commands.allowed_installs(guilds=True, users=True)
async def admin_abuse(interaction: discord.Interaction):
    if interaction.guild is None or interaction.permissions.mention_everyone:
        points = redis.get(str(interaction.user.id))
        if (points == None):
            await interaction.response.send_message(f"lmao {interaction.user.mention} has 0 points and decided to show it off to @everyone why", ephemeral=False)
        else:
            await interaction.response.send_message(f"{random.choice(prefixes)} {interaction.user.mention} has {points} points and decided to show it off to @everyone! {random.choice(suffixes)}", ephemeral=False, allowed_mentions=discord.AllowedMentions(everyone=True))
    else:
        await interaction.response.send_message(f"Yeah sorry no you're not an admin", ephemeral=True)


@bot.tree.command(name="points_of", description="Find the points of a specific player")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@discord.app_commands.allowed_installs(guilds=True, users=True)
async def points_of(interaction: discord.Interaction, user: discord.User):
    try:
        fetched_user = await bot.fetch_user(user.id)
    except:
        fetched_user = None
    if fetched_user != None:
        points = redis.get(str(user.id))
        if (points == None):
            await interaction.response.send_message(f"{fetched_user.display_name} has no points. Get them to start playing!", ephemeral=True)
        else:
            await interaction.response.send_message(f"{fetched_user.display_name} has {points} points.", ephemeral=True)
    else:
        await interaction.response.send_message(f"Not a valid user!", ephemeral=True)
        return
    
@bot.event
async def on_ready():
    await bot.tree.sync()
    print("The bot is logged in and ready!", flush=True)

bot.run(str(os.environ.get("DISCORD_BOT_TOKEN")))
