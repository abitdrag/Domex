class User:
    def __init__(self, userid, fname, lname, emailid, address, city, country, postalcode, dob, registrationdate, lastlogindate, comments, password, isadmin):
        self.__userid = userid
        self.__fname = fname
        self.__lname = lname
        self.__emailid = emailid
        self.__address = address
        self.__city = city
        self.__country = country
        self.__postalcode = postalcode
        self.__dob = dob
        self.__registrationdate = registrationdate
        self.__lastlogindate = lastlogindate
        self.__comments = comments
        self.__password = password
        self.isadmin = isadmin  # isadmin = 0 when user is not admin, isadmin = 1 when user is admin

    def getuserid(self):
        return self.__userid
    
    def setuserid(self, newuserid):
        self.__userid = newuserid

    def getfname(self):
        return self.__fname
    
    def setfname(self, newfname):
        self.__fname = newfname

    def getlname(self):
        return self.__lname

    def setlname(self, newlname):
        self.__lname = newlname
    
    def getemailid(self):
        return self.__emailid

    def setemailid(self, newemailid):
        self.__emailid = newemailid

    def getaddress(self):
        return self.__address
    
    def setaddress(self, newaddress):
        self.__address = newaddress

    def getcity(self):
        return self.__city

    def setcity(self, newcity):
        self.__city = newcity

    def getcountry(self):
        return self.__country
    
    def setcountry(self, newcountry):
        self.__country = newcountry

    def getpostalcode(self):
        return self.__postalcode
    
    def setpostalcode(self, newpostalcode):
        self.__postalcode = newpostalcode

    def getdob(self):
        return self.__dob

    def setdob(self, newdob):
        self.__dob = newdob    
    
    def getregistrationdate(self):
        return self.__registrationdate

    def setregistrationdate(self, newregistrationdate):
        self.__registrationdate = newregistrationdate

    def getlastlogindate(self):
        return self.__lastlogindate

    def setlastlogindate(self, newlastlogindate):
        self.__lastlogindate = newlastlogindate
    
    def getcomments(self):
        return self.__comments
    
    def setcomments(self, newcomments):
        self.__comments = newcomments
    
    def getpassword(self):
        return self.__password
    
    def setpassword(self, newpassword):
        self.__password = newpassword

class Emails:
    def __init__(self, userid, emailid, date):
        self.__userid = userid
        self.__emailid = emailid
        self.__date = date
    
    def getuserid(self):
        return self.__userid
    
    def setuserid(self, newuserid):
        self.__userid = newuserid
    
    def getemailid(self):
        return self.__emailid
    
    def setemailid(self, newemailid):
        self.__emailid = newemailid
    
    def getdate(self):
        return self.__date
    
    def setdate(self, newdate):
        self.__date = newdate

class SearchHistory:
    def __init__(self, urlid, userid, watching, searchdate, numberofsearches):
        self.__urlid = urlid
        self.__userid = userid
        self.__watching = watching
        self.__searchdate = searchdate
        self.__numberofsearches = numberofsearches
    
    def geturlid(self):
        return self.__urlid
    
    def seturlid(self, newurlid):
        self.__urlid = newurlid
    
    def getuserid(self):
        return self.__userid
    
    def setuserid(self, newuserid):
        self.__userid = newuserid
    
    def getwatching(self):
        return self.__watching
    
    def setwatching(self, newwatching):
        self.__watching = newwatching

    def getsearchdate(self):
        return self.__searchdate
    
    def setsearchdate(self, newsearchdate):
        self.__searchdate = newsearchdate
    
    def getnumberofsearches(self):
        return self.__numberofsearches
    
    def setnumberofsearches(self, newnumberofsearches):
        self.__numberofsearches = newnumberofsearches

class Urls:
    def __init__(self, urlid, url, expirydate):
        self.__urlid = urlid
        self.__url = url
        self.__expirydate = expirydate
    
    def geturlid(self):
        return self.__urlid
    
    def seturlid(self, newurlid):
        self.__urlid = newurlid
    
    def geturl(self):
        return self.__url
    
    def seturl(self, newurl):
        self.__url = newurl

    def getexpirydate(self):
        return self.__expirydate
    
    def setexpirydate(self, newexpirydate):
        self.__expirydate = newexpirydate

class Adminstats:
    def __init__(self, statid, stattype, date):
        self.__statid = statid
        self.__stattype = stattype
        self.__date = date
    
    def getstatid(self):
        return self.__statid
    
    def setstatid(self, newstatid):
        self.__statid = newstatid
    
    def getstattype(self):
        return self.__stattype
    
    def setstattype(self, newstattype):
        self.__stattype = newstattype
    
    def getdate(self):
        return self.__date
    
    def setdate(self, newdate):
        self.__date = newdate

class Notifications:
    def __init__(self, userid, notificationcontent, isseen, type):
        self.__userid = userid
        self.__notificationcontent = notificationcontent
        self.__isseen = isseen
        self.__type = type
    
    def getuserid(self):
        return self.__userid

    def setuserid(self, newuserid):
        self.__userid = newuserid
    
    def getnotificationcontent(self):
        return self.__notificationcontent
    
    def setnotificationcontent(self, newnotificationcontent):
        self.__notificationcontent = newnotificationcontent
    
    def getisseen(self):
        return self.__isseen
    
    def setisseen(self, newisseen):
        self.__isseen = newisseen
    
    def gettype(self):
        return self.__type
    
    def settype(self, newtype):
        self.__type = newtype

