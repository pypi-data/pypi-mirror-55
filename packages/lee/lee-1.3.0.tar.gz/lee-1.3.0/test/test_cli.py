from core.cli import Cli
from core.enhancer import Enhancer
import os
from main import main,createParse
# from core.main_args import  createParse
import pytest

@pytest.fixture
def parser():
    return  createParse()

# def test_questions(parser):
#     args = parser.parse_args(['q', '-dg'])
#     c = Cli(args)
#     json = c.questions()
#     print(json)

# def test_shell():
#     json = c.shell()
#     pass


# def test_algorithms():
#     json = c.algorithms()
#     pass


# def test_database():
#     json = c.database()
#     pass


# def test_save_question_to_local():
#     #     r = c.questions()
#     #     r = c.questions()
#     #     r = c.questions()
#     #     r = c.questions()
#     #     r = c.questions()
#     #     r = c.questions()
#     pass


# def test_test_question_to_cloud():
#     pass


# def test_submit_question_to_cloud():
#     pass


# def test_show_question_solution_from_cloud():
#     pass
