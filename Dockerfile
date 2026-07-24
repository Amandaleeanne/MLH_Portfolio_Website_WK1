FROM python:3.14-slim-bookworm

WORKDIR /MLH_Portfolio_Website_WK2

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]

EXPOSE 5000