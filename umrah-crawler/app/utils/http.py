"""HTTP client utilities."""
import httpx
from typing import Dict, Any, Optional

# Default timeout
DEFAULT_TIMEOUT = 30.0


async def get(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: float = DEFAULT_TIMEOUT
) -> httpx.Response:
    """
    Async HTTP GET request.

    Args:
        url: Request URL
        headers: Optional headers
        params: Optional query parameters
        timeout: Request timeout in seconds

    Returns:
        httpx.Response object
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response


async def post(
    url: str,
    headers: Optional[Dict[str, str]] = None,
    data: Optional[Dict[str, Any]] = None,
    json: Optional[Dict[str, Any]] = None,
    timeout: float = DEFAULT_TIMEOUT
) -> httpx.Response:
    """
    Async HTTP POST request.

    Args:
        url: Request URL
        headers: Optional headers
        data: Form data
        json: JSON body
        timeout: Request timeout in seconds

    Returns:
        httpx.Response object
    """
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(url, headers=headers, data=data, json=json)
        response.raise_for_status()
        return response
