import discord
from dotenv import dotenv_values
from discord.ext import commands
from discord import app_commands
from gpt_client import GPTClient
import asyncio


token = dotenv_values(".env")["TOKEN"]
guild_id = dotenv_values(".env")["GUILD"]
openai_key = dotenv_values('.env')["OPENAI_API_KEY"]
gpt_client = GPTClient(openai_key)

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

@bot.tree.command(name='generatestory',
                  description = "Generate a background story for your DnD character.",
                  guild=discord.Object(guild_id))
@app_commands.describe(character_name="What's your character's name?")
@app_commands.describe(race="ex. Dwarf, Dragonborn, Human, etc")
@app_commands.describe(char_class="ex. Barbarian, Bard, Cleric, etc.")
@app_commands.describe(background="ex. Noble, Soldier, Urchin, etc.")
@app_commands.describe(appearance="ex. Tall, muscular, short black hair, stern blue eyes, rugged beard, worn leather armor.")
@app_commands.describe(alignment="ex. Lawful Good, True Neutral, Chaotic Evil, etc.")
@app_commands.describe(personality_traits="(use 'and' to include two personality traits) ex. Curious, Cheerful and Cautious, Sarcastic, etc.")
@app_commands.describe(ideals='ex. Justice (Believes in fairness and law), Knowledge (Seeks to discover and learn as much as possible), etc.')
@app_commands.describe(bonds="(use 'and' to include more than one bond) ex. Family and Comrades (Cherishes loyalty to family and the bonds formed with friends), Mentor (Feels a debt to a benefactor, mentor, or organization), etc.")
@app_commands.describe(flaws='ex. Greedy (Overly possessive or desirous of wealth or possessions), Fearful (Possesses a deep-seated fear or phobia), etc.')
async def generatestory(interaction: discord.Interaction,
                        character_name: str,
                        race: str,
                        char_class: str,
                        background: str,
                        appearance: str = None,
                        alignment: str = None,
                        personality_traits: str = None,
                        ideals: str = None,
                        bonds: str = None,
                        flaws: str = None):
    await interaction.response.defer()

    # Get the current event loop
    loop = asyncio.get_event_loop()

    # Run the GPT-3 call in a separate thread to avoid blocking the event loop
    character_story = await loop.run_in_executor(None, lambda: gpt_client.create_character_story(character_name, race, char_class, background, appearance,
                                                              alignment, personality_traits, ideals, bonds, flaws))

    # await interaction.response.send_message(character_story)
    await interaction.followup.send(content=character_story)


bot.run(token)
