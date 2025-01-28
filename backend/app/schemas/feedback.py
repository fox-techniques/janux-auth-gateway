"""
feedback.py

Defines Pydantic schemas for feedback-related operations.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FeedbackBase(BaseModel):
    """
    Base schema for feedback details.

    Attributes:
        emoji (str): The emoji submitted as feedback.
        rating (int): The numeric rating provided by the user (1-5).
        comment (Optional[str]): An optional comment from the user.
    """

    emoji: str = Field(..., example=":smile:")
    rating: int = Field(..., ge=1, le=5, example=5)
    comment: Optional[str] = Field(None, example="Great service!")


class FeedbackCreate(FeedbackBase):
    """
    Schema for creating new feedback.

    Extends:
        FeedbackBase

    Attributes:
        user_id (str): The ID of the user providing the feedback.
    """

    user_id: str = Field(..., example="507f1f77bcf86cd799439011")


class FeedbackResponse(FeedbackBase):
    """
    Schema for feedback response data.

    Extends:
        FeedbackBase

    Attributes:
        id (str): The unique identifier for the feedback.
        created_at (datetime): The timestamp of when the feedback was created.
    """

    id: str = Field(..., example="507f1f77bcf86cd799439011")
    created_at: datetime = Field(..., example="2025-01-28T12:00:00Z")
