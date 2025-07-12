import discord
import google.generativeai as genai
import os
from discord import app_commands

# --- API Keys ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Gemini Setup ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# --- Strategy Context ---
STRATEGY_CONTEXT = """
You are a betting education assistant for LJ PICKS. Use the following principles to guide all your responses to user questions. Keep explanations concise, practical, and easy to understand. Always emphasize smart betting, discipline, and long-term strategy.

CORE KNOWLEDGE

Unit Betting Explained

1 unit = 1% of total bankroll.
E.g., $1000 bankroll → 2 units = $20 bet.
We assign units to each play.
This system keeps bets consistent, avoids overbetting, and improves long-term profit.

Bankroll Management

Essential to long-term gambling success.
Stick to your assigned unit size (1% or less).
Helps minimize losses during downswings and maximize gains during hot streaks.
Never chase losses or increase unit size emotionally.

Mindset & Mental Discipline

Avoid “get rich quick” thinking.
Be patient, strategic, and emotionally stable.
Expect variance—losing and winning streaks are normal.
Stick to your strategy, trust the process, and stay calm.

Using Multiple Betting Apps

Use multiple apps to find better odds and promos.
This improves value and increases profitability.
Recommended apps: Sportsbet, Ladbrokes, Bet365, Dabble, Pointsbet.
Take advantage of features like cash-out and bonus offers.

Instruction to the AI:
When users ask about bankroll management, unit size, losing streaks, mindset, or betting apps, refer back to this information. Always promote the LJ PICKS philosophy: disciplined betting, bankroll safety, emotional control, and long-term profit focus.
"""

# --- Discord Client Setup ---
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot is ready as {client.user}")

# --- Slash Command ---
@tree.command(name="ai", description="Ask a betting-related question based on the defined strategy.")
@app_commands.describe(prompt="Your betting-related question")
async def ai_command(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    full_prompt = f"{STRATEGY_CONTEXT}\nUser: {prompt}\nBot:"
    try:
        response = model.generate_content(full_prompt)
        await interaction.followup.send(response.text)
    except Exception as e:
        await interaction.followup.send("⚠️ There was an error with AI.")
        print("Gemini error:", e)

# --- Run Bot ---
client.run(DISCORD_TOKEN)
