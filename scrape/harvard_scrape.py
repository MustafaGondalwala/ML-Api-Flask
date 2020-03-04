import requests
import json


def getCurrentHarvard():
	lastest = requests.get("https://hbr.org/service/components/external-list/latest/0/8?format=json&id=page.external-list.the-latest").json()

	main = []
	for i in lastest['entry']:
	  href = "https://hbr.org"+i['link']['href']
	  image = "https://hbr.org"+i['content']['image']
	  title = i['title']
	  main.append([title,href,image])

	popular = requests.get("https://hbr.org/service/components/search-list/popular-content/0/8?format=json&id=page.search-list.most-popular").json()
	for i in popular['entry']:
	  href = "https://hbr.org"+i['link']['href']
	  image = "https://hbr.org"+i['content']['image']
	  title = i['title']
	  main.append([title,href,image])
	return main