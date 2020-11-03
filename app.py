from flask import Flask, jsonify, make_response
import json
import sqlite3
import time
#from flask_cors import CORS



app = Flask(__name__)
app.config['DEBUG'] = True

databasePath = './database/database.sqlite3'



@app.route('/api/tickers/get_all_tickers_with_id')
def get_all_tickers():

	conn = sqlite3.connect(databasePath)
	c = conn.cursor()

	c.execute(''' SELECT DISTINCT ticker FROM priceHistory ''')
	data = c.fetchall()

	tick_id_json_array = []
	id = 100
	for tick in data:
		this_tick = tick[0]
		tick_id_json_array.append({'id': id, 'title': this_tick})
		id += 1

	return jsonify(tick_id_json_array)



@app.route('/api/get_latest_update_date')
def get_latest_update_date():
	conn = sqlite3.connect(databasePath)
	c = conn.cursor()
	c.execute(''' SELECT MAX(id), date_added FROM priceHistory ''')
	data = c.fetchone()
	return jsonify(data[1])



@app.route('/api/priceHistory/<ticker>', methods=['GET'])
def home(ticker):
	print(f'Request made for data on: {ticker}.')
	try:
		conn = sqlite3.connect('./database/database.sqlite3')
		c = conn.cursor()

		c.execute('''SELECT date, close, volume FROM priceHistory WHERE ticker = ? ''', (ticker.lower().strip(),))
		data = c.fetchall()

		conn.close()

		# Organizing data
		dates = []
		closes = []
		volumes = []

		for element in data:
			dates.append(element[0])
			closes.append(element[1])
			volumes.append(element[2])

		#time.sleep(2)

		return jsonify({"date": dates, "close": closes, "volume": volumes})

		'''
			str({
				"prices": [20,30,40,50],
				"dates": [2020-01-01, 2020-02-02],
				"volumes": [1000, 2000, 3000]
			})
		'''
	except Exception as e:
		return make_response(jsonify({'error': 'The request did not go through. ', 'Exception: ': e}), 404)

	#else:
	#	return make_response(jsonify({'error': 'Did not find the requested stock in database.'}), 404)

@app.route('/api/get_all_company_descriptions')
def get_all_descriptions():
	try:
		conn = sqlite3.connect('./database/database.sqlite3')
		c = conn.cursor()
		c.execute(''' SELECT ticker, description FROM companyDescription ''')
		data = c.fetchall()
		conn.close()

		#time.sleep(2)

		return jsonify(data)

	except Exception:
		pass













#CORS(app)




app.run()
