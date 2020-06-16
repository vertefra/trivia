import os
import unittest
import json
from flask import Flask, jsonify
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
    #    GET CATEGORIES     #
    #=======================#

    # test get_category

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['categories'],[])
        self.assertIsInstance(data['total_categories'], int)


    #=======================#
    #    DELETE QUESTION    #
    #=======================#

    # Test delete_question

    def test_delete_question(self):
        
        # adding a new trivia to test delete request
        
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
        res = self.client().post('/questions', json= (self.new_trivia))
        data = json.loads(res.data)

        
        #looking if the new entry has been created
        new_trivia = Question.query.filter_by(question='QUESTION').one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(new_trivia)


    #=======================#
    #    SEARCH QUESTIONS   #
    #=======================#

    # Test search_question_found

    def test_search_question_found(self):
       
        #Creating a trivia test

        with self.app.app_context():
            trivia = Question(
                question = 'QUESTION',
                answer = 'ANSWER',
                difficulty = 1,
                category = 1
            )
            self.db.session.add(trivia)
            self.db.session.commit()

        res = self.client().post('/question', json={"searchTerm": "QUEST"})
        data = json.loads(res.data)


        self.assertEqual(res.status_code,200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 1)
        self.assertEqual(data['questions'][0]['answer'], 'ANSWER')


    # Test search_question_not_found

    def test_search_question_not_found(self):
        
        #Creating a trivia test

        with self.app.app_context():
            trivia = Question(
                question = 'QUESTION',
                answer = 'ANSWER',
                difficulty = 1,
                category = 1
            )
            self.db.session.add(trivia)
            self.db.session.commit()

        res = self.client().post('/question', json={"searchTerm": "XXXXXXXXXXX"})
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        
    #=======================#
    # GET QUESTIONS BY CAT. #
    #=======================#

    # Test get_questions_by_category

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)


        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['questions'], [])
        self.assertEqual(data['current_category'], 'Science')
        self.assertNotEqual(data['categories'], {})


    #Test get_questions_by_category_404

    def test_get_questions_by_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertNotEqual(data['questions'], [])
        self.assertEqual(data['current_category'], 'Science')
        self.assertNotEqual(data['categories'], {})


    # Test get_random_quesiton

    # Case with no previous question
    def test_get_random_question(self):
        res = self.client().post('/quizzes', json = { 
                                                'quiz_category': { 
                                                        'id': 1, 
                                                        'type': 'Science' 
                                                        },
                                                'previous_questions': []                                                      
                                                            })
        data = json.loads(res.data)

        print('Data' ,data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['current_category'], 1)
        self.assertEqual(data['question']['category'], 1)

    # Case with depleted avaiable questions        

        res = self.client().post('/quizzes', json = {
                                                'quiz_category': { 
                                                        'id': 1, 
                                                        'type': 'Science' 
                                                        },
                                                'previous_questions': ['q1','q2','q3'] 
        })

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

        # question should be false to trgger forceEnd
        self.assertEqual(data['question'], False)
        self.assertEqual(data['current_category'], 1)


    def tearDown(self):
        with self.app.app_context():

            # Clearing test questions if they are present

            print('Executing TearDown: ')
            test_questions = Question.query.filter_by(question='QUESTION').one_or_none()
            print('Test question found')
            if (test_questions):
                try:
                    test_questions.delete()
                    self.db.session.commit()
                    print('test questions cleared')
                except:
                    self.db.session.rollback()
                    print('An error occurred. probably you have some test question to clear manually from testdb')
            else: 
                print('No test question for this test')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()