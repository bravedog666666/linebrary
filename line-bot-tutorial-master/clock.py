from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request
import datetime
sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='0-4', minute='*/25')
def scheduled_job():
    url = "https://ancient-gorge-17795.herokuapp.com/"
    conn = urllib.request.urlopen(url)
        
    for key, value in conn.getheaders():
        print(key, value)

# @sched.scheduled_job('cron', minute='*/2')
# def scheduled_job():
#     print('========== APScheduler CRON =========')
#     # 馬上讓我們瞧瞧
#     print('This job runs every day */2 min.')
#     # 利用datetime查詢時間
#     print(f'{datetime.datetime.now().ctime()}')
#     print('========== APScheduler CRON =========')

#     url = "https://ancient-gorge-17795.herokuapp.com/"
#     conn = urllib.request.urlopen(url)
        
#     for key, value in conn.getheaders():
#         print(key, value)

sched.start()
