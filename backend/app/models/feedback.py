"""
user.py

Defines the Feedback model for MongoDB using Beanie

Features:
- Stores user details such as id, emoji, rating, and comment.
- Automatically sets the creation timestamp for new users.
- Uses unique constraints and Pydantic for validation.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from beanie import Document
from pydantic import Field
from datetime import datetime, timezone
from typing import Optional


class Feedback(Document):
    """
    Beanie model for the Feedback collection in MongoDB.

    Attributes:
        user_id (str): The ID of the user providing the feedback.
        emoji (str): The emoji submitted as feedback (e.g., ":smile:").
        rating (int): The numeric rating provided by the user (1-5).
        comment (Optional[str]): An optional comment from the user.
        created_at (datetime): The timestamp of when the feedback was created.
    """

    user_id: str = Field(..., example="507f1f77bcf86cd799439011")
    emoji: str = Field(..., example=":smile:")
    rating: int = Field(..., ge=1, le=5, example=5)
    comment: Optional[str] = Field(None, example="Great service!")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        """
        Settings for the MongoDB collection for feedback.
        """

        collection = "feedbacks"

    class Config:
        """
        Pydantic model configuration for JSON serialization and schema.
        """

        json_schema_extra = {
            "example": {
                "user_id": "507f1f77bcf86cd799439011",
                "emoji": ":smile:",
                "rating": 5,
                "comment": "Great service!",
                "created_at": "2025-01-28T12:00:00Z",
            }
        }
