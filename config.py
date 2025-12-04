"""Configuration manager untuk LinkedIn Bot."""

import os
from dotenv import load_dotenv


class Config:
    """Static class untuk manage configuration."""

    # Load environment variables
    load_dotenv()

    # LinkedIn credentials
    LINKEDIN_EMAIL: str = os.getenv("LINKEDIN_EMAIL", "")
    LINKEDIN_PASSWORD: str = os.getenv("LINKEDIN_PASSWORD", "")

    # Browser configuration
    BROWSER_PORT: int = int(os.getenv("BROWSER_PORT", "9222"))

    # Session configuration
    SESSION_DIR: str = os.getenv("SESSION_DIR", "./sessions")
