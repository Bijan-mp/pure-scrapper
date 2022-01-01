FROM ubuntu:18.04

RUN apt update
RUN apt install python3.8 -y  
RUN apt install python3-pip -y
RUN apt-get install netcat -y

WORKDIR /home
RUN pip3 install --upgrade pip
COPY ./requirements.txt /home/requirements.txt
RUN pip3 install -r requirements.txt

COPY ./src ./src
ENV LANG=C.UTF-8

COPY entrypoint.sh entrypoint.sh
CMD ["sh", "entrypoint.sh"]