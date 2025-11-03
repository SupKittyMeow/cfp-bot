import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
import json

try:
    with open('data.json', 'r') as fp:
        data: dict = json.load(fp)

except IOError:
    print('Data not found, will create a new one.')
    data: dict = {}

load_dotenv()
token = str(os.environ.get("DISCORD_BOT_TOKEN"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

@bot.tree.command(name="click", description="Get 1 point")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@discord.app_commands.allowed_installs(guilds=True, users=True)
async def click(interaction: discord.Interaction):
    data.update({str(interaction.user.id): data.get(str(interaction.user.id), 0) + 1})
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    await interaction.response.send_message(f"Click! You now have {data.get(str(interaction.user.id), 0)} points!", ephemeral=True)

@bot.tree.command(name="reset_points", description="Set your points to 0")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@discord.app_commands.allowed_installs(guilds=True, users=True)
async def reset_points(interaction: discord.Interaction):
    del data[str(interaction.user.id)]
    await interaction.response.send_message(f"You deleted your points :( why", ephemeral=True)


prefixes = ["", "Wow!", "Amazing!", "How?", "no."]
suffixes = ["", "I didn't know it was possible!", "That's crazy!", "This user should probably touch grass...", "This user should DEFINITELY touch grass!", "pretty cool i guess.", "67 mustard mangos hahahaha", "If you think this is fun, try the real game on Steam! (https://store.steampowered.com/app/2159370/Click_For_Points/) also yes this is an ad in my cfp bot", "jk this user only has -1 because he's bad at video games :("]

@bot.tree.command(name="show_off", description="Publicly show how many points you have")
@discord.app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)
@discord.app_commands.allowed_installs(guilds=True, users=True)
async def show_off(interaction: discord.Interaction):
    await interaction.response.send_message(f"{random.choice(prefixes)} {interaction.user.mention} has {data.get(str(interaction.user.id), 0)} points! {random.choice(suffixes)}", ephemeral=False)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("The bot is logged in and ready!")

bot.run(token)