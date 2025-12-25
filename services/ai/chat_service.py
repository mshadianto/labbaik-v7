"""
LABBAIK AI v6.0 - Chat Service Implementations
==============================================
Chat completion services for Groq and OpenAI.
"""

import time
import logging
from typing import Optional, Generator, AsyncGenerator, List, Dict, Any
from dataclasses import dataclass

from services.ai.base import (
    BaseChatService,
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    MessageRole,
    RateLimiter,
    AIServiceFactory,
)
from core.exceptions import AIServiceError, AIRateLimitError, AIQuotaExceededError

logger = logging.getLogger(__name__)


# =============================================================================
# GROQ CHAT SERVICE
# =============================================================================

class GroqChatService(BaseChatService):
    """Chat service implementation for Groq API."""
    
    DEFAULT_MODEL = "llama-3.3-70b-versatile"
    AVAILABLE_MODELS = [
        "llama-3.3-70b-versatile",
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "gemma2-9b-it",
    ]
    
    def __init__(
        self,
        api_key: str,
        model: str = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        requests_per_minute: int = 30,
        tokens_per_minute: int = 100000,
        **kwargs
    ):
        super().__init__(api_key, **kwargs)
        self.model = model or self.DEFAULT_MODEL
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._client = None
        self._rate_limiter = RateLimiter(requests_per_minute, tokens_per_minute)
    
    @property
    def provider_name(self) -> str:
        return "groq"
    
    def initialize(self) -> bool:
        """Initialize Groq client."""
        try:
            from groq import Groq
            self._client = Groq(api_key=self.api_key)
            self._initialized = True
            logger.info(f"Groq service initialized with model: {self.model}")
            return True
        except ImportError:
            logger.error("Groq package not installed. Run: pip install groq")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize Groq: {e}")
            return False
    
    def _check_rate_limit(self, estimated_tokens: int = 1000):
        """Check and wait for rate limit if needed."""
        can_proceed, wait_time = self._rate_limiter.can_proceed(estimated_tokens)
        if not can_proceed:
            logger.warning(f"Rate limit hit, waiting {wait_time:.1f}s")
            time.sleep(wait_time)
    
    def _prepare_messages(self, messages: List[ChatMessage]) -> List[Dict[str, str]]:
        """Convert ChatMessage objects to API format."""
        return [msg.to_dict() for msg in messages]
    
    def complete(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """Generate chat completion."""
        self._ensure_initialized()
        self._check_rate_limit(request.max_tokens)
        
        start_time = time.time()
        
        try:
            response = self._client.chat.completions.create(
                model=request.model or self.model,
                messages=self._prepare_messages(request.messages),
                max_tokens=request.max_tokens or self.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                stop=request.stop_sequences,
                stream=False,
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            # Record usage
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
            self._rate_limiter.record_request(usage["total_tokens"])
            
            return ChatCompletionResponse(
                content=response.choices[0].message.content,
                model=response.model,
                usage=usage,
                finish_reason=response.choices[0].finish_reason,
                latency_ms=latency_ms,
            )
            
        except Exception as e:
            error_msg = str(e).lower()
            if "rate_limit" in error_msg:
                raise AIRateLimitError(provider="groq")
            elif "quota" in error_msg:
                raise AIQuotaExceededError(provider="groq")
            else:
                logger.error(f"Groq API error: {e}")
                raise AIServiceError(message=str(e), provider="groq")
    
    def stream(self, request: ChatCompletionRequest) -> Generator[str, None, None]:
        """Generate streaming chat completion."""
        self._ensure_initialized()
        self._check_rate_limit(request.max_tokens)
        
        try:
            stream_response = self._client.chat.completions.create(
                model=request.model or self.model,
                messages=self._prepare_messages(request.messages),
                max_tokens=request.max_tokens or self.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                stop=request.stop_sequences,
                stream=True,
            )
            
            for chunk in stream_response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
            
            self._rate_limiter.record_request(request.max_tokens // 2)
            
        except Exception as e:
            logger.error(f"Groq streaming error: {e}")
            raise AIServiceError(message=str(e), provider="groq")
    
    async def acomplete(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """Async chat completion."""
        self._ensure_initialized()
        
        try:
            from groq import AsyncGroq
            async_client = AsyncGroq(api_key=self.api_key)
            
            start_time = time.time()
            
            response = await async_client.chat.completions.create(
                model=request.model or self.model,
                messages=self._prepare_messages(request.messages),
                max_tokens=request.max_tokens or self.max_tokens,
                temperature=request.temperature,
                stream=False,
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
            
            return ChatCompletionResponse(
                content=response.choices[0].message.content,
                model=response.model,
                usage=usage,
                finish_reason=response.choices[0].finish_reason,
                latency_ms=latency_ms,
            )
            
        except Exception as e:
            logger.error(f"Groq async error: {e}")
            raise AIServiceError(message=str(e), provider="groq")
    
    async def astream(self, request: ChatCompletionRequest) -> AsyncGenerator[str, None]:
        """Async streaming chat completion."""
        self._ensure_initialized()
        
        try:
            from groq import AsyncGroq
            async_client = AsyncGroq(api_key=self.api_key)
            
            stream_response = await async_client.chat.completions.create(
                model=request.model or self.model,
                messages=self._prepare_messages(request.messages),
                max_tokens=request.max_tokens or self.max_tokens,
                temperature=request.temperature,
                stream=True,
            )
            
            async for chunk in stream_response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"Groq async streaming error: {e}")
            raise AIServiceError(message=str(e), provider="groq")


# =============================================================================
# OPENAI CHAT SERVICE
# =============================================================================

class OpenAIChatService(BaseChatService):
    """Chat service implementation for OpenAI API."""
    
    DEFAULT_MODEL = "gpt-4o-mini"
    AVAILABLE_MODELS = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-3.5-turbo",
    ]
    
    def __init__(
        self,
        api_key: str,
        model: str = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        requests_per_minute: int = 60,
        tokens_per_minute: int = 150000,
        **kwargs
    ):
        super().__init__(api_key, **kwargs)
        self.model = model or self.DEFAULT_MODEL
        self.max_tokens = max_tokens
        self.temperature = temperature
        self._client = None
        self._rate_limiter = RateLimiter(requests_per_minute, tokens_per_minute)
    
    @property
    def provider_name(self) -> str:
        return "openai"
    
    def initialize(self) -> bool:
        """Initialize OpenAI client."""
        try:
            from openai import OpenAI
            self._client = OpenAI(api_key=self.api_key)
            self._initialized = True
            logger.info(f"OpenAI service initialized with model: {self.model}")
            return True
        except ImportError:
            logger.error("OpenAI package not installed. Run: pip install openai")
            return False
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI: {e}")
            return False
    
    def _prepare_messages(self, messages: List[ChatMessage]) -> List[Dict[str, str]]:
        """Convert ChatMessage objects to API format."""
        return [msg.to_dict() for msg in messages]
    
    def complete(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """Generate chat completion."""
        self._ensure_initialized()
        
        start_time = time.time()
        
        try:
            response = self._client.chat.completions.create(
                model=request.model or self.model,
                messages=self._prepare_messages(request.messages),
                max_tokens=request.max_tokens or self.max_tokens,
                temperature=request.temperature,
                top_p=request.top_p,
                stop=request.stop_sequences,
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
            
            return ChatCompletionResponse(
                content=response.choices[0].message.content,
                model=response.model,
                usage=usage,
                finish_reason=response.choices[0].finish_reason,
                latency_ms=latency_ms,
            )
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise AIServiceError(message=str(e), provider="openai")
    
    def stream(self, request: ChatCompletionRequest) -> Generator[str, None, None]:
        """Generate streaming chat completion."""
        self._ensure_initialized()
        
        try:
            stream_response = self._client.chat.completions.create(
                model=request.model or self.model,
                messages=self._prepare_messages(request.messages),
                max_tokens=request.max_tokens or self.max_tokens,
                temperature=request.temperature,
                stream=True,
            )
            
            for chunk in stream_response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"OpenAI streaming error: {e}")
            raise AIServiceError(message=str(e), provider="openai")
    
    async def acomplete(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """Async chat completion."""
        self._ensure_initialized()
        
        try:
            from openai import AsyncOpenAI
            async_client = AsyncOpenAI(api_key=self.api_key)
            
            start_time = time.time()
            
            response = await async_client.chat.completions.create(
                model=request.model or self.model,
                messages=self._prepare_messages(request.messages),
                max_tokens=request.max_tokens or self.max_tokens,
                temperature=request.temperature,
            )
            
            latency_ms = (time.time() - start_time) * 1000
            
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
            }
            
            return ChatCompletionResponse(
                content=response.choices[0].message.content,
                model=response.model,
                usage=usage,
                finish_reason=response.choices[0].finish_reason,
                latency_ms=latency_ms,
            )
            
        except Exception as e:
            logger.error(f"OpenAI async error: {e}")
            raise AIServiceError(message=str(e), provider="openai")
    
    async def astream(self, request: ChatCompletionRequest) -> AsyncGenerator[str, None]:
        """Async streaming chat completion."""
        self._ensure_initialized()
        
        try:
            from openai import AsyncOpenAI
            async_client = AsyncOpenAI(api_key=self.api_key)
            
            stream_response = await async_client.chat.completions.create(
                model=request.model or self.model,
                messages=self._prepare_messages(request.messages),
                max_tokens=request.max_tokens or self.max_tokens,
                temperature=request.temperature,
                stream=True,
            )
            
            async for chunk in stream_response:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            logger.error(f"OpenAI async streaming error: {e}")
            raise AIServiceError(message=str(e), provider="openai")


# =============================================================================
# UNIFIED CHAT SERVICE WITH FALLBACK
# =============================================================================

class UnifiedChatService:
    """
    Unified chat service with automatic fallback between providers.
    Tries primary provider first, falls back to secondary if it fails.
    """
    
    def __init__(
        self,
        primary_service: BaseChatService,
        fallback_service: Optional[BaseChatService] = None,
        max_retries: int = 2
    ):
        self.primary = primary_service
        self.fallback = fallback_service
        self.max_retries = max_retries
        self._current_service = primary_service
    
    def complete(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """Generate completion with automatic fallback."""
        for attempt in range(self.max_retries):
            try:
                return self._current_service.complete(request)
            except AIServiceError as e:
                logger.warning(f"Service error (attempt {attempt + 1}): {e}")
                if self.fallback and self._current_service == self.primary:
                    logger.info("Switching to fallback service")
                    self._current_service = self.fallback
                elif attempt == self.max_retries - 1:
                    raise
        
        # Reset to primary for next request
        self._current_service = self.primary
        raise AIServiceError(message="All providers failed")
    
    def stream(self, request: ChatCompletionRequest) -> Generator[str, None, None]:
        """Generate streaming completion with fallback."""
        try:
            yield from self._current_service.stream(request)
        except AIServiceError as e:
            if self.fallback and self._current_service == self.primary:
                logger.info("Switching to fallback service for streaming")
                self._current_service = self.fallback
                yield from self._current_service.stream(request)
            else:
                raise
        finally:
            self._current_service = self.primary


# =============================================================================
# REGISTER SERVICES
# =============================================================================

AIServiceFactory.register_chat_service("groq", GroqChatService)
AIServiceFactory.register_chat_service("openai", OpenAIChatService)
