"""Test the 'addition' function in math_operations.py"""
from mock_function import addition


def test_addition_mocked(mocker):
    """This test uses a mock to test the 'addition' function"""
    # Mock the 'addition' function to return 2
    mocker.patch("mock_function.addition", return_value=2)

    result = addition(1, 1)  # This will return 2 because we've mocked it to do so

    assert result == 2, "Expected addition(1, 1) to return 2"
