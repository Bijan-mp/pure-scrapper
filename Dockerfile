FROM ubuntu

RUN apt update
RUN apt install python3.8 -y  
RUN apt install python3-pip -y
RUN apt-get install netcat -y

WORKDIR /home
COPY ./requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000

COPY ./src ./src


COPY entrypoint.sh entrypoint.sh
CMD ["sh", "entrypoint.sh"]