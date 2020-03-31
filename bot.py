import discord
import api.corona_api as corona
import time
import sys
from discord.ext import commands
from discord.ext import tasks

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

# events
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("with Earth"))
    corona_count.start()
    print('Bot is ready')

# commands
@bot.command()
async def test(ctx, *args):
    await ctx.send(args)


@bot.command()
async def help(ctx):
    embed = discord.Embed(colour = discord.Colour.orange())
    embed.set_author(name="Help",
        icon_url='https://cdn.discordapp.com/attachments/489217124469047316/694464582860800000/e971f0968fccc139486620a523d2f832.png')

    embed.add_field(name='.corona', value='shows worldwide coronavirus stats', inline=False)
    embed.add_field(name='.corona <country>', value='shows <country> coronavirus stats', inline=False)
    embed.add_field(name='.ping', value='shows bot latency', inline=False)
    embed.set_footer(text='Stay the fuck at home.')
    await ctx.send(embed=embed)

@bot.command()
async def exit(ctx):
    await ctx.send('Shuting down...')
    await bot.logout()

@bot.command()
async def ping(ctx):
    await ctx.send(f"pong {round(bot.latency * 1000)}ms")

@bot.command(name='corona')
async def _corona(ctx, *args):
    country = ""
    if args:
        country = args[0]
        if not corona.does_country_exist(country):
            await ctx.send(f'Country \'{country}\' does not exist.')
            return
    
    await send_corona_embed(ctx.message.channel, country)

async def send_corona_embed(channel, country: str=""):
    corona_counter = corona.counter_from_country(country)

    region_display = country.capitalize() + '\'s' if country else ''

    embed = discord.Embed(colour = discord.Colour.blue())
    embed.add_field(name='Total Cases', value=corona_counter.cases)
    embed.add_field(name='Deaths', value=corona_counter.deaths)
    embed.add_field(name='Recovered', value=corona_counter.recovered)
    embed.set_footer(text=time.strftime("%X %d/%m/%Y") + '\nStay the fuck at home.')
    embed.set_author(name=f"{region_display} COVID-19 Cases",
        icon_url='https://cdn.discordapp.com/attachments/489217124469047316/694153156938170388/CORONAS-23.jpg')
    await channel.send(embed=embed)

# tasks
@tasks.loop(minutes=10)
async def corona_count():
    # link to corona api
    corona_counter = corona.counter_from_country()

    # change own status
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("with %s people" % corona_counter.cases))
    print('updating status')


bot.run('')