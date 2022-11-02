FROM python:3.8

WORKDIR /bolt-app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./app ./app

CMD ["python", "./app/remotecall4L3-onramp.py"]