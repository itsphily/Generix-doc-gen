import os

from dotenv import load_dotenv
from openai import OpenAI

import typer

from docgen import display
from docgen.constants import EXIT_ERROR

# Load environment variables from .env file
load_dotenv()


def _get_client() -> OpenAI:
    """Create an OpenAI client. Uses OPENAI_API_KEY env var."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        display.error("OPENAI_API_KEY environment variable is not set")
        raise typer.Exit(EXIT_ERROR)
    return OpenAI(api_key=api_key)


def generate_documentation(source_code: str, filename: str) -> str:
    """Generate markdown documentation for source code using an LLM.

    Args:
        source_code: The contents of the source file.
        filename: The name of the source file (for context).

    Returns:
        Generated markdown documentation as a string.
    """
    client = _get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a technical documentation writer. "
                "Generate clear, comprehensive markdown documentation "
                "for the provided source code. Include: overview, "
                "functions/classes, parameters, return values, and usage examples.",
            },
            {
                "role": "user",
                "content": f"Generate documentation for `{filename}`:\n\n```\n{source_code}\n```",
            },
        ],
    )

    return response.choices[0].message.content


def check_accuracy(source_code: str, existing_docs: str) -> str:
    """Check if existing documentation is still accurate for the current source code.

    Args:
        source_code: The current contents of the source file.
        existing_docs: The existing markdown documentation.

    Returns:
        An accuracy report as a string.
    """
    client = _get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a documentation reviewer. Compare the source code "
                "against the existing documentation. Report any inaccuracies, "
                "missing items, or outdated information. Be concise.",
            },
            {
                "role": "user",
                "content": f"Source code:\n```\n{source_code}\n```\n\n"
                f"Existing documentation:\n{existing_docs}",
            },
        ],
    )

    return response.choices[0].message.content


def generate_summary(source_code: str, filename: str) -> str:
    """Generate a one-paragraph summary of source code using an LLM.

    Args:
        source_code: The contents of the source file.
        filename: The name of the source file (for context).

    Returns:
        A one-paragraph summary as a string.
    """
    client = _get_client()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a technical writer. Generate a single concise "
                "paragraph summarizing what the provided source code does. "
                "Focus on purpose, key functionality, and important details.",
            },
            {
                "role": "user",
                "content": f"Summarize `{filename}`:\n\n```\n{source_code}\n```",
            },
        ],
    )

    return response.choices[0].message.content
