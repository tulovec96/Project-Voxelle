"""
Logging Constants and Utilities for Voxelle

Provides centralized logging configuration and constants for consistency
across the entire application.
"""

from enum import Enum
from typing import Optional
import logging


class LogLevel(Enum):
    """Standard logging levels."""
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class LogCategory(Enum):
    """Log categories for organized logging."""
    STARTUP = "STARTUP"
    SHUTDOWN = "SHUTDOWN"
    JOB = "JOB"
    CONFIG = "CONFIG"
    OPERATION = "OPERATION"
    API = "API"
    DATABASE = "DATABASE"
    CACHE = "CACHE"
    INTEGRATION = "INTEGRATION"
    DISCORD = "DISCORD"
    TWITCH = "TWITCH"
    VTS = "VTS"
    PERFORMANCE = "PERFORMANCE"
    SECURITY = "SECURITY"
    ERROR = "ERROR"
    WARNING = "WARNING"


def get_category_logger(category: LogCategory) -> logging.Logger:
    """
    Get a logger for a specific category.
    
    Args:
        category: LogCategory enum value
        
    Returns:
        Logger instance for the category
    """
    return logging.getLogger(f"voxelle.{category.value.lower()}")


def log_operation_start(
    logger: logging.Logger,
    operation_name: str,
    **context
) -> None:
    """
    Log the start of an operation.
    
    Args:
        logger: Logger instance
        operation_name: Name of the operation
        **context: Additional context information
    """
    context_str = " | ".join(f"{k}={v}" for k, v in context.items())
    msg = f"Starting {operation_name}"
    if context_str:
        msg += f" [{context_str}]"
    logger.info(msg)


def log_operation_complete(
    logger: logging.Logger,
    operation_name: str,
    duration: Optional[float] = None,
    **context
) -> None:
    """
    Log the completion of an operation.
    
    Args:
        logger: Logger instance
        operation_name: Name of the operation
        duration: Optional duration in seconds
        **context: Additional context information
    """
    context_str = " | ".join(f"{k}={v}" for k, v in context.items())
    msg = f"Completed {operation_name}"
    if duration is not None:
        msg += f" in {duration:.2f}s"
    if context_str:
        msg += f" [{context_str}]"
    logger.info(msg)


def log_operation_error(
    logger: logging.Logger,
    operation_name: str,
    error: Exception,
    **context
) -> None:
    """
    Log an operation error.
    
    Args:
        logger: Logger instance
        operation_name: Name of the operation
        error: Exception that occurred
        **context: Additional context information
    """
    context_str = " | ".join(f"{k}={v}" for k, v in context.items())
    msg = f"Error in {operation_name}: {str(error)}"
    if context_str:
        msg += f" [{context_str}]"
    logger.error(msg, exc_info=True)


def log_state_change(
    logger: logging.Logger,
    component: str,
    old_state: str,
    new_state: str,
    **context
) -> None:
    """
    Log a state change.
    
    Args:
        logger: Logger instance
        component: Component name
        old_state: Previous state
        new_state: New state
        **context: Additional context information
    """
    context_str = " | ".join(f"{k}={v}" for k, v in context.items())
    msg = f"{component}: {old_state} -> {new_state}"
    if context_str:
        msg += f" [{context_str}]"
    logger.info(msg)


def log_performance_metric(
    logger: logging.Logger,
    metric_name: str,
    value: float,
    unit: str = "ms",
    **context
) -> None:
    """
    Log a performance metric.
    
    Args:
        logger: Logger instance
        metric_name: Name of the metric
        value: Metric value
        unit: Unit of measurement
        **context: Additional context information
    """
    context_str = " | ".join(f"{k}={v}" for k, v in context.items())
    msg = f"Metric: {metric_name} = {value}{unit}"
    if context_str:
        msg += f" [{context_str}]"
    logger.info(msg)


def log_security_event(
    logger: logging.Logger,
    event_type: str,
    severity: str = "INFO",
    **context
) -> None:
    """
    Log a security-related event.
    
    Args:
        logger: Logger instance
        event_type: Type of security event
        severity: Severity level (INFO, WARNING, ERROR)
        **context: Additional context information
    """
    context_str = " | ".join(f"{k}={v}" for k, v in context.items())
    msg = f"[SECURITY] {event_type}"
    if context_str:
        msg += f" [{context_str}]"
    
    level = getattr(logging, severity, logging.INFO)
    logger.log(level, msg)


__all__ = [
    "LogLevel",
    "LogCategory",
    "get_category_logger",
    "log_operation_start",
    "log_operation_complete",
    "log_operation_error",
    "log_state_change",
    "log_performance_metric",
    "log_security_event",
]
