import discord
from dotenv import dotenv_values
from discord import app_commands
from discord.ext import commands

token = dotenv_values(".env")["TOKEN"]
guild_id = dotenv_values(".env")["GUILD"]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='.', intents=intents)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Guilds: {bot.guilds[0].id}')
    await bot.tree.sync(guild=discord.Object(guild_id))
@bot.event
async def on_message(message):
    await bot.process_commands(message)
    print(message.content)

@bot.tree.command(name='generatebackground', description = "Generate a background for your dnd character", guild=discord.Object(guild_id))
async def generatebackground(interaction: discord.Interaction):
    await interaction.response.send_message("Hello World")


bot.run(token)
