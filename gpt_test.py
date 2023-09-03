from gpt import generate_completion
import pytest


def test_generate_completion():
    # Arrange
    model = "gpt-3.5-turbo"
    role = """You are a Principal Cloud Architect who is writing a weekly report...
    """
    prompt = "Accomplishments: Did rewroe a pytnon module"

    # Act
    result = generate_completion(model, role, prompt)

    # Assert
    assert isinstance(result, str), "Expected result to be a string"
    assert result != "", "Expected result to be a non-empty string"
