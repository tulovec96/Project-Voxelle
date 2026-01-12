"""
Unit Tests for Voxelle Exception System

Tests for all custom exception classes to ensure proper error handling
and exception hierarchy.
"""

import pytest
from src.utils.exceptions import (
    VoxelleException,
    JobNotFoundError,
    InvalidJobTypeError,
    ConfigValidationError,
    InvalidInputError,
    UnknownOperationIDError,
    OperationAlreadyActiveError,
)


class TestExceptionBasics:
    """Test base exception class."""
    
    def test_voxelle_exception_creation(self):
        """Test creating a basic VoxelleException."""
        exc = VoxelleException("Test error")
        assert str(exc) == "Test error"
        assert exc.message == "Test error"
        assert exc.context == {}
    
    def test_voxelle_exception_with_context(self):
        """Test VoxelleException with context."""
        context = {"job_id": "123", "action": "start"}
        exc = VoxelleException("Test error", context)
        assert exc.context == context


class TestJobExceptions:
    """Test job-related exceptions."""
    
    def test_job_not_found_error(self):
        """Test JobNotFoundError."""
        exc = JobNotFoundError("job_123")
        assert "job_123" in str(exc)
        assert exc.job_id == "job_123"
    
    def test_invalid_job_type_error(self):
        """Test InvalidJobTypeError."""
        exc = InvalidJobTypeError("INVALID_TYPE")
        assert "INVALID_TYPE" in str(exc)
        assert exc.job_type == "INVALID_TYPE"


class TestConfigExceptions:
    """Test configuration-related exceptions."""
    
    def test_config_validation_error(self):
        """Test ConfigValidationError."""
        exc = ConfigValidationError("field_name", "bad_value", "must be a number")
        assert "field_name" in str(exc)
        assert "bad_value" in str(exc)
        assert exc.field == "field_name"
        assert exc.value == "bad_value"


class TestInputExceptions:
    """Test input-related exceptions."""
    
    def test_invalid_input_error_basic(self):
        """Test InvalidInputError basic creation."""
        exc = InvalidInputError("email", "must be a valid email")
        assert "email" in str(exc)
        assert exc.field == "email"
    
    def test_invalid_input_error_with_value(self):
        """Test InvalidInputError with value."""
        exc = InvalidInputError("age", "must be positive", value=-5)
        assert "-5" in str(exc)
        assert exc.value == -5


class TestOperationExceptions:
    """Test operation-related exceptions."""
    
    def test_unknown_operation_id_error(self):
        """Test UnknownOperationIDError."""
        exc = UnknownOperationIDError("op_123")
        assert "op_123" in str(exc)
        assert exc.op_id == "op_123"
    
    def test_operation_already_active_error(self):
        """Test OperationAlreadyActiveError."""
        exc = OperationAlreadyActiveError("TTS", "tts_openai")
        assert "TTS" in str(exc)
        assert "tts_openai" in str(exc)
        assert exc.op_type == "TTS"
        assert exc.op_id == "tts_openai"


class TestExceptionHierarchy:
    """Test exception inheritance."""
    
    def test_job_exception_is_voxelle_exception(self):
        """Test that JobNotFoundError is a VoxelleException."""
        exc = JobNotFoundError("test_id")
        assert isinstance(exc, VoxelleException)
    
    def test_operation_exception_is_voxelle_exception(self):
        """Test that operation exceptions are VoxelleExceptions."""
        exc = UnknownOperationIDError("test_id")
        assert isinstance(exc, VoxelleException)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
