FROM python:3.11

WORKDIR /DevHackAPI

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./api ./api

CMD ["python", "./api/main.py"]