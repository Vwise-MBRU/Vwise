# Vwise Documentation - Phase1 Deployment - WHO data

DockerImages:
    Flask:vwiseme
    ActionServer:vwiseme_actions
    Rasa:vwiseme_rasa


The directory structure:
----vwise_training_public
    |--actions
    |--data
    |--models
    |--tests
    |--config.yml
    |--credentials.yml
    |--endpoints.yml
    |--domain.yml

    These(above) are files related to rasa

    |--templates/
    |--static/
    |--main.py
    |--main.wsgi
    |--logs/
    |--Pipfile

    These(above) are files related to Flask application

    |--requirements.txt
    |--Dockerfile
    |--docker-compose.yml
    

    Above are the files for running the rasa application

    |--PostSurveyDetails.db  //stores post survey details
    |--rasa.db  //created and stored automatically be rasa
    |--vaccine.db  // stores all the conversation history for later use (backup)
    |--surveydetails.db  // stores the pre survey details
    |--details.db  // stores the bot quality metric scores

    Above are the various database files


00. Install and configure Apache webserver

    * Clone the repo from GitHub
        >> cd
        >> cd /home/sree_mbru
        >> git clone <<"HTTP url from GiyHub repository">> 

    * Configure the webserver
        >> sudo su
        >> cd
        >> apt-get install apache2
        >> systemctl start apache2.service
        >> systemctl status apache2.service
        >> cd /etc/apache2/sites-available
        >> sudo nano 000-default.conf
            -->>ServerAdmin 20.185.1.25
            -->>DocumentRoot /home/sree_mbru/vwise_training_public/templates
        >> systemctl restart apache2.service
            

    * Edit 000-default.conf with our html file location
        >> DocumentRoot <<"path to the file">>
        >> sudo systemctl reload apache2.service

                Troubleshooting: ERROR: forbidden you don't have permission to access / on this server
                >> cd /etc/apache2
                >> nano apache2.conf
                Change the Directory part
                    <Directory />
                    Options Indexes FollowSymLinks Includes ExecCGI
                    AllowOverride All
                    Require all granted
                    </ Directory>
                Restart apache server
                >> sudo systemctl reload apache2.service


1. Deploy flask application to apache web server
    
    
    For a flask application the file arrangement should be:
        ---Main Directory
           |--templates  // templates folder has html files for different web pages
           |--static     // Static folder has all the static files like css, images ,etc
           |--main.py    // the python file to be executed
    

    * Create a "Pipfile" having following contents:
        [[source]]
        url="https://pypi.org/simple"
        verify_ssl=true
        name="pypi"

        [packages]
        flask="*"

        [dev-packages]

        [requires]
        python_version="3.6"

        A Pipfile.lock will automatically be created.



    * Install pipenv to create a virtual environment in the project folder
        
    
        Foldername- vwise_training_public
        >> cd vwise_training_public
        >> sudo apt install python3-pip
        >> sudo pip install pipenv
        >> pipenv install // it uses the Pipfile
        >> pipenv --venv //venv stands for virtual environment ---> copy the path to be pasted in main.wsgi file ("in activate_this" variable)

    

    * Create a directory called logs into which all the logs will be written
        >> mkdir logs
        // It creates "access.log" automatically inside it.


    * create a file "main.wsgi" with the following contents:

        import sys
        sys.path.insert(0,'/home/sree_mbru/vwise_training_public')

        activate_this='/home/sree_mbru/.local/share/virtualenvs/vwise_training_public$
        with open(activate_this) as file_:
                exec(file_.read(),dict(__file__=activate_this))

        from main import app as application
        //main is the main.py(file name), app is the variable used in this py file to initialise the program (app=Flask(__main))

    * Create a configuration file to link to the flask application- name it vwise_training_public.config
    

        >> cd /etc/apache2/sites-available/
        >> touch vwise_training_public.config
        >> nano vwise_training_public.config


        <VirtualHost *:80>
        ServerName 20.185.1.25

        WSGIDaemonProcess flaskapp user=www-data group=www-data threads=5
        WSGIScriptAlias / /home/sree_mbru/vwise_training_public/main.wsgi

        <Directory /home/sree_mbru/vwise_training_public>
                WSGIProcessGroup flaskapp
                WSGIApplicationGroup %{GLOBAL}
                Order deny,allow
                Allow from all
        </Directory>

        <Directory /home/sree_mbru/vwise_training_public/static/>
                Order allow,deny
                Allow from all
        </Directory>
        ErrorLog /home/sree_mbru/vwise_training_public/error.log
        CustomLog /home/sree_mbru/vwise_training_public/logs/access.log combined
        
        </VirtualHost>

    //flaskapp - is a name given(it can be anything)

    * If you have an IP or domain, specify it at the ServerName in this file.


    * Enable the website
        >> sudo a2ensite vwise_training_public.config
    

    * Reload apache
        >> sudo systemctl reload apache2.service
        This will give you an error- Invalid command- WSGIDeamonProcess- module not included in server configuration
        --> Resolution:
            >> sudo apt-get install libapache2-mod-wsgi-py3
            Check whether its enabled by:
                >> sudo a2enmod wsgi
            Check the configuration:
                >> sudo systemctl configtest
                --> Syntax OK
        >> sudo systemctl reload apache2.service


    * Trouble shooting: If some error, navigate to
        >> vim logs/error.log
        After rectifying errors if any, make sure you restart the apache server


2. Deploy the bot
    * Update endpoints.yml
        action_endpoint:
            url: "http://20.185.1.2:5055/webhook"
    * Update credentials.yml
        rasa:
            url: "http://20.185.1.2:5002/api"
    * Create a "Dockerfile"


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
    
    * Create a "docker-compose.yml" file with following contents:


        version: "3.8"
        services:
        #  app:
        #    build: .
        #    command: python main.py
        #    ports:
        #      - "5000:5000"
        #      - "443:443"
        #    volumes:
        #      - .:/vwiseme
        rasa_action_server:
            build: .
            #command: rasa run actions
            ports:
            - "5055:5055"
            volumes:
            - .:/vwiseme_actions
        rasa:
            build: .
            #command: rasa run -m models --enable-api --cors "*" --debug
            ports:
            - "5005:5005"
            volumes:
            - .:/vwiseme_rasa


    * Run the docker file
        >> sudoomkdir models
        >> sudo chmod a+rwx models
        >> sudo docker-compose up --remove-orphans // to abort any unused containers
        >> sudo docker-compose --build

    Troubleshooting:
        If some directories are not having write permissions:
        --> Check the permissions: ls -la
        --> Grant a permission: 
                >> sudo chmod a+rwx <directory/file name>
                    // I had to give the permisson for "models" directory as the model generated requires write permissions to the directory.


3. Deploying RasaX
    * Using Docker
        >> sudo su
        >> curl -sSL -o install.sh https://storage.googleapis.com/rasa-x-releases/0.32.2/install.sh
        >> sudo bash ./install.sh
        >> cd /etc/rasa
        >> ls
        >> sudo docker-compose up -d
        >> sudo python rasa_x_commands.py create --update admin me <password>


4. CI/CD pipeline - Connect to GitHub

    * Create a workflow
        - Navigate to Actions section in the GitHub
        - Create a vwise.yml file in .github/actions
        - Connect to the Virtual Machine in which we have the files available
        - On a new push to the repository, the following instructions should run on the file available in the VM