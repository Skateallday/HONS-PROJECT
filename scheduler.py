from flask import Flask
from flask_apscheduler import APScheduler
import sqlite3


app = Flask(__name__)
scheduler = APScheduler()

def changeLikesAvailable():
    conn =sqlite3.connect('userData.db')
    print("Opened database successfully")
    c = conn.cursor()
    with conn:
        try:            
            c.execute('UPDATE accountData SET dailyVotes = 4 WHERE dailyVotes < 4')    
            print('Daily Votes updated')
        except Exception as e: print(e)       
    
   

if __name__ =='__main__':
    scheduler.add_job(id='Update Daily Votes', func=changeLikesAvailable, trigger="interval", seconds=86400)
    scheduler.start()