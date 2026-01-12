"""
Voxelle Custom Exception Classes

Provides a comprehensive set of custom exceptions for better error handling
and clearer error messages across the application.
"""

from typing import Optional, Any, Dict


class VoxelleException(Exception):
    """Base exception class for all Voxelle exceptions."""
    
    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None):
        """
        Initialize exception with optional context.
        
        Args:
            message: Human-readable error message
            context: Optional dict with additional error context
        """
        super().__init__(message)
        self.message = message
        self.context = context or {}


# Job-related exceptions
class JobException(VoxelleException):
    """Base exception for job-related errors."""
    pass


class JobNotFoundError(JobException):
    """Raised when a job ID does not exist or has already finished."""
    
    def __init__(self, job_id: str):
        super().__init__(f"Job '{job_id}' not found or already completed")
        self.job_id = job_id


class InvalidJobTypeError(JobException):
    """Raised when an unknown job type is requested."""
    
    def __init__(self, job_type: str):
        super().__init__(f"Unknown job type: '{job_type}'")
        self.job_type = job_type


class JobCancellationError(JobException):
    """Raised when a job is cancelled."""
    
    def __init__(self, job_id: str, reason: Optional[str] = None):
        msg = f"Job '{job_id}' was cancelled"
        if reason:
            msg += f": {reason}"
        super().__init__(msg)
        self.job_id = job_id
        self.reason = reason


# Configuration exceptions
class ConfigException(VoxelleException):
    """Base exception for configuration-related errors."""
    pass


class UnknownConfigFieldError(ConfigException):
    """Raised when accessing an unknown configuration field."""
    
    def __init__(self, field: str):
        super().__init__(f"Configuration field '{field}' does not exist")
        self.field = field


class UnknownConfigFileError(ConfigException):
    """Raised when a configuration file is not found."""
    
    def __init__(self, filepath: str):
        super().__init__(f"Configuration file '{filepath}' not found")
        self.filepath = filepath


class ConfigValidationError(ConfigException):
    """Raised when configuration validation fails."""
    
    def __init__(self, field: str, value: Any, reason: str):
        super().__init__(
            f"Configuration field '{field}' with value '{value}' is invalid: {reason}"
        )
        self.field = field
        self.value = value
        self.reason = reason


# Operation exceptions
class OperationException(VoxelleException):
    """Base exception for operation-related errors."""
    pass


class UnknownOperationTypeError(OperationException):
    """Raised when an unknown operation type is used."""
    
    def __init__(self, op_type: str):
        super().__init__(f"Unknown operation type: '{op_type}'")
        self.op_type = op_type


class UnknownOperationIDError(OperationException):
    """Raised when an operation ID does not exist."""
    
    def __init__(self, op_id: str):
        super().__init__(f"Operation '{op_id}' not found")
        self.op_id = op_id


class UnknownOperationRoleError(OperationException):
    """Raised when an unknown operation role is used."""
    
    def __init__(self, role: str):
        super().__init__(f"Unknown operation role: '{role}'")
        self.role = role


class OperationAlreadyActiveError(OperationException):
    """Raised when trying to start an already active operation."""
    
    def __init__(self, op_type: str, op_id: str):
        super().__init__(f"{op_type} operation '{op_id}' is already active")
        self.op_type = op_type
        self.op_id = op_id


class OperationInactiveError(OperationException):
    """Raised when trying to use an inactive operation."""
    
    def __init__(self, op_type: str, op_id: str, action: str = "use"):
        super().__init__(f"Cannot {action} {op_type} operation '{op_id}': not active")
        self.op_type = op_type
        self.op_id = op_id
        self.action = action


class OperationUnloadedError(OperationException):
    """Raised when trying to use an unloaded operation."""
    
    def __init__(self, op_id: str):
        super().__init__(f"Operation '{op_id}' is not loaded")
        self.op_id = op_id


class DuplicateOperationError(OperationException):
    """Raised when attempting to register a duplicate operation."""
    
    def __init__(self, op_id: str):
        super().__init__(f"Operation '{op_id}' is already registered")
        self.op_id = op_id


# API/Request exceptions
class APIException(VoxelleException):
    """Base exception for API/request-related errors."""
    pass


class InvalidInputError(APIException):
    """Raised when API input validation fails."""
    
    def __init__(self, field: str, reason: str, value: Optional[Any] = None):
        msg = f"Invalid input for field '{field}': {reason}"
        if value is not None:
            msg += f" (got: {value})"
        super().__init__(msg)
        self.field = field
        self.reason = reason
        self.value = value


