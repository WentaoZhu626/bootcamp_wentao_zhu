import os

from dotenv import load_dotenv


def load_env() -> None:
    """Load environment variables from the nearest .env file."""
    load_dotenv()


def get_key(key_name: str) -> str | None:
    """Return an environment variable by name."""
    return os.getenv(key_name)