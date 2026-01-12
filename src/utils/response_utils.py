"""
HTTP Response Utilities for Voxelle

Provides standardized response formatting for all API endpoints,
ensuring consistent error and success responses.
"""

from typing import Any, Dict, Optional, Union
from enum import Enum
import json


class StatusCode(Enum):
    """Standard HTTP status codes."""
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    RATE_LIMITED = 429
    INTERNAL_ERROR = 500
    SERVICE_UNAVAILABLE = 503


class ResponseStatus(Enum):
    """Application response status indicators."""
    SUCCESS = "success"
    ERROR = "error"
    PARTIAL = "partial"


def create_success_response(
    data: Any = None,
    message: str = "Operation completed successfully",
    status_code: int = StatusCode.OK.value,
) -> Dict[str, Any]:
    """
    Create a standardized success response.
    
    Args:
        data: Response data/payload
        message: Human-readable success message
        status_code: HTTP status code
        
    Returns:
        Standardized response dictionary
    """
    return {
        "status": status_code,
        "status_enum": ResponseStatus.SUCCESS.value,
        "message": message,
        "data": data,
    }


def create_error_response(
    error: Union[str, Exception],
    status_code: int = StatusCode.INTERNAL_ERROR.value,
    error_type: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Create a standardized error response.
    
    Args:
        error: Error message or exception
        status_code: HTTP status code
        error_type: Type of error (e.g., "ValidationError", "NotFoundError")
        details: Additional error details
        
    Returns:
        Standardized error response dictionary
    """
    error_message = str(error)
    if error_type is None and hasattr(error, '__class__'):
        error_type = error.__class__.__name__
    
    return {
        "status": status_code,
        "status_enum": ResponseStatus.ERROR.value,
        "message": error_message,
        "error_type": error_type,
        "details": details or {},
    }


def create_partial_response(
    data: Any = None,
    message: str = "Operation partially completed",
    warnings: Optional[list] = None,
    status_code: int = StatusCode.ACCEPTED.value,
) -> Dict[str, Any]:
    """
    Create a response for partially completed operations.
    
    Args:
        data: Response data/payload
        message: Message describing the partial completion
        warnings: List of warnings encountered
        status_code: HTTP status code
        
    Returns:
        Standardized partial response dictionary
    """
    return {
        "status": status_code,
        "status_enum": ResponseStatus.PARTIAL.value,
        "message": message,
        "data": data,
        "warnings": warnings or [],
    }


def create_paginated_response(
    items: list,
    page: int,
    page_size: int,
    total: int,
    message: str = "Items retrieved successfully",
) -> Dict[str, Any]:
    """
    Create a paginated response.
    
    Args:
        items: List of items for this page
        page: Current page number (1-indexed)
        page_size: Items per page
        total: Total number of items
        message: Response message
        
    Returns:
        Standardized paginated response
    """
    total_pages = (total + page_size - 1) // page_size
    
    return {
        "status": StatusCode.OK.value,
        "status_enum": ResponseStatus.SUCCESS.value,
        "message": message,
        "data": items,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        },
    }


def is_success_response(response: Dict[str, Any]) -> bool:
    """Check if a response indicates success."""
    return response.get("status_enum") == ResponseStatus.SUCCESS.value


def is_error_response(response: Dict[str, Any]) -> bool:
    """Check if a response indicates an error."""
    return response.get("status_enum") == ResponseStatus.ERROR.value


def is_partial_response(response: Dict[str, Any]) -> bool:
    """Check if a response indicates partial completion."""
    return response.get("status_enum") == ResponseStatus.PARTIAL.value


def get_response_status_code(response: Dict[str, Any]) -> int:
    """Extract the HTTP status code from a response."""
    return response.get("status", StatusCode.INTERNAL_ERROR.value)


def get_response_message(response: Dict[str, Any]) -> str:
    """Extract the message from a response."""
    return response.get("message", "")


def get_response_data(response: Dict[str, Any]) -> Any:
    """Extract the data payload from a response."""
    return response.get("data")


def get_response_error_type(response: Dict[str, Any]) -> Optional[str]:
    """Extract the error type from an error response."""
    return response.get("error_type")


__all__ = [
    "StatusCode",
    "ResponseStatus",
    "create_success_response",
    "create_error_response",
    "create_partial_response",
    "create_paginated_response",
    "is_success_response",
    "is_error_response",
    "is_partial_response",
    "get_response_status_code",
    "get_response_message",
    "get_response_data",
    "get_response_error_type",
]
