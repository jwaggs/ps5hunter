FROM python:3.10

ENV PYTHONUNBUFFERED True

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY core ./core
COPY main.py .

ENV PORT=8080
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 60 main:app
