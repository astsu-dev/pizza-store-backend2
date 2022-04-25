FROM python:3.10

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY gunicorn.conf.py ./
COPY pizza_store ./pizza_store
COPY .env ./

EXPOSE 8000

CMD ["gunicorn"]
