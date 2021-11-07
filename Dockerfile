FROM python:3.8-slim

WORKDIR .

COPY ./netomerch-backend /netomerch-backend

RUN python -m pip install --upgrade pip
RUN pip install -r /netomerch-backend/requirements.txt
