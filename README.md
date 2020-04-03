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
