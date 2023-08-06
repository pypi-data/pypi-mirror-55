from core.cli import Cli
from core.enhancer import Enhancer
import os
from main import main,createParse
# from core.main_args import  createParse
import pytest
import shutil


@pytest.fixture
def parser():
    return  createParse()



# def test_push(parser):
#     args = parser.parse_args(['push', "1.two-sum.py"])
#     main(args)

# def test_push_test(parser):
#     args = parser.parse_args(['push', "1.two-sum.py","-t"])
#     main(args)
