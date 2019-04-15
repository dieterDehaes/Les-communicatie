from bs4 import BeautifulSoup
import re


def main():
	plaatsen_list = ['haasrode', 'leuven', 'oostende']
	plaatsen_str = ', '.join(plaatsen_list)

	gekozen_plaats = input('Typ een plaats: ' + plaatsen_str + ': ')

	with open(gekozen_plaats + '.html', 'r') as file:
		html = file.read()

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
