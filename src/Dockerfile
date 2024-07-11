FROM python:3.11.8-slim

ADD requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt


COPY / /src

WORKDIR /src

CMD ["python", "bot/starter.py"]