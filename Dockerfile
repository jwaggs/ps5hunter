FROM joyzoursky/python-chromedriver:3.9

ENV PYTHONUNBUFFERED True

# USER root

#RUN apt-get update
#RUN apt-get install python3-pip -y
#RUN apt-get install vim -y

# set display port to avoid crash
ENV DISPLAY=:99

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY core ./core
COPY main.py .

# chrome driver crashes if running as root user on linux
# USER 1200

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
# ENTRYPOINT ["python3", "main.py"]