import io
import sys
from main import print_hi, print_bye


def test_print_hi():
    """测试 print_hi 函数输出正确的问候语。"""
    captured_output = io.StringIO()
    sys.stdout = captured_output
    print_hi("Test")
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == "Hi, Test"


def test_print_bye():
    """测试 print_bye 函数输出正确的告别语。"""
    captured_output = io.StringIO()
    sys.stdout = captured_output
    print_bye("Test")
    sys.stdout = sys.__stdout__
    assert captured_output.getvalue().strip() == "Bye, Test"
