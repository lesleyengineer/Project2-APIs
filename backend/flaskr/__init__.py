import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginated_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    //DONE! @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r'/*': {'origins': '*'}})
    """
    //DONE! @TODO: Use the after_request decorator to set Access-Control-Allow"""

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()
            if len(categories) == 0:
                abort(404)
            category_options = {}
            for category in categories:
                category_options[category.id] = category.type
            return jsonify({
                'success': True,
                'categories': category_options
            })
        except Exception as e:
            print(e)
            abort

    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            selection = Question.query.order_by(Question.id).all()
            questions = paginated_questions(request, selection)
            if len(questions) == 0:
                abort(404)
            category_options = {}
            categories = Category.query.all()
            for category in categories:
                category_options[category.id] = category.type
            return jsonify({
                'success': True,
                'questions': questions,
                'categories': category_options,
                'total_questions': len(Question.query.all()),
                'current_category': None
            })
        except Exception as e:
            print(e)
            abort

    """
    //DONE! @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    DONE // @TODO:
    Create an endpoint to DELETE question using a question ID.
    """

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        question = Question.query.filter(Question.id == id).one_or_none()
        if question is None:
            abort(404)
        else:
            question.delete()
        return jsonify({
            'success': True,
            'deleted': id
        })

    """
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    DONE! @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        if (new_question is None or new_answer is None or new_difficulty is None or new_category is None):
            abort(404)

        question = Question(question=new_question, answer=new_answer,
                            difficulty=new_difficulty, category=new_category)

        return jsonify({
            'success': True
        })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def questions_search():
        body = request.get_json()

        search_term = body.get('searchterm', None)
        if search_term is None:
            abort(404)

        selection = Question.query.filter(
            Question.question.ilike('%{}%'.format(search_term)))

        current_question = paginated_questions(request, selection)

        return jsonify({

        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>', methods=['GET'])
    def questions_by_category(id):
        category = Category.query.filter(Category.id == id).all()
        questions = Question.query.filter(Question.category == id).all()
        paginated_questions = paginated_questions(request, questions)

        if len(paginated_questions) == 0:
            return abort(404)

        return jsonify({
            'success': 'true',
            'questions': paginated_questions,
            'total_questions': len(questions),
            'current_category': category.type
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def quiz():
        body = request.get_json()

        previous = body.get('previous_question')

        category = body.get('category')

        if (category is None or previous is None):
            abort(400)

        question = Question.query.all(question.id)

        return jsonify({
            'success': True,
            'question': question.format()
        })

    """
    DONE? @TODO:
    Create error handlers for all expected errors
    including 404 and 422
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 400,
            'message': 'BAD REQUEST',
            'success': 'false'
        })

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 404,
            'message': 'NOT FOUND',
            'success': 'false'
        })

    @app.errorhandler(422)
    def unprocessable_content(error):
        return jsonify({
            'error': 422,
            'message': 'UNPROCESSABLE CONTENT',
            'success': 'false'
        })

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'error': 500,
            'message': 'INTERNAL SERVER ERROR',
            'success': 'false'
        })

    return app
