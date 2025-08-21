FROM python:3.12.10

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN apt-get -y install vim

RUN mkdir /app
ADD . /app
WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY .env .

# gunicorn 워커 수를 1개로 설정
CMD ["gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]