# RESTApi
This rest api is written using Django 2.1.4 and Django Rest Framework 3.9.0. Python 3.6 is required as well. Please make sure you have these installed before running the app.

Navigate into the TestProject folder and run the application with python manage.py runserver.

The following urls can be used for checking api functionality. These have been copied from the betting/urls.py file:

* http://127.0.0.1:8000/betting/submit
    here you can submit new event or odds updates. You can django rest's browsable api if you wish or alternatively use something like postman
* http://127.0.0.1:8000/betting/
    this will retrieve a list of all the events
* http://127.0.0.1:8000/betting/<int:pk>/
    this will retrieve match data based on id
* http://127.0.0.1:8000/betting/event/football/
    this will retrieve matches order by a match field. So if you want to order by start time,
you can enter http://127.0.0.1:8000/betting/event/football?ordering=start_time
* http://127.0.0.1:8000/betting/event/
    this will retrieve a match by name. If you wish to search by name you can enter http://127.0.0.1:8000/betting/event/?name=Real Madrid vs Barcelona

*Note you may run the app on a different port, 8000 is the default django one. 

TO DO:

* tests for the serializer objects
