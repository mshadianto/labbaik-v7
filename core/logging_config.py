"""
LABBAIK AI v6.0 - Logging Configuration
=======================================
Centralized logging with structured output, rotation, and multiple handlers.
"""

import logging
import logging.handlers
import sys
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
from functools import wraps
import traceback
import time

from core.config import get_settings


# =============================================================================
# CUSTOM FORMATTERS
# =============================================================================

class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else None,
                "message": str(record.exc_info[1]) if record.exc_info[1] else None,
                "traceback": self.formatException(record.exc_info)
            }
        
        # Add extra fields
        if hasattr(record, "extra_data"):
            log_data["extra"] = record.extra_data
        
        return json.dumps(log_data, ensure_ascii=False)


class ColoredFormatter(logging.Formatter):
    """Colored formatter for console output."""
    
    COLORS = {
        "DEBUG": "\033[36m",      # Cyan
        "INFO": "\033[32m",       # Green
        "WARNING": "\033[33m",    # Yellow
        "ERROR": "\033[31m",      # Red
        "CRITICAL": "\033[35m",   # Magenta
    }
    RESET = "\033[0m"
    
    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{color}{record.levelname}{self.RESET}"
        return super().format(record)


# =============================================================================
# CUSTOM FILTERS
# =============================================================================

class ContextFilter(logging.Filter):
    """Filter that adds contextual information to log records."""
    
    def __init__(self, app_name: str = "labbaik"):
        super().__init__()
        self.app_name = app_name
    
    def filter(self, record: logging.LogRecord) -> bool:
        record.app_name = self.app_name
        return True


class SensitiveDataFilter(logging.Filter):
    """Filter that masks sensitive data in log messages."""
    
    SENSITIVE_PATTERNS = [
        "password", "secret", "token", "api_key", "apikey",
        "authorization", "auth", "credential", "credit_card"
    ]
    
    def filter(self, record: logging.LogRecord) -> bool:
        message = record.getMessage().lower()
        for pattern in self.SENSITIVE_PATTERNS:
            if pattern in message:
                # Mask the sensitive data
                record.msg = self._mask_sensitive(record.msg)
                break
        return True
    
    def _mask_sensitive(self, message: str) -> str:
        """Mask sensitive data in message."""
        # Simple masking - replace values after = or :
        import re
        patterns = [
            r'(password["\']?\s*[:=]\s*["\']?)([^"\'\s,}]+)',
            r'(api_key["\']?\s*[:=]\s*["\']?)([^"\'\s,}]+)',
            r'(token["\']?\s*[:=]\s*["\']?)([^"\'\s,}]+)',
            r'(secret["\']?\s*[:=]\s*["\']?)([^"\'\s,}]+)',
        ]
        for pattern in patterns:
            message = re.sub(pattern, r'\1***MASKED***', message, flags=re.IGNORECASE)
        return message


# =============================================================================
# LOGGER SETUP
# =============================================================================

