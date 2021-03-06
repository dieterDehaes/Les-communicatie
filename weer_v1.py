import discord
from discord.ext import commands
from random import randint
import requests
from bs4 import BeautifulSoup
import re
import datetime

print('Discord version:', discord.__version__)

prefix = '!'

with open('token_test_bot.txt', 'r') as file:
	token = file.readline()

bot = commands.Bot(command_prefix=prefix)

start_time = datetime.datetime.now()

@bot.event
async def on_ready():
	print('Bot is ready!')


@bot.command(pass_context=True)
async def weer(ctx, *, msg=None):
	'''Toont het weerbericht'''

	plaatsen_dict = {
		"haasrode": "http://www.meteo-info.be/nl/europa/belgie/weer-haasrode/details/N-2733974/",
		"leuven": "http://www.meteo-info.be/nl/europa/belgie/weer-leuven/details/N-2739976/",
		"oostende": "http://www.meteo-info.be/nl/europa/belgie/weer-oostende/details/N-2743704/",
	}

	te_kiezen_plaatsen = [plaats for plaats in plaatsen_dict]

	if msg not in te_kiezen_plaatsen:
		plaatsen_str = ' | '.join(te_kiezen_plaatsen)
		await bot.say('Gebruik: `!weer { ' + plaatsen_str + ' }`')

	else:
		bezig = await bot.say('Bezig...')

		html = requests.get(plaatsen_dict[msg]).text[15100:17500]

		soup = BeautifulSoup(html, features="html.parser")
		div_text = soup.find("div", {"id": "weather-detail-summary"}).getText()

		search_str = 'Gem. wind: (.*) km/h\n.*Rel. luchtvochtigheid: (.*) %\n\n\n(.*)'
		m = re.search(search_str, div_text)

		windsnelheid, luchtvochtigheid, temperatuur = m.group(1), m.group(2), m.group(3)

		embed = discord.Embed(title='Weerbericht',
							  color=randint(0, 0xffffff),
							  description='Het weer in ' + msg)
		# color=discord.Color.green()

		embed.set_author(name=bot.user.name, icon_url=bot.user.avatar_url)

		msg_author = ctx.message.author

		avatar_url = msg_author.avatar_url
		if not avatar_url:
			avatar_url = msg_author.default_avatar_url
		embed.set_thumbnail(url=avatar_url)

		embed.add_field(name='Gemiddelde windsnelheid', value=windsnelheid + ' km/h', inline=False)
		embed.add_field(name='Relatieve luchtvochtigheid', value=luchtvochtigheid + ' %', inline=False)
		embed.add_field(name='Temperatuur', value=temperatuur, inline=False)
		embed.add_field(name='Tijd', value=str(datetime.datetime.now().replace(microsecond=0)), inline=False)

		embed.set_footer(text='Gevraagd door ' + msg_author.display_name)

		await bot.delete_message(bezig)
		await bot.say(embed=embed)
		await bot.send_message(msg_author, embed=embed)


@bot.command()
async def uptime():
	await bot.say('Uptime: ' + str(datetime.datetime.now().replace(microsecond=0) - start_time.replace(microsecond=0)))


bot.run(token)
