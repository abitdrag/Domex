import schedule
import time
import dbmanager

def myjob():
    dbmanager.do_daily_mails()
    print("Done !")

schedule.every().day.at("06:00").do(myjob)

while True:
    schedule.run_pending()
    time.sleep(1)