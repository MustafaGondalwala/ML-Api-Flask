import requests
import json
from bs4 import BeautifulSoup
def getCurrentTopHeadline():
	r = requests.get("https://economictimes.indiatimes.com/headlines.cms")
	soup = BeautifulSoup(r.content)
	main = []
	headline = soup.find('ul',attrs={"itemscope":"itemscope"})
	atag = headline.findAll('a')
	for i in atag:
	  main.append([i.text,"https://economictimes.indiatimes.com"+i['href'],""])
	return main