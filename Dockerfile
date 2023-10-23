FROM python:3.11

WORKDIR /var/www/app

ADD requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000/tcp
