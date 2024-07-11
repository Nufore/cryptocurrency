from celery import Celery
from db.updater import update_data_and_send_message
import asyncio

celery_task = Celery('tasks', broker='redis://redis:6379')


@celery_task.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60, execute_tasks.s(), name="execute every 60 min")


@celery_task.task
def execute_tasks():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_data_and_send_message())


