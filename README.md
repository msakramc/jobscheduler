# jobscheduler

PROJECT STRUCTURE

# PYTHON VERSION - Python 3.12.6

--jobscheduler----------|
--venv                  |---config --->
                        |---scheduler --->     
                        |---.env
                        |--.gitignore
                        |---manage.py
                        |---README.md
                        |---requirements.txt

# STEP TO RUN THIS PROJECT

# Clone the project

# Create virtaul environment: Sample "venv"
1. pip3 install virtualenv
2. virtualenv venv
# After executing the command 'virtualenv venv', a new folder named "venv" will be created.
# To activate the virtual environment, run the following command. 
# Make sure you're in the directory where the "venv" folder is located, 
# or adjust the path accordingly.
3. venv\Scripts\activate

# Once the virtual environment is activated, you will see (venv) at the beginning of your command prompt path.
# For example: (venv) C:\Users\username\Desktop\jobscheduler>

# Now, navigate to your project folder by using the 'cd' command.
# For example: cd jobscheduler
# Open VS Code or any other code editor of your choice.
4. pip install -r requirements.txt

# By default, the database in the .env file is set to postgres. If you wish to use a different database, please update .env file
# SAMPLE SHOWN BELOW
# DATABASE_URL=postgres://username:password@host:port/database
# !!! MAKE SURE YOU HAD CREATED THE DATABASE BEFORE MIGRATE
# YOU CAN VIEW DATABASE SCHEMA INSIDE SCHEDULER/MODELS.PY

# Now run below command to migrate the tables to database
5. python manage.py migrate

# Now create a user by executing below command
6. python manange.py createsuperuser

7. python manage.py runserver

# Now django server will run in http://127.0.0.1:8000/

-----SETTIN UP CELERY-------------------------

# To configure Celery for handling background tasks, follow these steps:
# Install RabbitMQ or Redis:
# If you're using RabbitMQ:
#      Download and install RabbitMQ from the official website.
#      Ensure the RabbitMQ server is running.
# If you're using Redis:
#       Install Redis from the official website.
#       Ensure the Redis server is running.
# Update settings.py:
# In your Django settings.py file, configure the CELERY_BROKER_URL based on the message broker you're using:

# In settings.py file in 171, 'CELERY_BROKER_URL = 'pyamqp://guest@localhost//'
# Here Iam using windows and I have RabbitMQ server

# Now run celery in another terminal (Here I am running 3 workers such that celery can execute 3 job simultaneously)
# Make sure venv is activated in every terminal were celery is running
# Command to run celery shown below
# celery -A your_project_name worker --loglevel=info -P solo
# Here your_project_name is "config" so run below commad
7. celery -A config worker --loglevel=info -P solo

# So there are total of 4 terminal currently running
# 1 django terminal and 3 celery terminal


# API DETAILS

# NEW USER CREATION
# YOU MUST CREATE A SUPERUSER FIRST THEN ONLY YOU CAN LOGIN TO ADMIN AND CREATE NEW USERS
1. python manage.py createsuperuser
# http://localhost:8000/admin

# DASHBOARD:
# http://localhost:8000

# SUBMIT JOBS:
# You can submit jobs via Dashboard or RESTAPI
# http://localhost:8000/api/v1/createjob/

# FETCH A JOB: 
# http://localhost:8000/api/v1/{job_id}/job/

# LIST ALL JOB FOR A USER
# http://localhost:8000/api/v1/getjobs/












