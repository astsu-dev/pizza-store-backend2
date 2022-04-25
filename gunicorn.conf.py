import multiprocessing

from pizza_store.settings import settings

wsgi_app = "pizza_store.adapters.app.app:create_app()"
bind = f"{settings.app_host}:{settings.app_port}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
