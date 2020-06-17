
## INTRODUCTION

API to access a database of trivia questions categorized for category.
Are included methods to add new trivias, retrieve categories or retrieve quenstions based on category. 

## GETTING STARTED

- In order to install all the dependecies required from nodejs run

```bash
npm install
```

- Make sure to install also all the requirements for python

```bash
pip install requirements.txt
```

All the backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/)

- To run the backend development server, run in the backend folder

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```


### Key dependecies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

- [Nodejs](https://nodejs.org/en/) is a Javascript runtime built on Chrome's V8 Javascript engine. It comes with  

- [Npm](https://www.npmjs.com/), Nodejs package manager to hadle all the js dependecies for the frontend

### Running the tests

The file **test_flaskr.py** run test for all the endpoints of the Api. 
it works on a test database  **testdb**. Just make a copy of the original database **trivia.psql** and load id with **postgres**
**test_flaskr** will take care of creating new test entries and deleted them at the end of each test 
   

### BASE URL

At the present this app can only run locally.

- The backend is hosted at the default http://localhost:5000.
- The frontend is hosted at the default http://localhost:3000

This version of the app does not require authentication

### ENDPOINTS


#### GET /questions


returns a dictionary where the key **questions** contains a list of all the questions in the database. 

A **Question** object is dictionary with the following key, values:

```bash
{
    'id': int,
    'question': str,
    'answer': str,
    'category': int,
    'difficulty': int

}
```

While 'question', 'answer' and 'difficulty' are pretty self explanatory, **category** is an integer related to a Model class in the models.py file, the subclass Category, representation of a table where the **id** number is associated to a string value **type**, the name of the category. 

You can also specify how many pages would you like to see adding the parameter **page** to the query

```bash
/questions?page=1```

every page shows 10 questions


#### DELETE /questions/question_id

This endpoint delete a question associated with the id **question_id**. 

Requires an integer as arguments associated with the id of the question that will be deleted 

if succesful returns a dictionary object with keys

-"deleted_id" Integer value, id of the question succesfully deleted
-"total_questions" Integer  value, the number of questions still in the database


#### POST /questions

This endpoint takes as argument a **Question** object with the following paramenters

question = String,
answer = String
difficulty = Integer,
category = Integer

if succesfull, returns the total number of questions in the database

#### GET /categories

returns a json object with the key **'categories'**, a dictionary with all the categories in the database with the numeric value of their id associated with the type, the string value of the category

#### POST /question

returns the result of a search for a string in the questions table of the database. Require a string as an argument. 

The search is **case insensitive** and looks also for **substring**

the key "questions" in the returned object contains the list of all the Question objects that matched the search. 

the key "total_questions" is the total amount of questions that matched the search.

#### GET /categories/category_id/questions

returns all the questions that match the requested category.
require the **category_id** as parameters based on the Category model

1 - "Science"
2 - "Art"
3 - "Geography"
4 - "History"
5 - "Entertainment"
6 - "Sports"

#### GET /quizzes

returns a random question. Reuire the category id of the question and a list of question object as arguments. if the list is empty will generate a random question (max 100 per category) between all the question in that category. 

If the list contain Question objects it will generate a random question that is **NOT** contained in the list.

If the length of the list is equal to the total questions it will return an dictionary object with key **'question': False**

### Errors handling

In case of errors the application can handle with approprieate response 4 types of errors:

-404 Resource not found

-422 Unprocessable Entity

-500 Internal server error

-405 Method not allowed

All the following errors will produce a dictionary Object as a response with the following keys

"succes", value False, indicate that the request was not succesfull
"error" the integer value associated with the error
"message" a String, textual descprition of the error


