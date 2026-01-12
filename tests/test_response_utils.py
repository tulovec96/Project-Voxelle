"""
Unit Tests for Response Utilities

Tests for API response creation and manipulation.
"""

import pytest
from src.utils.response_utils import (
    StatusCode,
    ResponseStatus,
    create_success_response,
    create_error_response,
    create_paginated_response,
    is_success_response,
    is_error_response,
)


class TestSuccessResponses:
    """Test success response creation."""
    
    def test_create_success_response_basic(self):
        """Test basic success response."""
        response = create_success_response(data={"key": "value"})
        
        assert response["status"] == 200
        assert response["status_enum"] == ResponseStatus.SUCCESS.value
        assert response["data"] == {"key": "value"}
        assert is_success_response(response)
    
    def test_create_success_response_custom_code(self):
        """Test success response with custom status code."""
        response = create_success_response(
            data={"id": "123"},
            status_code=StatusCode.CREATED.value
        )
        assert response["status"] == 201


class TestErrorResponses:
    """Test error response creation."""
    
    def test_create_error_response_basic(self):
        """Test basic error response."""
        response = create_error_response("Something went wrong")
        
        assert response["status"] == 500
        assert response["status_enum"] == ResponseStatus.ERROR.value
        assert "Something went wrong" in response["message"]
        assert is_error_response(response)
    
    def test_create_error_response_with_exception(self):
        """Test error response from exception."""
        exc = ValueError("Invalid input")
        response = create_error_response(exc, status_code=400)
        
        assert response["status"] == 400
        assert "Invalid input" in response["message"]
        assert response["error_type"] == "ValueError"
    
    def test_create_error_response_with_details(self):
        """Test error response with details."""
        response = create_error_response(
            "Validation failed",
            status_code=400,
            error_type="ValidationError",
            details={"field": "email", "reason": "invalid format"}
        )
        
        assert response["details"]["field"] == "email"


class TestPaginatedResponses:
    """Test paginated response creation."""
    
    def test_create_paginated_response(self):
        """Test paginated response."""
        items = [{"id": 1}, {"id": 2}]
        response = create_paginated_response(
            items=items,
            page=1,
            page_size=10,
            total=25
        )
        
        assert response["data"] == items
        assert response["pagination"]["page"] == 1
        assert response["pagination"]["total"] == 25
        assert response["pagination"]["total_pages"] == 3
        assert response["pagination"]["has_next"] is True
        assert response["pagination"]["has_prev"] is False
    
    def test_paginated_response_last_page(self):
        """Test paginated response on last page."""
        response = create_paginated_response(
            items=[],
            page=3,
            page_size=10,
            total=25
        )
        
        assert response["pagination"]["has_next"] is False
        assert response["pagination"]["has_prev"] is True


class TestResponseHelpers:
    """Test response helper functions."""
    
    def test_is_success_response(self):
        """Test is_success_response function."""
        success_resp = create_success_response()
        error_resp = create_error_response("Error")
        
        assert is_success_response(success_resp)
        assert not is_success_response(error_resp)
    
    def test_is_error_response(self):
        """Test is_error_response function."""
        success_resp = create_success_response()
        error_resp = create_error_response("Error")
        
        assert not is_error_response(success_resp)
        assert is_error_response(error_resp)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
