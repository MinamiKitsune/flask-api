# Flask API
Flask restful API for a vaccine webservice

## Requirements
Install python from https://www.python.org/

## How to set up the virtual environment for testing (This only needs to be done once)
Open a terminal or command prompt in the location of the application.

Paste the following in the command prompt:  
`pip install pipenv`

Run the following in the command prompt to create the environment:  
`pipenv shell`

Run the following in the command prompt to install all the packages:  
`pipenv install` 

Run the following to set up the environment for flask:  
For Linux:  
`export FLASK_APP=run.py`  
`export FLASK_ENV=development`  
`export FLASK_DEBUG=1`

For Windows CMD:  
`set FLASK_APP=run.py`  
`set FLASK_ENV=development`  
`set FLASK_DEBUG=1`

For Windows Powershell:  
`$env:FLASK_APP=run.py`  
`$env:FLASK_ENV=development`  
`$env:FLASK_DEBUG=1`

## Running the API
Execute the following to run the application:  
`flask run`