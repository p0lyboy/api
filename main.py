import nextcord
from nextcord.ext import commands
import sqlite3
import random
import string
import datetime
from concurrent.futures import ThreadPoolExecutor
import requests
from random import choice

intents = nextcord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

ignored_channels = [1181668184835756173, 1181668789159473154, 1181668554555281418, 1181896542802694204, 1181935007158247485, 1181932720700526694, 1181932287139528724]

conn = sqlite3.connect('license.db')

c = conn.cursor()

c.execute("""
    CREATE TABLE IF NOT EXISTS licenses (
        id INTEGER PRIMARY KEY,
        type TEXT,
        user_id INTEGER,
        views INTEGER
    )
""")

conn.commit()

num_threads = 500

OWNER_IDS = {1153690327274750022, 2345678901}
    
@bot.command()
async def generatelicense(ctx, license_type, num_keys: int, member: nextcord.Member):
    try:
        if ctx.author.id in OWNER_IDS:
            if license_type in ['beta', 'sigma', 'doom', 'doom+']:
                views = {'beta': 35000, 'sigma': 150000, 'doom': 750000, 'doom+': 1500000}[license_type]
                licenses = []
                for _ in range(num_keys):
                    license_key = 'DOOM-' + '-'.join(''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(3))
                    c.execute("INSERT INTO licenses (type, user_id, views, key) VALUES (?, ?, ?, ?)", (license_type, member.id, views, license_key))
                    embed.set_image(url="https://cdn.discordapp.com/attachments/1157441314007302255/1181891071253430272/standard_3.gif?ex=6582b4d5&is=65703fd5&hm=c7e6adb915e8b46d9b3cfa749723bd1219125fcd385414ac1555e20690ca8faa&")
                    licenses.append(f"License Key: {license_key}, Views: {views}")
                conn.commit()
                embed = nextcord.Embed(title="**DoomGen™ - License System**", description="", color=0xFF006C)
                embed.add_field(name="**LICENSES GENERATED!**", value="\n".join(licenses), inline=False)
                embed.set_image(url="https://cdn.discordapp.com/attachments/1157441314007302255/1181891071253430272/standard_3.gif?ex=6582b4d5&is=65703fd5&hm=c7e6adb915e8b46d9b3cfa749723bd1219125fcd385414ac1555e20690ca8faa&")
                embed.set_footer(text="2023 © DoomGen™, LLC. All rights reserved.")
                await ctx.author.send(embed=embed)
    except commands.BadArgument:
        embed = nextcord.Embed(title="**DoomGen™ - License System**", description="", color=0xFF006C)
        embed.add_field(name="**ERROR!**", value="Invalid argument.", inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1157441314007302255/1181891071253430272/standard_3.gif?ex=6582b4d5&is=65703fd5&hm=c7e6adb915e8b46d9b3cfa749723bd1219125fcd385414ac1555e20690ca8faa&")
        embed.set_footer(text="2023 © DoomGen™, LLC. All rights reserved.")
        await ctx.author.send(embed=embed)

@bot.command()
async def checklicense(ctx):
    license = c.execute("SELECT * FROM licenses WHERE user_id=?", (ctx.author.id,)).fetchone()
    if license is not None:
        embed = nextcord.Embed(title="**DoomGen™ - License System**", description="", color=0xFF006C)
        embed.add_field(name="**YOU HAVE A {license[1]} LICENSE WITH {license[3]} VIEWS REMAINING!**", value="", inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1157441314007302255/1181891071253430272/standard_3.gif?ex=6582b4d5&is=65703fd5&hm=c7e6adb915e8b46d9b3cfa749723bd1219125fcd385414ac1555e20690ca8faa&")
        embed.set_footer(text="2023 © DoomGen™, LLC. All rights reserved.")
    else:
        embed = nextcord.Embed(title="**DoomGen™ - License System**", description="", color=0xFF006C)
        embed.add_field(name="**NO LICENSE!**", value="", inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1157441314007302255/1181891071253430272/standard_3.gif?ex=6582b4d5&is=65703fd5&hm=c7e6adb915e8b46d9b3cfa749723bd1219125fcd385414ac1555e20690ca8faa&")
        embed.set_footer(text="2023 © DoomGen™, LLC. All rights reserved.")
        
@bot.command()
async def help(ctx):
    license = c.execute("SELECT * FROM licenses WHERE user_id=?", (ctx.author.id,)).fetchone()
    if license is not None:
        embed = nextcord.Embed(title="**DoomGen™ - Help**", description="", color=0xFF006C)

        embed.add_field(name="*Generation*", value="```\n!generate <method> <url> <amount>\n```", inline=False)

        embed.add_field(name="*Methods*", value="```\n!methods\n```", inline=False)

        embed.add_field(name="*Usage*", value="```\n!usage>\n```", inline=False)
    
        embed.add_field(name="*Admin*", value="```\n!generatelicense <type> <amount> <user>\n```", inline=False)
        
        embed.set_image(url="https://cdn.discordapp.com/attachments/1157441314007302255/1181891071253430272/standard_3.gif?ex=6582b4d5&is=65703fd5&hm=c7e6adb915e8b46d9b3cfa749723bd1219125fcd385414ac1555e20690ca8faa&")
    
        embed.set_footer(text="2023 © DoomGen™, LLC. All rights reserved.")

        await ctx.author.send(embed=embed)
    
    else:
        embed = nextcord.Embed(title="**DoomGen™ - License System**", description="", color=0xFF006C)
        embed.add_field(name="**ERROR!**", value="You do not have a license.", inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1157441314007302255/1181891071253430272/standard_3.gif?ex=6582b4d5&is=65703fd5&hm=c7e6adb915e8b46d9b3cfa749723bd1219125fcd385414ac1555e20690ca8faa&")
        embed.set_footer(text="2023 © DoomGen™, LLC. All rights reserved.")
        await ctx.author.send(embed=embed)
        
@bot.command()
async def methods(ctx):
    license = c.execute("SELECT * FROM licenses WHERE user_id=?", (ctx.author.id,)).fetchone()
    if license is not None:
        embed = nextcord.Embed(title="**DoomGen™ - Methods**", description="", color=0xFF006C)

        embed.add_field(name="*Youtube*", value="```\nyoutube\n```", inline=False)

        embed.add_field(name="*Spotify*", value="```\nspotify\n```", inline=False)

        embed.add_field(name="*Tiktok*", value="```\ntiktok\n```", inline=False)
    
        embed.add_field(name="*Deezer*", value="```\ndeezer\n```", inline=False)
        
        embed.set_image(url="https://cdn.discordapp.com/attachments/1157441314007302255/1181891071253430272/standard_3.gif?ex=6582b4d5&is=65703fd5&hm=c7e6adb915e8b46d9b3cfa749723bd1219125fcd385414ac1555e20690ca8faa&")
    
        embed.set_footer(text="2023 © DoomGen™, LLC. All rights reserved.")

        await ctx.author.send(embed=embed)
    
    else:
        embed = nextcord.Embed(title="**DoomGen™ - License System**", description="", color=0xFF006C)
        embed.add_field(name="**ERROR!**", value="You do not have a license.", inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1157441314007302255/1181891071253430272/standard_3.gif?ex=6582b4d5&is=65703fd5&hm=c7e6adb915e8b46d9b3cfa749723bd1219125fcd385414ac1555e20690ca8faa&")
        embed.set_footer(text="2023 © DoomGen™, LLC. All rights reserved.")
        await ctx.author.send(embed=embed)
        
@bot.command()
async def usage(ctx):
    license = c.execute("SELECT * FROM licenses WHERE user_id=?", (ctx.author.id,)).fetchone()
    if license is not None:
        if ctx.author.id in OWNER_IDS:
            views = "Unlimited"
            time_left = "Unlimited"
        else:
            views = license[3]  # Get the number of views from the license
            expiration_date = datetime.datetime.now() + datetime.timedelta(days=7)  # Set the expiration date to 7 days from now
            time_left = expiration_date - datetime.datetime.now()  # Calculate the time left
        
        embed = nextcord.Embed(title="**DoomGen™ - Usage**", description="", color=0xFF006C)
        embed.add_field(name="Views", value=str(views), inline=False)
        embed.add_field(name="Time Left", value=str(time_left), inline=False)
        
        embed.set_image(url="https://cdn.discordapp.com/attachments/1157441314007302255/1181891071253430272/standard_3.gif?ex=6582b4d5&is=65703fd5&hm=c7e6adb915e8b46d9b3cfa749723bd1219125fcd385414ac1555e20690ca8faa&")
        embed.set_footer(text="2023 © DoomGen™, LLC. All rights reserved.")

        await ctx.author.send(embed=embed)
    
    else:
        embed = nextcord.Embed(title="**DoomGen™ - License System**", description="", color=0xFF006C)
        embed.add_field(name="**ERROR!**", value="You do not have a license.", inline=False)
        embed.set_image(url="https://cdn.discordapp.com/attachments/1157441314007302255/1181891071253430272/standard_3.gif?ex=6582b4d5&is=65703fd5&hm=c7e6adb915e8b46d9b3cfa749723bd1219125fcd385414ac1555e20690ca8faa&")
        embed.set_footer(text="2023 © DoomGen™, LLC. All rights reserved.")
        await ctx.author.send(embed=embed)
        
# Load user-agents and proxies from files
with open('useragents.txt', 'r') as f:
    user_agents = f.read().splitlines()

with open('proxies.txt', 'r') as f:
    proxies = f.read().splitlines()

def visit_url(url, user_agent, proxy):
    headers = {'User-Agent': user_agent}
    proxy_dict = {'http': proxy, 'https': proxy}
    try:
        response = requests.get(url, headers=headers, proxies=proxy_dict)
        print(f"Visited {url} with status {response.status_code}")
    except Exception as e:
        print(f"Error visiting {url}: {e}")

                
@bot.command()
async def generate(ctx, url: str, amount: int):
    # Check if the user has a license
    license = c.execute("SELECT * FROM licenses WHERE user_id=?", (ctx.author.id,)).fetchone()
    if license is not None:
        # Check the license type and set the max amount
        license_type = license[1]  # Get the license type from the license
        if license_type == 'beta':
            max_amount = 35000
        elif license_type == 'sigma':
            max_amount = 150000
        elif license_type == 'doom':
            max_amount = 750000
        elif license_type == 'doom+':
            max_amount = 15000000
        else:
         embed = nextcord.Embed(title="**DoomGen™ - Generation System**", description="", color=0xFF006C)
         embed.add_field(name="**ERROR!**", value="You do not have a license.", inline=False)
         embed.set_footer(text="2023 © DoomGen™, LLC. All rights reserved.")
         await ctx.author.send(embed=embed)
        return

        # Limit the amount to the max amount
        if amount > max_amount:
            amount = max_amount

        # Start the threads
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for _ in range(amount):
                user_agent = choice(user_agents)
                proxy = choice(proxies)
                executor.submit(visit_url, url, user_agent, proxy)


        embed = nextcord.Embed(title="**DoomGen™ - Generation System**", description="", color=0xFF006C)
        embed.add_field(name="**SUCCESS!**", value="Started visiting {url} {amount} times.", inline=False)
        embed.set_footer(text="2023 © DoomGen™, LLC. All rights reserved.")
        await ctx.author.send(embed=embed)
    else:
        # Send an error message to the user
        embed = nextcord.Embed(title="**DoomGen™ - License System**", description="", color=0xFF006C)
        embed.add_field(name="**ERROR!**", value="You do not have a license.", inline=False)
        embed.set_footer(text="2023 © DoomGen™, LLC. All rights reserved.")
        await ctx.author.send(embed=embed)

bot.run('MTE4MDkyNjE5OTAxOTYxNDIyOQ.GAl6VF._zGXY_cXx-yIeGkff2CLXOuvI91T_nbBKbaWOQ')
