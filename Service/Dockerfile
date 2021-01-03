FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python3-dev python3-pip build-essential
WORKDIR /app 
COPY ./app /app
RUN pip3 install -r ./requirements.txt
RUN pip3 install pytz && pip3 install dnspython
ENTRYPOINT ["python3"]
CMD ["main_api.py"]