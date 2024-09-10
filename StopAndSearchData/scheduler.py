from apscheduler.schedulers.background import BackgroundScheduler
from StopAndSearchData.data_fetch import update_data
import atexit

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_data, trigger="interval", days=1)
    scheduler.start()

    # Ensure Flask shuts down properly
    atexit.register(lambda: scheduler.shutdown())
