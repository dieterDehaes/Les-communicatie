import requests
from bs4 import BeautifulSoup
import re


def main():
	plaatsen_dict = {
		"haasrode": "http://www.meteo-info.be/nl/europa/belgie/weer-haasrode/details/N-2733974/",
		"leuven": "http://www.meteo-info.be/nl/europa/belgie/weer-leuven/details/N-2739976/",
		"oostende": "http://www.meteo-info.be/nl/europa/belgie/weer-oostende/details/N-2743704/",
	}

	te_kiezen_plaatsen = [plaats for plaats in plaatsen_dict]
	plaatsen_str = ', '.join(te_kiezen_plaatsen)

	gekozen_plaats = input('Typ een plaats: ' + plaatsen_str + ': ').lower()

	html = requests.get(plaatsen_dict[gekozen_plaats]).text[15100:17500]

	soup = BeautifulSoup(html, features="html.parser")

	div_text = soup.find("div", {"id": "weather-detail-summary"}).getText()

	search_str = 'Gem. wind: (.*) km/h\n.*Rel. luchtvochtigheid: (.*) %\n\n\n(.*)'
	m = re.search(search_str, div_text)

	print('Het weer in ' + gekozen_plaats + ':')
	print('Gemiddelde windsnelheid: ' + m.group(1) + ' km/h')
	print('Relatieve luchtvochtigheid: ' + m.group(2) + ' %')
	print('Temperatuur: ' + m.group(3))


if __name__ == "__main__":
	main()
