FROM python:3.7

RUN apt-get update -y
RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN mkdir /home/logs && mkdir /home/app
RUN mkdir -p /home/appdata

WORKDIR /home/app

COPY app /home/app

CMD ["gunicorn", "--workers=4", "-b 0.0.0.0:5000", "--preload", "app_creator:create_app()"]
