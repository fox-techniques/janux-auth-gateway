"""
services.py

Contains reusable business logic for feedback-related operations.

Author: FOX Techniques <ali.nabbi@fox-techniques.com>
"""

from app.models.feedback import Feedback
from app.logging.custom_logger import get_logger

# Initialize logger
logger = get_logger("feedback_service_logger")


async def save_feedback(user_id: str, emoji: str, rating: int, comment: str = None):
    """
    Save a feedback entry to the database.

    Args:
        user_id (str): The ID of the user providing the feedback.
        emoji (str): The emoji submitted as feedback.
        rating (int): The numeric rating provided by the user (1-5).
        comment (str, optional): An optional comment from the user. Defaults to None.

    Returns:
        Feedback: The saved feedback entry.
    """
    logger.info(f"Saving feedback for user {user_id}.")

    feedback_entry = Feedback(
        user_id=user_id,
        emoji=emoji,
        rating=rating,
        comment=comment,
    )
    await feedback_entry.insert()
    logger.info(f"Feedback saved for user {user_id} with ID {feedback_entry.id}.")
    return feedback_entry


async def get_all_feedback():
    """
    Retrieve all feedback entries from the database.

    Returns:
        list[Feedback]: A list of all feedback entries.
    """
    logger.info("Fetching all feedback entries.")

    feedback_entries = await Feedback.find_all().to_list()
    logger.info(f"Retrieved {len(feedback_entries)} feedback entries.")
    return feedback_entries
