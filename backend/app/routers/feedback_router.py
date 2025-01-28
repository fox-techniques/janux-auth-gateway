"""
routers.py

Defines API routes for feedback-related operations.

Endpoints:
- `/submit`: Submit feedback.
- `/list`: List all feedback (Admin-only).

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.models.feedback import Feedback
from app.auth.jwt import get_current_user, get_current_admin
from app.logging.custom_logger import get_logger

# Initialize logger
logger = get_logger("feedback_service_logger")

# Initialize router
feedback_router = APIRouter()


@feedback_router.post(
    "/submit",
    response_model=FeedbackResponse,
    status_code=status.HTTP_201_CREATED,
)
async def submit_feedback(
    feedback: FeedbackCreate, current_user: dict = Depends(get_current_user)
):
    """
    Submit feedback from a logged-in user.

    Args:
        feedback (FeedbackCreate): The feedback details.
        current_user (dict): The currently authenticated user (injected by `get_current_user`).

    Returns:
        FeedbackResponse: The saved feedback details.
    """
    logger.info(f"User {current_user['username']} is submitting feedback.")

    feedback_entry = Feedback(
        user_id=current_user["username"],
        emoji=feedback.emoji,
        rating=feedback.rating,
        comment=feedback.comment,
    )
    await feedback_entry.insert()

    logger.info(f"Feedback submitted by user {current_user['username']}.")
    return FeedbackResponse(
        id=str(feedback_entry.id),
        emoji=feedback_entry.emoji,
        rating=feedback_entry.rating,
        comment=feedback_entry.comment,
        created_at=feedback_entry.created_at,
    )


@feedback_router.get(
    "/list",
    response_model=List[FeedbackResponse],
    status_code=status.HTTP_200_OK,
)
async def list_feedback(current_admin: dict = Depends(get_current_admin)):
    """
    List all feedback (Admin-only route).

    Args:
        current_admin (dict): The currently authenticated admin (injected by `get_current_admin`).

    Returns:
        List[FeedbackResponse]: A list of all feedback entries.
    """
    logger.info(f"Admin {current_admin['username']} is listing all feedback.")

    feedback_entries = await Feedback.find_all().to_list()
    return [
        FeedbackResponse(
            id=str(entry.id),
            emoji=entry.emoji,
            rating=entry.rating,
            comment=entry.comment,
            created_at=entry.created_at,
        )
        for entry in feedback_entries
    ]
