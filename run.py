import schedule
import time
from app.main import job
from config.settings import SCHEDULE_TIME
import sys

if __name__ == "__main__":
    print("🚀 Project [GitHub Trending Reporter] Started.")
    print(f"🕒 Scheduled job to run every day at {SCHEDULE_TIME}.")
    
    # 为了方便测试，可以取消下一行注释，在启动时立即执行一次
    print("🏃 Performing initial run immediately...")
    job()

    # 设置定时任务
    schedule.every().day.at(SCHEDULE_TIME).do(job)

    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Manual interruption detected. Shutting down.")
            sys.exit(0)