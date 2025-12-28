"""
LABBAIK AI - Speech-to-Text Service
====================================
Audio transcription using Groq Whisper API.
"""

import os
import logging
import tempfile
from typing import Optional
from groq import Groq

logger = logging.getLogger(__name__)


class SpeechService:
    """Speech-to-text service using Groq Whisper API."""

    DEFAULT_MODEL = "whisper-large-v3-turbo"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize speech service.

        Args:
            api_key: Groq API key (uses GROQ_API_KEY env var if not provided)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY", "")
        self._client = None

    @property
    def client(self) -> Groq:
        """Lazy-initialize Groq client."""
        if self._client is None:
            if not self.api_key:
                raise ValueError("GROQ_API_KEY not configured")
            self._client = Groq(api_key=self.api_key)
        return self._client

    def transcribe(
        self,
        audio_bytes: bytes,
        language: str = "id",
        filename: str = "audio.wav"
    ) -> str:
        """Transcribe audio to text.

        Args:
            audio_bytes: Raw audio data
            language: Language code (id=Indonesian, ar=Arabic, en=English)
            filename: Filename hint for format detection

        Returns:
            Transcribed text
        """
        if not audio_bytes:
            return ""

        try:
            # Write audio to temp file (Groq requires file path)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(audio_bytes)
                temp_path = f.name

            # Transcribe using Groq Whisper
            with open(temp_path, "rb") as audio_file:
                transcription = self.client.audio.transcriptions.create(
                    file=(filename, audio_file.read()),
                    model=self.DEFAULT_MODEL,
                    language=language,
                    response_format="text",
                )

            # Cleanup temp file
            try:
                os.unlink(temp_path)
            except Exception:
                pass

            result = transcription.strip() if isinstance(transcription, str) else str(transcription).strip()
            logger.info(f"Transcribed {len(audio_bytes)} bytes -> {len(result)} chars")
            return result

        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise


# Singleton instance
_speech_service: Optional[SpeechService] = None


def get_speech_service() -> SpeechService:
    """Get singleton speech service instance."""
    global _speech_service
    if _speech_service is None:
        _speech_service = SpeechService()
    return _speech_service


def transcribe_audio(audio_bytes: bytes, language: str = "id") -> str:
    """Convenience function to transcribe audio.

    Args:
        audio_bytes: Raw audio data
        language: Language code (id=Indonesian, ar=Arabic, en=English)

    Returns:
        Transcribed text
    """
    service = get_speech_service()
    return service.transcribe(audio_bytes, language=language)
