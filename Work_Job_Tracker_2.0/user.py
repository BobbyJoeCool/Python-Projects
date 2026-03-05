"""User domain model.

This module contains the minimal authenticated user context that is passed
throughout the application.

Note:
    For now, the user model contains only the username/zNumber. Role-based
    authorization can be added later.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """Authenticated user context.

    Args:
        zNumber: The user's username (zNumber).
    """

    zNumber: str
    # TODO: Add role/permissions fields (user/manager/admin) for access control.
