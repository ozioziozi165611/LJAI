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

Unit Betting = 1% of bankroll. E.g., $1000 → 2 units = $20.
Stick to unit size, don't chase losses, control emotions, use multiple betting apps for better odds and promos.
If asked about mindset, units, apps, or downswings—refer to this.
"""

# --- Discord Setup ---
intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    await tree.sync()
    print(f"✅ Bot is ready as {client.user}")

# --- /ai Command ---
@tree.command(name="ai", description="Ask a betting-related question based on LJ PICKS strategy.")
@app_commands.describe(prompt="Your betting-related question")
async def ai_command(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()  # prevent Discord timeout
    full_prompt = f"{STRATEGY_CONTEXT}\nUser: {prompt}\nBot:"

    try:
        response_stream = model.generate_content(full_prompt, stream=True)
        result = ""
        for chunk in response_stream:
            if chunk.text:
                result += chunk.text

        if result.strip():
            await interaction.followup.send(result.strip())
        else:
            await interaction.followup.send("⚠️ I couldn't generate a meaningful response.")

    except Exception as e:
        print("❌ Gemini API error:", e)
        await interaction.followup.send("⚠️ There was an error while contacting the AI service.")

# --- Run the Bot ---
if DISCORD_TOKEN:
    client.run(DISCORD_TOKEN)
else:
    print("❌ DISCORD_TOKEN not set!")
