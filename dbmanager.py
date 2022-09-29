from os import curdir
import sqlite3
import models
import dnshelper
from datetime import datetime
from datetime import timedelta
import mailmanager
db_location = "E:\Miki\domain project\DomeX\DomexDB.db"
def check_login(username, password):
	try:
		con = sqlite3.connect(db_location)
		cur = con.cursor()
		cur.execute("SELECT emailid, password, userid, isadmin from User where emailid=? and password=?;",(username, password))
		row = cur.fetchall()
		if not row:  
			print("Login failed")
			return -1, 0
		else:
			print("Welcome")
			print(row)
			return row[0][2], row[0][3]
		con.close()
	except Exception as e:
		print(e)

def sign_up(u):
	try:
		con = sqlite3.connect(db_location, timeout=1000)
		cur = con.cursor()
		q = "SELECT emailid FROM User"
		cur.execute(q)
		if u.getemailid() in cur.fetchall():
			print("Already a User!!!!!")
		else:
			fname = u.getfname()
			lname = u.getlname()
			emailid = u.getemailid()
			address = u.getaddress()
			city = u.getcity()
			country = u.getcountry()
			postalcode = u.getpostalcode()
			dob = u.getdob()
			registrationdate = u.getregistrationdate()
			lastlogindate = u.getlastlogindate()
			comments = u.getcomments()
			password = u.getpassword()
			
			cur.execute("INSERT INTO User(fname, lname,emailid, address, city, country, postalcode, dob,registrationdate, lastlogindate , comments , password ) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?)",fname, lname,emailid, address, city, country, postalcode, dob,registrationdate, lastlogindate , comments , password)
			con.commit()
		cur.close()
	except Exception as e:
		print("Error occurred : " + str(e))

def get_urlid(url_obj):
	try:
		con = sqlite3.connect(db_location)
		cur = con.cursor()
		url_txt = url_obj.geturl()
		cur.execute("SELECT urlid from Urls where url=?", (url_txt,))
		row = cur.fetchall()
		if not row:  
			# print("URL ID not found!")
			return -1
		else:
			# print("URL ID found")
			return row[0][0]
		con.close()
	except Exception as e:
		print(e)

def add_new_url(url_obj):
	url = url_obj.geturl()
	expirydate = url_obj.getexpirydate()
	try:
		con = sqlite3.connect(db_location)
		cur = con.cursor()
		cur.execute(f"INSERT INTO Urls (url, expirydate) values (?, ?)", (url, expirydate,))
		con.commit()
		con.close()
		return cur.lastrowid
	except Exception as e:
		print(e)

# below function will add the url if it doesnt exist and return the url id
def get_and_add_url(url_obj):
	urlid = get_urlid(url_obj)
	if urlid == -1:
		urlid = add_new_url(url_obj)
	return urlid

def add_new_search_history(searchHistoryObj):
	urlid = searchHistoryObj.geturlid()
	userid = searchHistoryObj.getuserid()
	watching = searchHistoryObj.getwatching()
	searchdate = searchHistoryObj.getsearchdate()
	numberofsearches = searchHistoryObj.getnumberofsearches()
	try:
		con = sqlite3.connect(db_location)
		cur = con.cursor()
		cur.execute("INSERT INTO SearchHistory (urlid, userid, watching, searchdate, numberofsearches) values (?, ?, ?, ?, ?)", (urlid, userid, watching, searchdate, numberofsearches,))
		con.commit()
		con.close()
		return cur.lastrowid
	except Exception as e:
		print(e)

def update_url_watching_status(searchHistoryObj):
	urlid = searchHistoryObj.geturlid()
	userid = searchHistoryObj.getuserid()
	watching = searchHistoryObj.getwatching()
	searchdate = searchHistoryObj.getsearchdate()
	numberofsearches = searchHistoryObj.getnumberofsearches()
	try:
		con = sqlite3.connect(db_location)
		cur = con.cursor()
		cur.execute("UPDATE SearchHistory SET watching =? WHERE urlid =? AND userid =?", (watching, urlid, userid,))
		con.commit()
		con.close()
	except Exception as e:
		print(e)

def get_search_history(userid):
	try:
		con = sqlite3.connect(db_location)
		cur = con.cursor()
		cur.execute("SELECT * FROM SearchHistory AS sh INNER JOIN Urls AS u ON u.urlid=sh.urlid WHERE sh.userid=?", (userid,))
		rows = cur.fetchall()
		entries = []
		if not rows:  
			# print("URL ID not found!")
			return -1
		else:
			for row in rows:
				if (len(row) >= 5):
					# 6 = url, 2 = watching, 0 = urlid, 7 = exp_date
					entries.append((row[6], row[2], row[0], row[7]))
				else:
					print("Invalid entry found: " + str(row))
		con.close()
		return entries		
	except Exception as e:
		print(e)

def do_daily_mails():
	try:
		con = sqlite3.connect(db_location)
		cur = con.cursor()
		# get all users
		cur.execute("SELECT * FROM User")
		rows = cur.fetchall()
		users = [] # list of tuple
		for row in rows:
			# 0 = userid, 1 = fname, 2 = lname, 3 = emailid, 8 = dob
			users.append((row[0], row[1], row[2], row[3]))
		# get all watching email ids
		con.close()
		
		con = sqlite3.connect(db_location)
		cur = con.cursor()
		cur.execute("SELECT * FROM SearchHistory AS sh INNER JOIN Urls AS u ON u.urlid=sh.urlid")
		rows = cur.fetchall()
		con.close()
		
		watch_results = []
		for row in rows:
			if(row[2] == 1):
				
				domain_details = dnshelper.make_whois_query(row[6])
				# print(domain_details)
				try:
					
					exp_date = domain_details.expiration_date[0]
					expiry_date = domain_details.expiration_date[0].strftime("%d %B, %Y")
				except Exception as e:
					
					exp_date = domain_details.expiration_date
					expiry_date = domain_details.expiration_date.strftime("%d %B, %Y")
				# 0 = urlid, 1 = userid, 2 = watching, 6 = url, 7 = expirydate
				
				watch_results.append((row[0], row[1], row[6], expiry_date))
				# print(watch_results)
				# if expirydate has been changed then update it in table
				
				if(row[7] != expiry_date):
					con = sqlite3.connect(db_location)
					cur = con.cursor()
					cur.execute("UPDATE Urls SET expirydate =? WHERE url =?", (expiry_date, row[6], ))
					con.commit()
					con.close()
				# check if expiry is in one week
				if exp_date > datetime.now() and exp_date < datetime.now() + timedelta(days=7):
					
					for user in users:
						if user[0] == row[1]:
							# matched user
							name = user[1] + " " + user[2]
							msg = "Hello "+ name +"! The domain " + str(row[6]) + " will expire on " + str(expiry_date) +". Please take some action. Thank you for using our services!!" 
							print("mail msg: " + str(msg))
							mailmanager.send_email(user[3], msg)
	except Exception as e:
		print(e)


# user1 = models.User(None,"Dhruvik","Patel","dhruvik@gmail.com","Shreenathji","Vadodara","India","390099","29-2-2000",None,None,None,"Password")
# sign_up(user1)
# check_login("12@23", "1223")