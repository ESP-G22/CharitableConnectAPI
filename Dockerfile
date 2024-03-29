FROM ubuntu:latest
RUN apt update
RUN apt upgrade -y
RUN apt install python3 python3-pip -y
RUN pip3 install django
RUN mkdir /workdir
WORKDIR /workdir
COPY . /workdir
RUN pip3 install -r requirements.txt
EXPOSE 8000
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
ENTRYPOINT python3 manage.py runserver 0.0.0.0:8000
