FROM python:3.10

RUN apt-get update

COPY . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "main.py"]