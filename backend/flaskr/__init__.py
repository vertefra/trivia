import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE
  
  questions = [question.format() for question in selection]
  paginated_questions = questions[start:end]
  return paginated_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
    return response

  #=======================#
  #       ENDPOINTS       #
  #=======================#


  # GET QUESTIONS

  @app.route('/questions')
  def get_questions():
    categories = {}
    selection = Question.query.all()
    current_questions = paginate_questions(request, selection)

    if (len(current_questions)!=0):
      for question in current_questions:
        category_key = question['category']
        category_value = Category.query.get(category_key)
        categories[category_key]=category_value.type
        categories_list = dict(categories)
    elif (len(current_questions)==0):
      abort(404)

    return jsonify({
      "success": True,
      "questions": current_questions,
      "total_questions": len(selection),
      "current_category": None,
      "categories": categories_list
    })

  
  # DELETE QUESTIONS

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question_to_delete = Question.query.get(question_id)
    total_questions = Question.query.all()
    if (question_to_delete):
      try:
        db.session.delete(question_to_delete)
        deleted_id = question_id
        db.session.commit()
      except:
        db.session.rollback()
        abort(500)
    else:
      abort(404)

    total_questions = len(Question.query.all())

    return jsonify({
      "success": True,
      "deleted_id": deleted_id,
      "total_questions": total_questions
    })

  # POST QUESTION

  @app.route('/questions', methods=['POST'])
  def post_question():
    res = request.get_json()
    
    new_question = Question(
        question = res['question'],
        answer = res['answer'],
        difficulty = res['difficulty'],
        category = res['category']
    )

    try:
      Question.query.add(new_question)
      db.session.commit()
      posted_id = db.session.query(Question.id).filter('question'==res['question'])
      print('POSTED ID', posted_id)
    except:
      db.session.rollback()
      abort(500)

    return jsonify({
      "success": True,
      "posted_id": 'posted_id',
      "total_questions": 'total_quesitons'
    })

    # need to create GET for /categories first


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource not found"    
      })

  @app.errorhandler(500)
  def not_found(error):
      return jsonify({
          "success": False,
          "error": 500,
          "message": "Internal server error"    
      })
  return app

    