class MissingRequiredFieldError(APIException):
    """Raised when a required field is missing from request."""
    
    def __init__(self, field: str):
        super().__init__(f"Required field '{field}' is missing")
        self.field = field


class AuthenticationError(APIException):
    """Raised when authentication fails."""
    
    def __init__(self, reason: str = "Authentication failed"):
        super().__init__(reason)


class RateLimitError(APIException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, retry_after: Optional[int] = None):
        msg = "Rate limit exceeded"
        if retry_after:
            msg += f". Retry after {retry_after} seconds"
        super().__init__(msg)
        self.retry_after = retry_after


# Backend service exceptions
class BackendServiceException(VoxelleException):
    """Base exception for backend service errors."""
    pass


class ConnectionError(BackendServiceException):
    """Raised when unable to connect to a backend service."""
    
    def __init__(self, service: str, reason: Optional[str] = None):
        msg = f"Failed to connect to {service}"
        if reason:
            msg += f": {reason}"
        super().__init__(msg)
        self.service = service
        self.reason = reason


class ServiceTimeoutError(BackendServiceException):
    """Raised when a backend service request times out."""
    
    def __init__(self, service: str, timeout: float):
        super().__init__(f"{service} request timed out after {timeout}s")
        self.service = service
        self.timeout = timeout


class ServiceUnavailableError(BackendServiceException):
    """Raised when a required service is unavailable."""
    
    def __init__(self, service: str, status_code: Optional[int] = None):
        msg = f"{service} is unavailable"
        if status_code:
            msg += f" (HTTP {status_code})"
        super().__init__(msg)
        self.service = service
        self.status_code = status_code


# Process exceptions
class ProcessException(VoxelleException):
    """Base exception for process-related errors."""
    pass


class ProcessStartError(ProcessException):
    """Raised when a process fails to start."""
    
    def __init__(self, process_name: str, reason: str):
        super().__init__(f"Failed to start {process_name}: {reason}")
        self.process_name = process_name
        self.reason = reason


class ProcessNotRunningError(ProcessException):
    """Raised when trying to use a process that's not running."""
    
    def __init__(self, process_name: str):
        super().__init__(f"Process '{process_name}' is not running")
        self.process_name = process_name


# Data/Parsing exceptions
class DataException(VoxelleException):
    """Base exception for data-related errors."""
    pass


class DataParsingError(DataException):
    """Raised when data parsing fails."""
    
    def __init__(self, data_type: str, reason: str, raw_data: Optional[Any] = None):
        msg = f"Failed to parse {data_type}: {reason}"
        if raw_data:
            msg += f" (data: {raw_data})"
        super().__init__(msg)
        self.data_type = data_type
        self.reason = reason
        self.raw_data = raw_data


class DataValidationError(DataException):
    """Raised when data validation fails."""
    
    def __init__(self, field: str, expected: str, got: Any):
        super().__init__(
            f"Invalid data for field '{field}': expected {expected}, got {type(got).__name__}"
        )
        self.field = field
        self.expected = expected
        self.got = got


# Integration-specific exceptions
class DiscordException(APIException):
    """Base exception for Discord integration errors."""
    pass


class TwitchException(APIException):
    """Base exception for Twitch integration errors."""
    pass


class VTubeStudioException(APIException):
    """Base exception for VTube Studio integration errors."""
    pass


__all__ = [
    "VoxelleException",
    # Job exceptions
    "JobException",
    "JobNotFoundError",
    "InvalidJobTypeError",
    "JobCancellationError",
    # Config exceptions
    "ConfigException",
    "UnknownConfigFieldError",
    "UnknownConfigFileError",
    "ConfigValidationError",
    # Operation exceptions
    "OperationException",
    "UnknownOperationTypeError",
    "UnknownOperationIDError",
    "UnknownOperationRoleError",
    "OperationAlreadyActiveError",
    "OperationInactiveError",
    "OperationUnloadedError",
    "DuplicateOperationError",
    # API exceptions
    "APIException",
    "InvalidInputError",
    "MissingRequiredFieldError",
    "AuthenticationError",
    "RateLimitError",
    # Backend exceptions
    "BackendServiceException",
    "ConnectionError",
    "ServiceTimeoutError",
    "ServiceUnavailableError",
    # Process exceptions
    "ProcessException",
    "ProcessStartError",
    "ProcessNotRunningError",
    # Data exceptions
    "DataException",
    "DataParsingError",
    "DataValidationError",
    # Integration exceptions
    "DiscordException",
    "TwitchException",
    "VTubeStudioException",
]
