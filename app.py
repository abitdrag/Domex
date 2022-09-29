from flask import Flask, render_template, request, redirect, jsonify, url_for, session
import dbmanager
import models
import sqlite3
import dnshelper
from datetime import datetime
import json

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'This is a secret key selected by me'

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	print("I have been called!!! yay!!")
	if request.method == 'GET':
		return render_template('index.html')
	else:
		# fetch the url and process it
		post_data = request.json
		print('search-url: ' + str(post_data))
		url = post_data['search_url']
		domain_details = dnshelper.make_whois_query(url)
		print(type(domain_details))
		print(domain_details)
		try:
			expiry_date = domain_details.expiration_date[0].strftime("%d %B, %Y")
		except Exception as e:
			expiry_date = domain_details.expiration_date.strftime("%d %B, %Y")
		return jsonify(
			url=str(post_data['search_url']),
			expiry_date=expiry_date,
		)

@app.route('/about', methods=['GET', 'POST'])
def about():
	return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
	return render_template('contact.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	return render_template('colorlib-regform-7/signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('Login_v1/login.html')
	else:
		# fetch the userid and password
		post_data = request.form
		print('username: ' + str(post_data))
		email = request.form.get('email')
		password = request.form.get('pass')
		print(email, password)
		userid, isadmin = dbmanager.check_login(email, password)
		session["userid"] = userid
		session["isadmin"] = isadmin
		if(isadmin == 0):
			# redirect to user dashboard
			return redirect(url_for('dashboard'))
		else:
			# redirect to admin dashboard
			return redirect(url_for('admindashboard'))

@app.route('/admindashboard', methods=['GET', 'POST'])
def admindashboard():
	if 'userid' in session:
		userid = session["userid"]
	if 'isadmin' in session:
		isadmin = session["isadmin"]
	return render_template('material-dashboard-master/examples/admindashboard.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
	if 'userid' in session:
		del session["userid"]
	if 'isadmin' in session:
		del session["isadmin"]
	return redirect(url_for('index'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
	if request.method == 'GET':
		if 'userid' in session:
			userid = session["userid"]
			print(userid)
		else:
			return redirect(url_for('login'))
		if 'isadmin' in session:
			isadmin = session["isadmin"]
		return render_template('material-dashboard-master/examples/dashboard.html')
	else:
		if 'userid' in session:
			userid = session["userid"]
			# print(userid)
		else:
			return redirect(url_for('login'))
		if 'isadmin' in session:
			isadmin = session["isadmin"]
		# fetch the url and process it
		post_data = request.json
		if(post_data['request_type'] == 'search_click'):
			print('search-url: ' + str(post_data))
			url = post_data['search_url']
			domain_details = dnshelper.make_whois_query(url)
			print(domain_details)
			try:
				try:
					expiry_date = domain_details.expiration_date[0].strftime("%d %B, %Y")
				except:
					expiry_date = domain_details.expiration_date.strftime("%d %B, %Y")
				# find url related information
				url_obj = models.Urls(None, url, expiry_date)
				urlid = dbmanager.get_and_add_url(url_obj)
				usersearchhistory_obj = models.SearchHistory(urlid, userid, 0, datetime.now(), 1) # left from here
				dbmanager.add_new_search_history(usersearchhistory_obj)
				# return result expiry date
				return jsonify(
					url=str(url),
					expiry_date=expiry_date,
				)
			except Exception as e:
				print(e)
				return jsonify(
					url="Not found!",
					expiry_date="Error. Please try again!",
				)
		elif(post_data['request_type'] == 'history_watchlist_request'):
			print("python got it")
			histories = []
			watchlist = []
			urlid_histories = []
			urlid_watchlist = []
			is_in_watch_list = []
			search_histories = dbmanager.get_search_history(userid)
			for row in search_histories:
				if row[1] == 1:
					if(row[0] not in watchlist):
						watchlist.append(row[0])
						urlid_watchlist.append(row[2])
					if(row[0] not in histories):
						histories.append(row[0])
						urlid_histories.append(row[2])
						is_in_watch_list.append(1)           
				else:
					if(row[0] not in histories):
						histories.append(row[0])
						urlid_histories.append(row[2])
						is_in_watch_list.append(0)
			# print("returning " + str(histories))
			return jsonify(
					histories=histories,
					watchlist=watchlist,
					urlid_histories=urlid_histories,
					urlid_watchlist=urlid_watchlist,
					is_in_watch_list=is_in_watch_list,
				)
		elif(post_data['request_type'] == 'changing_watch_list'):
			urlid = post_data['urlid']
			watching = post_data['action']
			search_history_obj = models.SearchHistory(urlid, userid, watching, None, None)
			dbmanager.update_url_watching_status(search_history_obj)
			return jsonify(
				action='done'
			)

@app.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
	if request.method == 'GET':
		if 'userid' in session:
			userid = session["userid"]
			print(userid)
		else:
			return redirect(url_for('login'))
		if 'isadmin' in session:
			isadmin = session["isadmin"]
		return render_template('material-dashboard-master/examples/watchlist.html')
	else:
		if 'userid' in session:
			userid = session["userid"]
			# print(userid)
		else:
			return redirect(url_for('login'))
		if 'isadmin' in session:
			isadmin = session["isadmin"]
		# fetch the url and process it
		post_data = request.json
		watchlist = []
		exp_date = []
		search_histories = dbmanager.get_search_history(userid)
		for row in search_histories:
			if row[1] == 1:
				if(row[0] not in watchlist):
					watchlist.append(row[0])
					exp_date.append(row[3])
		return jsonify(
				watchlist=watchlist,
				exp_date=exp_date
			)


if __name__ == '__main__':
	app.run()
