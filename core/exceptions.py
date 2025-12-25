"""
LABBAIK AI v6.0 - Custom Exceptions
===================================
Centralized exception handling with custom exception classes.
"""

from typing import Optional, Dict, Any
from http import HTTPStatus


class LABBAIKException(Exception):
    """Base exception for all LABBAIK-related errors."""
    
    def __init__(
        self,
        message: str = "An error occurred",
        code: str = "LABBAIK_ERROR",
        status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert exception to dictionary for API responses."""
        return {
            "error": True,
            "code": self.code,
            "message": self.message,
            "status_code": self.status_code,
            "details": self.details
        }


# =============================================================================
# AUTHENTICATION EXCEPTIONS
# =============================================================================

class AuthenticationError(LABBAIKException):
    """Raised when authentication fails."""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="AUTH_ERROR",
            status_code=HTTPStatus.UNAUTHORIZED,
            details=details
        )


class InvalidCredentialsError(AuthenticationError):
    """Raised when credentials are invalid."""
    
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message=message, details={"type": "invalid_credentials"})


class TokenExpiredError(AuthenticationError):
    """Raised when authentication token has expired."""
    
    def __init__(self, message: str = "Your session has expired. Please login again."):
        super().__init__(message=message, details={"type": "token_expired"})


class TokenInvalidError(AuthenticationError):
    """Raised when authentication token is invalid."""
    
    def __init__(self, message: str = "Invalid authentication token"):
        super().__init__(message=message, details={"type": "token_invalid"})


class SessionExpiredError(AuthenticationError):
    """Raised when user session has expired."""
    
    def __init__(self, message: str = "Session expired. Please login again."):
        super().__init__(message=message, details={"type": "session_expired"})


# =============================================================================
# AUTHORIZATION EXCEPTIONS
# =============================================================================

class AuthorizationError(LABBAIKException):
    """Raised when user lacks required permissions."""
    
    def __init__(
        self,
        message: str = "You don't have permission to perform this action",
        required_role: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if required_role:
            details["required_role"] = required_role
        super().__init__(
            message=message,
            code="AUTHORIZATION_ERROR",
            status_code=HTTPStatus.FORBIDDEN,
            details=details
        )


class InsufficientPermissionsError(AuthorizationError):
    """Raised when user has insufficient permissions."""
    pass


class FeatureNotAvailableError(AuthorizationError):
    """Raised when feature is not available for user's subscription tier."""
    
    def __init__(
        self,
        feature: str,
        required_tier: str,
        message: Optional[str] = None
    ):
        message = message or f"Feature '{feature}' requires {required_tier} subscription"
        super().__init__(
            message=message,
            details={
                "feature": feature,
                "required_tier": required_tier,
                "type": "feature_locked"
            }
        )


# =============================================================================
# VALIDATION EXCEPTIONS
# =============================================================================

class ValidationError(LABBAIKException):
    """Raised when input validation fails."""
    
    def __init__(
        self,
        message: str = "Validation failed",
        field: Optional[str] = None,
        errors: Optional[Dict[str, str]] = None
    ):
        details = {}
        if field:
            details["field"] = field
        if errors:
            details["errors"] = errors
        super().__init__(
            message=message,
            code="VALIDATION_ERROR",
            status_code=HTTPStatus.BAD_REQUEST,
            details=details
        )


class InvalidInputError(ValidationError):
    """Raised when input data is invalid."""
    pass


class MissingFieldError(ValidationError):
    """Raised when required field is missing."""
    
    def __init__(self, field: str):
        super().__init__(
            message=f"Required field '{field}' is missing",
            field=field
        )


class InvalidFormatError(ValidationError):
    """Raised when data format is invalid."""
    
    def __init__(self, field: str, expected_format: str):
        super().__init__(
            message=f"Invalid format for '{field}'. Expected: {expected_format}",
            field=field,
            errors={"expected_format": expected_format}
        )


# =============================================================================
# DATABASE EXCEPTIONS
# =============================================================================

class DatabaseError(LABBAIKException):
    """Base exception for database-related errors."""
    
    def __init__(
        self,
        message: str = "Database error occurred",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            code="DATABASE_ERROR",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=details
        )


class ConnectionError(DatabaseError):
    """Raised when database connection fails."""
    
    def __init__(self, message: str = "Failed to connect to database"):
        super().__init__(message=message, details={"type": "connection_failed"})


class RecordNotFoundError(DatabaseError):
    """Raised when requested record is not found."""
    
    def __init__(
        self,
        entity: str,
        identifier: Optional[str] = None
    ):
        message = f"{entity} not found"
        if identifier:
            message = f"{entity} with ID '{identifier}' not found"
        super().__init__(
            message=message,
            details={"entity": entity, "identifier": identifier}
        )
        self.status_code = HTTPStatus.NOT_FOUND


class DuplicateRecordError(DatabaseError):
    """Raised when attempting to create duplicate record."""
    
    def __init__(
        self,
        entity: str,
        field: str,
        value: str
    ):
        super().__init__(
            message=f"{entity} with {field} '{value}' already exists",
            details={"entity": entity, "field": field, "value": value}
        )
        self.status_code = HTTPStatus.CONFLICT


class TransactionError(DatabaseError):
    """Raised when database transaction fails."""
    
    def __init__(self, message: str = "Transaction failed"):
        super().__init__(message=message, details={"type": "transaction_failed"})


# =============================================================================
# AI SERVICE EXCEPTIONS
# =============================================================================

class AIServiceError(LABBAIKException):
    """Base exception for AI service errors."""
    
    def __init__(
        self,
        message: str = "AI service error",
        provider: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if provider:
            details["provider"] = provider
        super().__init__(
            message=message,
            code="AI_SERVICE_ERROR",
            status_code=HTTPStatus.SERVICE_UNAVAILABLE,
            details=details
        )


class AIQuotaExceededError(AIServiceError):
    """Raised when AI API quota is exceeded."""
    
    def __init__(self, provider: str):
        super().__init__(
            message="AI service quota exceeded. Please try again later.",
            provider=provider,
            details={"type": "quota_exceeded"}
        )


class AIRateLimitError(AIServiceError):
    """Raised when AI API rate limit is hit."""
    
    def __init__(
        self,
        provider: str,
        retry_after: Optional[int] = None
    ):
        details = {"type": "rate_limited"}
        if retry_after:
            details["retry_after"] = retry_after
        super().__init__(
            message="Too many requests. Please wait a moment.",
            provider=provider,
            details=details
        )


class AIModelError(AIServiceError):
    """Raised when AI model returns an error."""
    
    def __init__(
        self,
        provider: str,
        model: str,
        message: str = "Model error"
    ):
        super().__init__(
            message=message,
            provider=provider,
            details={"model": model, "type": "model_error"}
        )


class EmbeddingError(AIServiceError):
    """Raised when embedding generation fails."""
    
    def __init__(self, message: str = "Failed to generate embeddings"):
        super().__init__(message=message, details={"type": "embedding_error"})


class RAGError(AIServiceError):
    """Raised when RAG retrieval fails."""
    
    def __init__(self, message: str = "Failed to retrieve relevant context"):
        super().__init__(message=message, details={"type": "rag_error"})


# =============================================================================
# BOOKING EXCEPTIONS
# =============================================================================

class BookingError(LABBAIKException):
    """Base exception for booking-related errors."""
    
    def __init__(
        self,
        message: str = "Booking error",
        booking_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if booking_id:
            details["booking_id"] = booking_id
        super().__init__(
            message=message,
            code="BOOKING_ERROR",
            status_code=HTTPStatus.BAD_REQUEST,
            details=details
        )


class BookingNotFoundError(BookingError):
    """Raised when booking is not found."""
    
    def __init__(self, booking_id: str):
        super().__init__(
            message=f"Booking '{booking_id}' not found",
            booking_id=booking_id
        )
        self.status_code = HTTPStatus.NOT_FOUND


class InvalidBookingStatusError(BookingError):
    """Raised when booking status transition is invalid."""
    
    def __init__(
        self,
        booking_id: str,
        current_status: str,
        target_status: str
    ):
        super().__init__(
            message=f"Cannot change booking status from '{current_status}' to '{target_status}'",
            booking_id=booking_id,
            details={
                "current_status": current_status,
                "target_status": target_status
            }
        )


class BookingCapacityError(BookingError):
    """Raised when booking exceeds capacity."""
    
    def __init__(self, message: str = "Booking capacity exceeded"):
        super().__init__(message=message, details={"type": "capacity_exceeded"})


# =============================================================================
# PLUGIN EXCEPTIONS
# =============================================================================

class PluginError(LABBAIKException):
    """Base exception for plugin-related errors."""
    
    def __init__(
        self,
        message: str = "Plugin error",
        plugin_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        if plugin_name:
            details["plugin_name"] = plugin_name
        super().__init__(
            message=message,
            code="PLUGIN_ERROR",
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            details=details
        )


class PluginNotFoundError(PluginError):
    """Raised when plugin is not found."""
    
    def __init__(self, plugin_name: str):
        super().__init__(
            message=f"Plugin '{plugin_name}' not found",
            plugin_name=plugin_name
        )
        self.status_code = HTTPStatus.NOT_FOUND


class PluginLoadError(PluginError):
    """Raised when plugin fails to load."""
    
    def __init__(self, plugin_name: str, reason: str):
        super().__init__(
            message=f"Failed to load plugin '{plugin_name}': {reason}",
            plugin_name=plugin_name,
            details={"reason": reason}
        )


class PluginDependencyError(PluginError):
    """Raised when plugin dependency is missing."""
    
    def __init__(self, plugin_name: str, dependency: str):
        super().__init__(
            message=f"Plugin '{plugin_name}' requires missing dependency: {dependency}",
            plugin_name=plugin_name,
            details={"missing_dependency": dependency}
        )


# =============================================================================
# EXTERNAL SERVICE EXCEPTIONS
# =============================================================================

class ExternalServiceError(LABBAIKException):
    """Base exception for external service errors."""
    
    def __init__(
        self,
        service: str,
        message: str = "External service error",
        details: Optional[Dict[str, Any]] = None
    ):
        details = details or {}
        details["service"] = service
        super().__init__(
            message=message,
            code="EXTERNAL_SERVICE_ERROR",
            status_code=HTTPStatus.BAD_GATEWAY,
            details=details
        )


class PaymentServiceError(ExternalServiceError):
    """Raised when payment service fails."""
    
    def __init__(
        self,
        provider: str,
        message: str = "Payment processing failed"
    ):
        super().__init__(service=f"payment:{provider}", message=message)


class EmailServiceError(ExternalServiceError):
    """Raised when email service fails."""
    
    def __init__(self, message: str = "Failed to send email"):
        super().__init__(service="email", message=message)


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def handle_exception(exc: Exception) -> Dict[str, Any]:
    """Convert any exception to a standardized error response."""
    if isinstance(exc, LABBAIKException):
        return exc.to_dict()
    
    # Default error response for unknown exceptions
    return {
        "error": True,
        "code": "INTERNAL_ERROR",
        "message": "An unexpected error occurred",
        "status_code": HTTPStatus.INTERNAL_SERVER_ERROR,
        "details": {"original_error": str(exc)}
    }
