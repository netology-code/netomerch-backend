FROM python:3.8-slim

WORKDIR /app

RUN python -m pip install --upgrade pip
RUN pip install gunicorn

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x ./scripts/* && mv ./scripts/* . && rm -r ./scripts/

CMD bash run.sh
