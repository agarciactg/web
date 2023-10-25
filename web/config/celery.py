import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.config.settings")

app = Celery("web")
app.conf.timezone = "America/Argentina/Buenos_Aires"
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf["worker_prefetch_multiplier"] = 1  # noqa

app.conf.update(
    BROKER_URL="redis://redis:6379/0",  # noqa
)


@app.task(bind=True)  # noqa
def debug_task(self):
    print("Request: {0!r}".format(self.request))
