FROM tiangolo/uwsgi-nginx-flask:python3.8

# RUN pip install --upgrade pip && pip install pymongo && pip install zope.interface
RUN pip install --upgrade pip
RUN mkdir database_file
WORKDIR /app 
COPY ./app /app
RUN pip install -r ./requirements.txt
# RUN pip install flask-jwt-extended && pip install pytz
RUN pip install pytz
# EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["main_api.py"]