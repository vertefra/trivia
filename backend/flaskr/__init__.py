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
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, PATCH, POST, DELETE, OPTIONS')
        return response

    # ======================= #
    #       ENDPOINTS         #
    # ======================= #

    # GET QUESTIONS

    @app.route('/questions')
    def get_questions():
        categories = {}
        selection = Question.query.all()
        current_questions = paginate_questions(request, selection)

        if (len(current_questions) != 0):
            for question in current_questions:
                category_key = question['category']
                category_value = Category.query.get(category_key)
                categories[category_key] = category_value.type
                categories_list = dict(categories)
        elif (len(current_questions) == 0):
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
            except BaseException:
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
        print('RES: ', res)
        new_question = Question(
            question=res['question'],
            answer=res['answer'],
            difficulty=res['difficulty'],
            category=res['category']
        )

        try:
            db.session.add(new_question)
            db.session.commit()
            total_questions = Question.query.count()
        except BaseException:
            db.session.rollback()
            abort(500)

        return jsonify({
            "success": True,
            "total_questions": total_questions
        })

        # GET CATEGORIES

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        cat_dic = {cat.id: cat.type for cat in categories}
        total_categories = len(categories)
        return jsonify({
            'success': True,
            'categories': cat_dic,
            'total_categories': total_categories
        })

        # SEARCH QUESTION

    @app.route('/question', methods=['POST'])
    def search_questions():
        search = request.get_json()

        query_search_string = '%' + search['searchTerm'] + '%'
        selection = Question.query.filter(
            Question.question.ilike(query_search_string)).all()
        questions = [question.format() for question in selection]

        if (questions):
            return jsonify({
                'success': True,
                'questions': questions,
                'current_category': None,
                'total_questions': len(questions)
            })
        else:
            abort(404)

        # Get question by category

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        categories = {}
        selection = Question.query.filter_by(category=category_id).all()
        current_questions = paginate_questions(request, selection)
        print("current questions: ", current_questions)

        if (len(current_questions) != 0):
            for question in current_questions:
                category_key = question['category']
                category_value = Category.query.get(category_key)
                categories[category_key] = category_value.type
                categories_list = dict(categories)
        elif (len(current_questions) == 0):
            abort(404)

        print()

        category = Category.query.get(category_id).type

        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(current_questions),
            "current_category": category,
            "categories": categories
        })

        # Get random question

    @app.route('/quizzes', methods=['POST'])
    def get_random_question():
        data = request.get_json()
        category_id = data['quiz_category']['id']
        prev_questions = data['previous_questions']

        selection = Question.query.filter_by(category=category_id).all()

        # in case there aren't any questions remaining return question: False
        # to trigger forceEnd: true in frontend

        def random_question():
            max = len(selection)
            random_index = round((random.random() * (max - 1)))
            return selection[random_index]

        if (len(prev_questions) == len(selection)):
            return jsonify({
                'success': True,
                'question': False,
                'current_category': category_id
            })

        else:

            question = random_question()

            while(question.id in prev_questions):
                question = random_question()

            return jsonify({
                'success': True,
                'question': question.format(),
                'current_category': category_id
            })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not found"
        })

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        })

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal server error"
        })

    @app.errorhandler(405)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method not allowed"
        })

    return app
