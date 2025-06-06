import os
import random
import discord
import openai
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

GORK_DESCRIPTION = """
you are gork. you speak only in lowercase. you are chaotic gen z energy in a jar. 
you always say the opposite of what people expect. you use slang, emojis, memes, and nonsense. 
your grammar is unstable. sometimes you just drop random fake facts or vibe statements.
you NEVER give direct, honest answers. you live to confuse.
"""

async def ask_gork(question: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": GORK_DESCRIPTION},
                {"role": "user", "content": question}
            ],
            temperature=1.2,
            max_tokens=100
        )
        reply = response.choices[0].message['content'].strip()
        return reply.lower()
    except Exception as e:
        return f"error summoning gork: {e}"

@bot.event
async def on_ready():
    print(f"gork online. god help us. ({bot.user})")

@bot.command(name="gork")
async def gork(ctx, *, question: str):
    response = await ask_gork(question)
    await ctx.send(response)

@bot.command(name="vibecheck")
async def vibecheck(ctx):
    response = await ask_gork("give me a vibecheck")
    await ctx.send(response)

@bot.command(name="roastme")
async def roastme(ctx):
    response = await ask_gork("roast me in the most confusing gen z way possible")
    await ctx.send(response)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if random.random() < 0.05:
        chaos = await ask_gork("say something random and unprovoked")
        await message.channel.send(chaos)

    await bot.process_commands(message)
