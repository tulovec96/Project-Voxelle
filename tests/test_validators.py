"""
Unit Tests for Voxelle Validators

Tests for all validation functions to ensure proper input validation
and error reporting.
"""

import pytest
from pathlib import Path
from src.utils.validators import (
    validate_required,
    validate_string,
    validate_integer,
    validate_list,
    validate_dict,
    validate_email,
    validate_url,
)
from src.utils.exceptions import (
    MissingRequiredFieldError,
    DataValidationError,
    InvalidInputError,
)


class TestRequiredValidation:
    """Test required field validation."""
    
    def test_validate_required_success(self):
        """Test successful required field validation."""
        data = {"field1": "value1", "field2": "value2"}
        validate_required(data, "field1", "field2")
        # No exception should be raised
    
    def test_validate_required_missing_field(self):
        """Test missing required field."""
        data = {"field1": "value1"}
        with pytest.raises(MissingRequiredFieldError):
            validate_required(data, "field1", "field2")
    
    def test_validate_required_none_value(self):
        """Test None value for required field."""
        data = {"field1": None}
        with pytest.raises(MissingRequiredFieldError):
            validate_required(data, "field1")


class TestStringValidation:
    """Test string validation."""
    
    def test_validate_string_success(self):
        """Test successful string validation."""
        result = validate_string("hello", "test_field")
        assert result == "hello"
    
    def test_validate_string_min_length(self):
        """Test string minimum length validation."""
        with pytest.raises(InvalidInputError):
            validate_string("hi", "test_field", min_length=3)
    
    def test_validate_string_max_length(self):
        """Test string maximum length validation."""
        with pytest.raises(InvalidInputError):
            validate_string("hello world", "test_field", max_length=5)
    
    def test_validate_string_pattern(self):
        """Test string regex pattern validation."""
        # Valid pattern
        validate_string("abc123", "test_field", pattern=r'^[a-z]+\d+$')
        
        # Invalid pattern
        with pytest.raises(InvalidInputError):
            validate_string("123abc", "test_field", pattern=r'^[a-z]+\d+$')
    
    def test_validate_string_allowed_values(self):
        """Test string enumeration validation."""
        validate_string("active", "status", allowed_values=["active", "inactive"])
        
        with pytest.raises(InvalidInputError):
            validate_string("pending", "status", allowed_values=["active", "inactive"])


class TestIntegerValidation:
    """Test integer validation."""
    
    def test_validate_integer_success(self):
        """Test successful integer validation."""
        result = validate_integer(42, "test_field")
        assert result == 42
    
    def test_validate_integer_bounds(self):
        """Test integer bounds validation."""
        validate_integer(50, "test_field", min_value=0, max_value=100)
        
        with pytest.raises(InvalidInputError):
            validate_integer(-1, "test_field", min_value=0)
        
        with pytest.raises(InvalidInputError):
            validate_integer(101, "test_field", max_value=100)
    
    def test_validate_integer_wrong_type(self):
        """Test integer type validation."""
        with pytest.raises(DataValidationError):
            validate_integer("42", "test_field")


class TestListValidation:
    """Test list validation."""
    
    def test_validate_list_success(self):
        """Test successful list validation."""
        result = validate_list([1, 2, 3], "test_field")
        assert result == [1, 2, 3]
    
    def test_validate_list_length(self):
        """Test list length validation."""
        validate_list([1, 2], "test_field", min_length=1, max_length=3)
        
        with pytest.raises(InvalidInputError):
            validate_list([], "test_field", min_length=1)
    
    def test_validate_list_with_item_validator(self):
        """Test list with item validator."""
        validator = lambda x: validate_integer(x, "item")
        result = validate_list([1, 2, 3], "test_field", item_validator=validator)
        assert result == [1, 2, 3]


class TestDictValidation:
    """Test dictionary validation."""
    
    def test_validate_dict_success(self):
        """Test successful dict validation."""
        data = {"key1": "value1", "key2": "value2"}
        result = validate_dict(data, "test_field")
        assert result == data
    
    def test_validate_dict_required_keys(self):
        """Test dict with required keys."""
        data = {"key1": "value1", "key2": "value2"}
        validate_dict(data, "test_field", required_keys=["key1"])
        
        with pytest.raises(InvalidInputError):
            validate_dict(data, "test_field", required_keys=["key1", "key3"])


class TestEmailValidation:
    """Test email validation."""
    
    def test_validate_email_success(self):
        """Test successful email validation."""
        result = validate_email("user@example.com")
        assert result == "user@example.com"
    
    def test_validate_email_failure(self):
        """Test invalid email."""
        with pytest.raises(InvalidInputError):
            validate_email("invalid-email")


class TestURLValidation:
    """Test URL validation."""
    
    def test_validate_url_success(self):
        """Test successful URL validation."""
        result = validate_url("https://example.com/path")
        assert result == "https://example.com/path"
    
    def test_validate_url_failure(self):
        """Test invalid URL."""
        with pytest.raises(InvalidInputError):
            validate_url("not-a-url")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
