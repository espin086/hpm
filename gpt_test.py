"""

Test the GPT-3 API
"""

from gpt import generate_completion


def test_generate_completion():
    """
    Function should return a string
    """
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
