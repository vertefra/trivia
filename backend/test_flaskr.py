import os
import unittest
import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgres://postgres:postgres@localhost:5432/testdb"
        self.db = SQLAlchemy()
        setup_db(self.app, self.database_path)
        
        self.new_trivia = {
            'question': 'QUESTION',
            'answer': 'ANSWER',
            'category': 1,
            'difficulty': 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

   #=======================#
   #     GET QUESTIONS     #
   #=======================#

    # Test get_questions

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertEqual(data['current_category'], None)
        self.assertGreaterEqual(data['total_questions'], len(data['questions']))


    # Test get_questions 404 error

    def test_get_questions_404(self):
        res = self.client().get('/questions?page=500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    #=======================#
    #    DELETE QUESTION    #
    #=======================#

    # Test delete_question

    def test_delete_question(self):
        
        # adding a new trivia
        
        with self.app.app_context():
            trivia = Question(
                question = 'QUESTION',
                answer = 'ANSWER',
                difficulty = 1,
                category = 1
            )
            self.db.session.add(trivia)
            self.db.session.commit()

        # retrieving the just created trivia to get the id

        trivia_temp = Question.query.filter_by(question = 'QUESTION').one()
        trivia_id = trivia_temp.id

        # starting the test requesting a delete method on /questions/trivia_id
        # for the trivia just created

        res = self.client().delete(f'/questions/{trivia_id}')
        data = json.loads(res.data)
        
        # checking if the trivia_id is still in the database
        is_id_still_present = Question.query.get(trivia_id)
        
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_id'], trivia_temp.id)
        self.assertFalse(is_id_still_present, False)

    # Test delete_question_404

    def test_delete_question_404(self):
        res = self.client().get('question/400')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    #=======================#
    #    POST QUESTION      #
    #=======================#


    # Test post_question

    def test_post_question(self):
        res = self.client().post('/questions')
        data = json.load(res.data)
        
        is_id_present = Question.query.get(data['posted_id'])

        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(data['posted_id'], int)
        self.assertTrue(is_id_present, 'checking if new id is present')


    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()