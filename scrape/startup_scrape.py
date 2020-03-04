import requests
import json
def getCurrentStartup():
	startUp  = requests.get("https://techcrunch.com/wp-json/tc/v1/magazine?page=0&_embed=true&_envelope=true&categories=20429&cachePrevention=0").json()
	main = []
	for i in startUp['body']:
	    try:
	      href=(i['link'])
	      title = (i['title']['rendered'])
	      url = (i['_embedded']['wp:featuredmedia'][0]['media_details']['sizes']['medium_large']['source_url'])
	      main.append([title,href,url])
	    except:
	      pass
	return main