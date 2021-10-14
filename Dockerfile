FROM rasa/rasa:2.8.1

USER root
 # The Rasa SDK image runs as non-root user by default. Hence, you have to swit$
 # back to the `root` user if you want to install additional dependencies
# USER root

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip==20.2

RUN pip install sqlite3
RUN pip install -U spacy
RUN python -m spacy download en_core_web_md

RUN pip install -r requirements.txt

#RUN mkdir models
VOLUME /app
VOLUME /app/data
VOLUME /app/models

CMD [ "run","-m","/app/models","--enable-api","--cors","*","--debug"]

# Switch back to a non-root user
USER 1001




#FROM python:3.7-slim


#COPY . ./
#pip install python-dotenv
#FROM python:3.7-slim


#COPY . ./
#pip install python-dotenv
#RUN pip install Flask
#CMD ["python3", "main.py"]



# # Pull a pre-built alpine docker image with nginx and python3 installed
# FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

# # Set the port on which the app runs; make both values the same.
# #
# # IMPORTANT: When deploying to Azure App Service, go to the App Service on th$
# # portal, navigate to the Applications Settings blade, and create a setting n$
# # WEBSITES_PORT with a value that matches the port here (the Azure default is$
# # You can also create a setting through the App Service Extension in VS Code.
# ENV LISTEN_PORT=5000
# EXPOSE 5000

# # Indicate where uwsgi.ini lives
# ENV UWSGI_INI uwsgi.ini

# # Tell nginx where static files live. Typically, developers place static file$
# # multiple apps in a shared folder, but for the purposes here we can use the $
# # app's folder. Note that when multiple apps share a folder, you should creat$
# # with the same name as the app underneath "static" so there aren't any colli$
# # when all those static files are collected together.
# ENV STATIC_URL /hello_app/static

# # Set the folder where uwsgi looks for the app
# WORKDIR /hello_app


# # Copy the app contents to the image
# COPY . /hello_app

# # If you have additional requirements beyond Flask (which is included in the
# # base image), generate a requirements.txt file with pip freeze and uncomment
# # the next three lines.
# #COPY requirements.txt /
# #RUN pip install --no-cache-dir -U pip
# #RUN pip install --no-cache-dir -r /requirements.txt

