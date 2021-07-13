FROM python:3.7.6

WORKDIR /code/hms

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000 