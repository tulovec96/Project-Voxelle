"""
Input Validation Utilities for Voxelle

Provides validation functions for API inputs, configuration, and common data types.
Centralizes validation logic for consistency and reusability.
"""

from typing import Any, Optional, List, Dict, Union, Type, Callable
import re
from pathlib import Path

from .exceptions import (
    InvalidInputError,
    MissingRequiredFieldError,
    DataValidationError,
)


def validate_required(data: Dict[str, Any], *fields: str) -> None:
    """
    Validate that required fields exist in a dictionary.
    
    Args:
        data: Dictionary to validate
        *fields: Field names that are required
        
    Raises:
        MissingRequiredFieldError: If any required field is missing
    """
    for field in fields:
        if field not in data or data[field] is None:
            raise MissingRequiredFieldError(field)


def validate_type(
    value: Any,
    expected_type: Union[Type, tuple],
    field_name: str = "value",
) -> None:
    """
    Validate that a value is of the expected type.
    
    Args:
        value: Value to validate
        expected_type: Expected type or tuple of types
        field_name: Name of the field for error messages
        
    Raises:
        DataValidationError: If type validation fails
    """
    if not isinstance(value, expected_type):
        if isinstance(expected_type, tuple):
            expected_str = " or ".join(t.__name__ for t in expected_type)
        else:
            expected_str = expected_type.__name__
        raise DataValidationError(field_name, expected_str, value)


def validate_string(
    value: Any,
    field_name: str = "value",
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[str] = None,
    allowed_values: Optional[List[str]] = None,
) -> str:
    """
    Validate a string value with various constraints.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        min_length: Minimum string length
        max_length: Maximum string length
        pattern: Regex pattern the string must match
        allowed_values: List of allowed string values
        
    Returns:
        Validated string value
        
    Raises:
        DataValidationError: If validation fails
    """
    validate_type(value, str, field_name)
    
    if min_length is not None and len(value) < min_length:
        raise InvalidInputError(
            field_name,
            f"must be at least {min_length} characters long",
            value,
        )
    
    if max_length is not None and len(value) > max_length:
        raise InvalidInputError(
            field_name,
            f"must be at most {max_length} characters long",
            value,
        )
    
    if pattern is not None and not re.match(pattern, value):
        raise InvalidInputError(
            field_name,
            f"must match pattern: {pattern}",
            value,
        )
    
    if allowed_values is not None and value not in allowed_values:
        raise InvalidInputError(
            field_name,
            f"must be one of: {', '.join(allowed_values)}",
            value,
        )
    
    return value


def validate_integer(
    value: Any,
    field_name: str = "value",
    min_value: Optional[int] = None,
    max_value: Optional[int] = None,
) -> int:
    """
    Validate an integer value with optional bounds.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        
    Returns:
        Validated integer value
        
    Raises:
        DataValidationError: If validation fails
    """
    validate_type(value, int, field_name)
    
    if min_value is not None and value < min_value:
        raise InvalidInputError(
            field_name,
            f"must be at least {min_value}",
            value,
        )
    
    if max_value is not None and value > max_value:
        raise InvalidInputError(
            field_name,
            f"must be at most {max_value}",
            value,
        )
    
    return value


def validate_float(
    value: Any,
    field_name: str = "value",
    min_value: Optional[float] = None,
    max_value: Optional[float] = None,
) -> float:
    """
    Validate a float value with optional bounds.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        min_value: Minimum allowed value
        max_value: Maximum allowed value
        
    Returns:
        Validated float value
        
    Raises:
        InvalidInputError: If validation fails
    """
    validate_type(value, (int, float), field_name)
    value = float(value)
    
    if min_value is not None and value < min_value:
        raise InvalidInputError(
            field_name,
            f"must be at least {min_value}",
            value,
        )
    
    if max_value is not None and value > max_value:
        raise InvalidInputError(
            field_name,
            f"must be at most {max_value}",
            value,
        )
    
    return value


def validate_list(
    value: Any,
    field_name: str = "value",
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    item_validator: Optional[Callable[[Any], Any]] = None,
) -> list:
    """
    Validate a list value.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        min_length: Minimum list length
        max_length: Maximum list length
        item_validator: Optional function to validate each item
        
    Returns:
        Validated list
        
    Raises:
        DataValidationError: If validation fails
    """
    validate_type(value, list, field_name)
    
    if min_length is not None and len(value) < min_length:
        raise InvalidInputError(
            field_name,
            f"must have at least {min_length} items",
            value,
        )
    
    if max_length is not None and len(value) > max_length:
        raise InvalidInputError(
            field_name,
            f"must have at most {max_length} items",
            value,
        )
    
    if item_validator is not None:
        value = [item_validator(item) for item in value]
    
    return value


def validate_dict(
    value: Any,
    field_name: str = "value",
    required_keys: Optional[List[str]] = None,
) -> dict:
    """
    Validate a dictionary value.
    
    Args:
        value: Value to validate
        field_name: Name of the field for error messages
        required_keys: Optional list of required keys
        
    Returns:
        Validated dictionary
        
    Raises:
        DataValidationError: If validation fails
    """
    validate_type(value, dict, field_name)
    
    if required_keys:
        missing = [k for k in required_keys if k not in value]
        if missing:
            raise InvalidInputError(
                field_name,
                f"missing required keys: {', '.join(missing)}",
            )
    
    return value


def validate_file_path(
    value: Any,
    field_name: str = "file_path",
    must_exist: bool = False,
    must_be_file: bool = False,
    must_be_dir: bool = False,
) -> Path:
    """
    Validate a file path.
    
    Args:
        value: Path value to validate
        field_name: Name of the field for error messages
        must_exist: Whether the path must exist
        must_be_file: Whether the path must be a file
        must_be_dir: Whether the path must be a directory
        
    Returns:
        Validated Path object
        
    Raises:
        InvalidInputError: If validation fails
    """
    validate_type(value, (str, Path), field_name)
    path = Path(value)
    
    if must_exist and not path.exists():
        raise InvalidInputError(
            field_name,
            "path does not exist",
            value,
        )
    
    if must_be_file and not path.is_file():
        raise InvalidInputError(
            field_name,
            "path must be a file",
            value,
        )
    
    if must_be_dir and not path.is_dir():
        raise InvalidInputError(
            field_name,
            "path must be a directory",
            value,
        )
    
    return path.resolve()


def validate_email(value: Any, field_name: str = "email") -> str:
    """
    Validate an email address.
    
    Args:
        value: Email value to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated email address
        
    Raises:
        InvalidInputError: If validation fails
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return validate_string(
        value,
        field_name,
        pattern=email_pattern,
    )


def validate_url(value: Any, field_name: str = "url") -> str:
    """
    Validate a URL.
    
    Args:
        value: URL value to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated URL
        
    Raises:
        InvalidInputError: If validation fails
    """
    url_pattern = r'^https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)$'
    return validate_string(
        value,
        field_name,
        pattern=url_pattern,
    )


def validate_uuid(value: Any, field_name: str = "uuid") -> str:
    """
    Validate a UUID.
    
    Args:
        value: UUID value to validate
        field_name: Name of the field for error messages
        
    Returns:
        Validated UUID string
        
    Raises:
        InvalidInputError: If validation fails
    """
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return validate_string(
        value,
        field_name,
        pattern=uuid_pattern,
    )


__all__ = [
    "validate_required",
    "validate_type",
    "validate_string",
    "validate_integer",
    "validate_float",
    "validate_list",
    "validate_dict",
    "validate_file_path",
    "validate_email",
    "validate_url",
    "validate_uuid",
]