def setup_logging(
    level: str = "INFO",
    log_format: Optional[str] = None,
    log_file: Optional[str] = None,
    json_format: bool = False,
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Setup application logging with multiple handlers.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_format: Custom log format string
        log_file: Path to log file (optional)
        json_format: Use JSON formatting
        max_bytes: Max log file size before rotation
        backup_count: Number of backup files to keep
    
    Returns:
        Root logger instance
    """
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Default format
    if log_format is None:
        log_format = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    
    if json_format:
        console_handler.setFormatter(JSONFormatter())
    else:
        console_handler.setFormatter(ColoredFormatter(log_format))
    
    # Add filters
    console_handler.addFilter(ContextFilter("labbaik"))
    console_handler.addFilter(SensitiveDataFilter())
    
    root_logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(JSONFormatter())  # Always JSON for files
        file_handler.addFilter(ContextFilter("labbaik"))
        file_handler.addFilter(SensitiveDataFilter())
        
        root_logger.addHandler(file_handler)
    
    # Suppress noisy loggers
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("chromadb").setLevel(logging.WARNING)
    logging.getLogger("sentence_transformers").setLevel(logging.WARNING)
    
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name.
    
    Args:
        name: Logger name (usually __name__)
    
    Returns:
        Logger instance
    """
    return logging.getLogger(name)


# =============================================================================
# LOGGING DECORATORS
# =============================================================================

def log_execution(
    logger: Optional[logging.Logger] = None,
    level: int = logging.INFO,
    log_args: bool = True,
    log_result: bool = False,
    log_time: bool = True
):
    """
    Decorator to log function execution.
    
    Args:
        logger: Logger instance (uses function's module logger if None)
        level: Log level
        log_args: Whether to log function arguments
        log_result: Whether to log return value
        log_time: Whether to log execution time
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = logging.getLogger(func.__module__)
            
            # Log entry
            entry_msg = f"Entering {func.__name__}"
            if log_args:
                # Mask sensitive arguments
                safe_kwargs = {k: "***" if "password" in k.lower() or "secret" in k.lower() 
                              else v for k, v in kwargs.items()}
                entry_msg += f" | args={args[:3]}... | kwargs={safe_kwargs}"
            
            logger.log(level, entry_msg)
            
            # Execute function
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                
                # Log exit
                exit_msg = f"Exiting {func.__name__}"
                if log_time:
                    elapsed = time.time() - start_time
                    exit_msg += f" | time={elapsed:.3f}s"
                if log_result:
                    exit_msg += f" | result={str(result)[:100]}"
                
                logger.log(level, exit_msg)
                return result
                
            except Exception as e:
                elapsed = time.time() - start_time
                logger.error(
                    f"Error in {func.__name__} | time={elapsed:.3f}s | error={str(e)}",
                    exc_info=True
                )
                raise
        
        return wrapper
    return decorator


def log_error(
    logger: Optional[logging.Logger] = None,
    reraise: bool = True,
    default_return: Any = None
):
    """
    Decorator to log exceptions.
    
    Args:
        logger: Logger instance
        reraise: Whether to re-raise the exception
        default_return: Default return value if not reraising
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal logger
            if logger is None:
                logger = logging.getLogger(func.__module__)
            
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(
                    f"Exception in {func.__name__}: {str(e)}",
                    exc_info=True,
                    extra={"extra_data": {"function": func.__name__}}
                )
                if reraise:
                    raise
                return default_return
        
        return wrapper
    return decorator


# =============================================================================
# CONTEXT MANAGERS
# =============================================================================

class LogContext:
    """Context manager for adding context to log messages."""
    
    _context: Dict[str, Any] = {}
    
    def __init__(self, **kwargs):
        self.context = kwargs
    
    def __enter__(self):
        LogContext._context.update(self.context)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        for key in self.context:
            LogContext._context.pop(key, None)


# =============================================================================
# AUDIT LOGGING
# =============================================================================

class AuditLogger:
    """Special logger for audit trail events."""
    
    def __init__(self, name: str = "audit"):
        self.logger = logging.getLogger(f"labbaik.audit.{name}")
        self.logger.setLevel(logging.INFO)
    
    def log_action(
        self,
        action: str,
        user_id: Optional[str] = None,
        resource: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
        success: bool = True
    ):
        """Log an audit event."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "user_id": user_id,
            "resource": resource,
            "resource_id": resource_id,
            "success": success,
            "details": details or {}
        }
        
        level = logging.INFO if success else logging.WARNING
        self.logger.log(level, json.dumps(event, ensure_ascii=False))
    
    def log_login(self, user_id: str, success: bool = True, method: str = "password"):
        """Log login attempt."""
        self.log_action(
            action="login",
            user_id=user_id,
            success=success,
            details={"method": method}
        )
    
    def log_data_access(
        self,
        user_id: str,
        resource: str,
        resource_id: str,
        operation: str = "read"
    ):
        """Log data access event."""
        self.log_action(
            action=f"data_{operation}",
            user_id=user_id,
            resource=resource,
            resource_id=resource_id
        )


# =============================================================================
# PERFORMANCE LOGGING
# =============================================================================

class PerformanceLogger:
    """Logger for performance metrics."""
    
    def __init__(self, name: str = "performance"):
        self.logger = logging.getLogger(f"labbaik.perf.{name}")
        self.logger.setLevel(logging.INFO)
    
    def log_metric(
        self,
        metric_name: str,
        value: float,
        unit: str = "ms",
        tags: Optional[Dict[str, str]] = None
    ):
        """Log a performance metric."""
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "metric": metric_name,
            "value": value,
            "unit": unit,
            "tags": tags or {}
        }
        self.logger.info(json.dumps(event, ensure_ascii=False))
    
    def log_response_time(self, endpoint: str, duration_ms: float, status_code: int):
        """Log API response time."""
        self.log_metric(
            metric_name="response_time",
            value=duration_ms,
            unit="ms",
            tags={"endpoint": endpoint, "status": str(status_code)}
        )
    
    def log_ai_latency(self, provider: str, model: str, duration_ms: float, tokens: int):
        """Log AI service latency."""
        self.log_metric(
            metric_name="ai_latency",
            value=duration_ms,
            unit="ms",
            tags={"provider": provider, "model": model, "tokens": str(tokens)}
        )


# =============================================================================
# INITIALIZE LOGGING ON IMPORT
# =============================================================================

def init_logging():
    """Initialize logging with settings from config."""
    try:
        settings = get_settings()
        setup_logging(
            level=settings.logging.level,
            log_format=settings.logging.format,
            log_file=settings.logging.file_path,
            json_format=settings.is_production(),
            max_bytes=settings.logging.max_bytes,
            backup_count=settings.logging.backup_count
        )
    except Exception:
        # Fallback to basic logging if config fails
        setup_logging(level="INFO")


# Create singleton loggers
audit_logger = AuditLogger()
perf_logger = PerformanceLogger()
