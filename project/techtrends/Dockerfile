FROM python:3.8
LABEL maintainer="Ali Habib"

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

#intitate the database 
RUN python init_db.py 

# command to run on container start
CMD [ "python", "app.py" ] 