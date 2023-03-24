import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # test for get paginated questions
    # test def paginated_questions(request, selection):

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['current_questions'])

    # test for get categories
    # test @app.route('/categories', methods=['GET'])
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])

    # failed test for get categories
    # @app.route('/categories', methods=['POST'])
    def test_for_unavailable_categories(self):
        res = self.client().post('/categories?')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['categories'], 'error')
        self.assertEqual(data['message'], 'Not Found!')

    # test for get questions
    # @app.route('/questions', methods=['GET'])
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])

    # failed test for get questions
    # test - @app.route('/questions', methods=['POST'])
    def test_for_unavailable_questions(self):
        res = self.client().post('/questions?')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['questions'], 'error')
        self.assertEqual(data['message'], 'Not Found!')

    # test to delete a questions
    # @app.route('/questions/<int:id>', methods=['DELETE'])
    def test_delete_question(self):
        res = self.client().delete('/questions/')
        question = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(question, None)

    # failed test to delete question
    # @app.route('/questions/<int:id>', methods=['DELETE'])
    def test_questions_does_not_exist_404(self):
        res = self.client().delete('/questions/555')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found!')

    # create new question test
    # @app.route('/questions', methods=['POST'])
    def test_create_new_question(self):
        res = self.client().post('/questions', json={
            'question': 'How many days are in a leap year',
            'answer': '366',
            'difficulty': 2,
            'category': 1
        })
        self.assertEqual(res.status_code, 200)

    # failed test new questions post (missing question info)
    # @app.route('/questions', methods=['POST'])
    def test_fail_new_question(self):
        res = self.client().post('/questions', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found!')

    # question search test
    # @app.route('/questions/search', methods=['POST'])
    def test_question_search(self):
        res = self.client().post('/questions/search',
                                 json={'searchTerm': 'blanket'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['current_questions'], 0)

    # question search fail test
    # @app.route('/questions/search', methods=['POST'])
    def failed_question_search(self):
        res = self.client().post('/questions/search',
                                 json={'search_term': 'bleepbleep'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['current_question'], 0)
        self.assertEqual(data['message'], 'Not Found!')

    # test questions by category id
    # @app.route('/categories/<int:id>', methods=['GET'])
    def test_get_question_by_categories(self):
        res = self.client().get(f'/categories/{id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(len(data['total_questions']))
        self.assertEqual(data['current_category'], '')

    # failed test questions by category id
    # @app.route('/categories/<int:id>', methods=['GET'])
    def failed_test_get_question_by_categories(self):
        id = 250
        res = self.client().get(f'/categories/{id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found!')

    # test quiz post
    # @app.route('/quizzes', methods=['POST'])
    def test_start_quiz(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question']['category'])

    # test quiz fail
    # @app.route('/quizzes', methods=['POST'])
    def test_quiz_fail(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request!')


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
