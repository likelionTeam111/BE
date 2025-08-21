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

# gunicorn 실행 명령어를 CMD에 추가
CMD ["gunicorn", "Hack_BE.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1", "--timeout", "120", "--log-level", "info"]