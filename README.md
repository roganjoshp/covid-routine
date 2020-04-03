# covid-routine
Scheduling app for nurses and doctors attempting to fight COVID19

This is a project inspired by the call for help issued by the German Center for Infection Research. In particular, the app:
* Must be able to pool personnel from given operational entities.
* Must be able to record and bookkeep personnel capabilities in an easy / intuitive way.
* Must support finding replacements and rescheduling in the case that personnel is infected.

More information can be found on the thread [here](https://discourse.data-against-covid.org/t/request-for-help-simple-and-safe-software-solutions-for-efficiently-dispatching-personnel/573).

## Running the app - Windows cmd ##

```
flask db upgrade # To ensure the database schema is up to date
set FLASK_APP=main_app.py
set FLASK_DEBUG=1
flask run
```

## Running the app - Windows Powershell ##

```
flask db upgrade
$env:FLASK_APP="main_app.py"
$env:FLASK_DEBUG=1
flask run
```

## Running the app - Linux ##

```
flask db upgrade
export FLASK_APP=main_app.py
export FLASK_DEBUG=1
flask run
```

## Logging in to the app ##
When first launching the app, a check will be made to see if there are any registered users in the database. 
If not, a default will be created with the username "default" and password "deleteme". 
This user will have full admin privileges (once implemented) in order to create a new administrator. 
