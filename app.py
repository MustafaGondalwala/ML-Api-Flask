
from flask import Flask,render_template,request
import MySQLdb

from scrape import harvard_scrape as h_scrape
from scrape import techcrunch_scrape as t_scrape
from scrape import topheadline_scrape as top_scrape
from scrape import startup_scrape as s_scrape

import datetime
from datetime import datetime as current_time
from flask import jsonify
from flask_cors import CORS, cross_origin



app = Flask(__name__)
cors = CORS(app)

@app.route("/<page_type>")
def hello(page_type="all"):
    return render_template('home.html')

@app.route("/")
def hello2():
	return "ok";


@app.route("/scrape/<type>")
def hello3(type="all"):
	try:
		c, conn = connection()
	except Exception as e:
		return str(e)
	if(type=="harvard"):
		store = h_scrape.getCurrentHarvard()
	elif(type=="techcrunch"):
		store = t_scrape.getCurrentTechcrush()
	elif(type=="startup"):
		store = s_scrape.getCurrentStartup()
	elif(type=="top10"):
		store = top_scrape.getCurrentTopHeadline()
	else:
		return "Sorry Not Found";
	for i in store:
		try:
			c.execute("INSERT INTO `quicknews`.`coreapi_news` (`type`, `title`, `link`, `image_link`, `created_date`) VALUES ('"+type+"', '"+(i[0])+"', '"+i[1]+"', '"+i[2]+"', '"+str(current_time.now())+"')")
		except:
			pass
	conn.commit()
	return str(store);

@app.route("/scrape")
def hello4(type="all"):
	hello3("harvard")
	hello3("techcrunch")
	hello3("top10")
	return "Done"

def connection():
    conn = MySQLdb.connect(host="mustafa-db.cyptmcja8bd2.us-east-2.rds.amazonaws.com",
                           user = "mustafa",
                           passwd = "mustafas1",
                           db = "quicknews")
    c = conn.cursor()

    return c, conn


@app.route('/get/<type>')
def hello5(type,justNews=False):
	try:
		c, conn = connection()
	except Exception as e:
		return str(e)
	l = ['harvard','startup','techcrunch','top10']
	if(type not in l):
		return jsonify([]);
	c.execute("select * from quicknews.coreapi_news where type='"+type+"' order by created_date DESC LIMIT 10;")
	records = c.fetchall()
	news = []
	for i in records:
		item = {
					'title':i[2],
					'url':i[3],
					'urlToImage':i[4],
					'created_date':i[5]
				}
		news.append(item)
	if(justNews==True):
		return news;
	context = {
		'items': news,
		'length': len(news),
		'type':type
	}	
	return jsonify(context)



@app.route('/get')
def hello6():
	news = []
	news.extend(hello5("harvard",justNews=True))
	news.extend(hello5("startup",justNews=True))
	news.extend(hello5("techcrunch",justNews=True))
	context = {
		'items': news,
		'length': len(news),
		'type':"all"
	}	
	return jsonify(context)

if __name__ == "__main__":
	print("Running")
	app.run(debug=True)